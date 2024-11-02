import os
import numpy as np
from keras.applications.resnet import ResNet50, preprocess_input
from keras.preprocessing.image import load_img, img_to_array
from models import SongketFeatures
from flask import url_for

class CBIRModel:
    def __init__(self, upload_folder, batch_size=1000):
        self.upload_folder = upload_folder
        self.batch_size = batch_size
        self.img_size = (255, 255)
        self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

    def extract_features(self, img_path):
        """Extract features from the given image path."""
        try:
            img = load_img(img_path, target_size=self.img_size)
            x = preprocess_input(img_to_array(img)[None, ...])
            return self.model.predict(x, verbose=0).flatten()
        except Exception as e:
            print(f"Error extracting features from {img_path}: {str(e)}")
            return None

    def find_similar_images(self, query_features, n_results=10):
        """Find similar images based on feature similarity."""
        if not isinstance(n_results, int) or n_results <= 0:
            n_results = 10  # Fallback to default if invalid input
            
        db_features = []
        image_names = []

        # Process in batches
        offset = 0
        while True:
            batch = SongketFeatures.query.limit(self.batch_size).offset(offset).all()
            if not batch:
                break

            for feature in batch:
                db_features.append(np.array(feature.features))
                image_names.append(feature.image_name)

            offset += len(batch)

        if not db_features:
            return []

        # Convert to numpy array for efficient computation
        db_features = np.array(db_features)

        # Calculate cosine similarity
        query_norm = np.linalg.norm(query_features)
        db_norm = np.linalg.norm(db_features, axis=1)
        similarities = np.dot(db_features, query_features) / (db_norm * query_norm)

        # Get top N similar images
        top_indices = np.argsort(similarities)[-n_results:][::-1]  # Remove the ::-2 step

        results = []
        for idx in top_indices:
            # Use serve_upload endpoint for database images
            image_url = url_for('user.serve_upload', 
                              filename=image_names[idx], 
                              _external=True)
            
            results.append({
                'image': image_url,
                'similarity': float(similarities[idx])
            })

        return results[:n_results]  # Ensure we return exactly n_results items

def get_last_processing_time():
    """Get the last processing time from a text file."""
    try:
        with open('model/last_processing.txt') as f:  # Fixed file path
            return f.read().strip()
    except FileNotFoundError:
        print("Last processing time file not found.")
        return None

# Usage example
if __name__ == "__main__":
    model = CBIRModel(upload_folder='uploads/', batch_size=1000)
    success, message = model.process_database()
    print(message)
