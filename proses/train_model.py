from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from datetime import datetime
import os
from PIL import Image
import logging
from models import db, SongketDataset
import json
import h5py

class CBIRModel:
    def __init__(self, upload_folder, features_path='model/features.h5'):
        self.upload_folder = upload_folder
        self.features_path = features_path
        self.img_size = (255, 255)
        self.model = self._build_model()
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger('CBIRModel')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler('cbir.log')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger

    def _build_model(self):
        """Build ResNet50 model for feature extraction"""
        try:
            base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
            return base_model
        except Exception as e:
            self.logger.error(f"Error building model: {str(e)}")
            return None

    def extract_features(self, img_path):
        """Extract features from a single image"""
        try:
            # Load and preprocess image
            img = load_img(img_path, target_size=self.img_size)
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            
            # Extract features
            features = self.model.predict(x)
            return features.flatten()
            
        except Exception as e:
            self.logger.error(f"Error extracting features from {img_path}: {str(e)}")
            return None

    def process_database(self):
        """Process all images in database and save their features"""
        try:
            # Get all dataset entries
            datasets = SongketDataset.query.all()
            
            if not datasets:
                self.logger.error("No datasets found in database")
                return False, "No datasets found"

            # Create directories if they don't exist
            os.makedirs(os.path.dirname(self.features_path), exist_ok=True)

            # Dictionary to store features and metadata
            features_dict = {
                'features': [],
                'filenames': [],
                'fabric_names': [],
                'regions': []
            }

            total_images = len(datasets)
            processed = 0

            for dataset in datasets:
                try:
                    img_path = os.path.join(self.upload_folder, dataset.image_filename)
                    if not os.path.exists(img_path):
                        self.logger.warning(f"Image not found: {img_path}")
                        continue

                    # Extract features
                    features = self.extract_features(img_path)
                    if features is None:
                        continue

                    # Store features and metadata
                    features_dict['features'].append(features)
                    features_dict['filenames'].append(dataset.image_filename)
                    features_dict['fabric_names'].append(dataset.fabric_name)
                    features_dict['regions'].append(dataset.region)

                    processed += 1
                    
                except Exception as e:
                    self.logger.error(f"Error processing {dataset.image_filename}: {str(e)}")
                    continue

            if processed == 0:
                return False, "No images were successfully processed"

            # Convert lists to numpy arrays for efficient storage
            features_array = np.array(features_dict['features'])

            # Save features and metadata to H5 file
            with h5py.File(self.features_path, 'w') as f:
                f.create_dataset('features', data=features_array)
                
                # Save metadata as string datasets
                f.create_dataset('filenames', data=np.array(features_dict['filenames'], dtype='S'))
                f.create_dataset('fabric_names', data=np.array(features_dict['fabric_names'], dtype='S'))
                f.create_dataset('regions', data=np.array(features_dict['regions'], dtype='S'))

            # Save processing timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('model/last_processing.txt', 'w') as f:
                f.write(timestamp)

            return True, f"Successfully processed {processed} out of {total_images} images"

        except Exception as e:
            self.logger.error(f"Error during database processing: {str(e)}")
            return False, f"Processing failed: {str(e)}"

def get_last_processing_time():
    """Get the timestamp of the last successful feature extraction"""
    try:
        with open('model/last_processing.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None