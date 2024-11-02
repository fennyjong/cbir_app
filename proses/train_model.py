import os
import numpy as np
from keras.applications.resnet import ResNet50, preprocess_input
from keras.preprocessing.image import load_img, img_to_array
from models import SongketDataset, SongketFeatures, db  # Adjust this import to your actual database module
from tqdm import tqdm  # For progress tracking

class CBIRModel:
    def __init__(self, upload_folder, batch_size=1000, features_path=None):
        self.upload_folder = upload_folder
        self.features_path = features_path
        self.batch_size = batch_size
        self.img_size = (255, 255)
        self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

    def extract_features(self, img_path):
        """Extract features from the given image path."""
        try:
            img = load_img(img_path, target_size=self.img_size)
            x = preprocess_input(img_to_array(img)[None, ...])
            return self.model.predict(x, verbose=0).flatten()  # Disable per-image prediction verbose
        except Exception as e:
            print(f"Error extracting features from {img_path}: {str(e)}")
            return None

    def process_database(self):
        """Process the image database to extract and save features in batches."""
        datasets = SongketDataset.query.all()
        if not datasets:
            return False, "No datasets found"

        processed, skipped = 0, 0
        existing_image_names = {feature.image_name for feature in SongketFeatures.query.all()}
        
        # Prepare batches
        pending_features = []
        total_datasets = len(datasets)
        
        print(f"Processing {total_datasets} images in batches of {self.batch_size}")
        
        # Use tqdm for progress tracking
        for dataset in tqdm(datasets, desc="Processing images", unit="img"):
            img_path = os.path.join(self.upload_folder, dataset.image_filename)
            if not os.path.exists(img_path):
                print(f"\nImage not found: {img_path}")
                continue

            if dataset.image_filename in existing_image_names:
                skipped += 1
                continue

            features = self.extract_features(img_path)
            if features is not None:
                pending_features.append({
                    'image_name': dataset.image_filename,
                    'features': features.tolist()
                })
                
                # Process batch when it reaches batch_size
                if len(pending_features) >= self.batch_size:
                    self._save_features_batch(pending_features)
                    processed += len(pending_features)
                    print(f"\nSaved batch of {len(pending_features)} features. Total processed: {processed}")
                    pending_features = []

        # Process remaining features
        if pending_features:
            self._save_features_batch(pending_features)
            processed += len(pending_features)
            print(f"\nSaved final batch of {len(pending_features)} features. Total processed: {processed}")

        print(f"\nProcessing complete:")
        print(f"- Total images processed: {processed}")
        print(f"- Images skipped (already existed): {skipped}")
        print(f"- Total images handled: {processed + skipped}")

        if processed == 0 and skipped == 0:
            return False, "No images processed"

        return True, f"Successfully processed {processed} new images, skipped {skipped} existing images"

    def _save_features_batch(self, features_batch):
        """Save a batch of features to the database."""
        try:
            features_objects = [
                SongketFeatures(
                    image_name=item['image_name'],
                    features=item['features']
                )
                for item in features_batch
            ]
            db.session.bulk_save_objects(features_objects)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving batch: {str(e)}")
            
    def get_features_from_db(self):
        """Retrieve all features from the database in batches."""
        features_dict = {
            'features': [],
            'filenames': []
        }
        
        total_features = SongketFeatures.query.count()
        if total_features == 0:
            return None
            
        print(f"Retrieving {total_features} features from database in batches of {self.batch_size}")
        
        # Process in batches
        offset = 0
        with tqdm(total=total_features, desc="Loading features", unit="features") as pbar:
            while offset < total_features:
                batch = SongketFeatures.query.limit(self.batch_size).offset(offset).all()
                
                for feature in batch:
                    features_dict['features'].append(np.array(feature.features))
                    features_dict['filenames'].append(feature.image_name)
                
                offset += len(batch)
                pbar.update(len(batch))
        
        print(f"\nLoaded {len(features_dict['filenames'])} features successfully")
        return features_dict

def get_last_processing_time():
    """Get the last processing time from a text file."""
    try:
        with open('model/last_processing.txt') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# Usage example
if __name__ == "__main__":
    # Initialize the model with the uploads folder and batch size
    model = CBIRModel(
        upload_folder='uploads/',
        batch_size=1000  # Set batch size to 1000
    )

    # Process the database to extract and save features
    success, message = model.process_database()
    print(message)

    # Retrieve features from the database
    features = model.get_features_from_db()
    if features:
        print(f"Retrieved {len(features['filenames'])} features from the database.")