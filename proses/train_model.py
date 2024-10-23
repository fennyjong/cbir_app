from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import h5py
from datetime import datetime
from models import SongketDataset

class CBIRModel:
    def __init__(self, upload_folder, features_path='model/features.h5'):
        self.upload_folder = upload_folder
        self.features_path = features_path
        self.img_size = (255, 255)
        self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        
    def extract_features(self, img_path):
        img = load_img(img_path, target_size=self.img_size)
        x = preprocess_input(img_to_array(img)[None, ...])
        return self.model.predict(x).flatten()

    def process_database(self):
        datasets = SongketDataset.query.all()
        if not datasets:
            return False, "No datasets found"

        os.makedirs(os.path.dirname(self.features_path), exist_ok=True)
        features_dict = {'features': [], 'filenames': [], 'fabric_names': [], 'regions': []}
        processed = 0

        for dataset in datasets:
            img_path = os.path.join(self.upload_folder, dataset.image_filename)
            if not os.path.exists(img_path):
                print(f"Image not found: {img_path}")
                continue
            
            features = self.extract_features(img_path)
            if features is not None:
                features_dict['features'].append(features)
                features_dict['filenames'].append(dataset.image_filename)
                features_dict['fabric_names'].append(dataset.fabric_name)
                features_dict['regions'].append(dataset.region)
                processed += 1

        if processed == 0:
            return False, "No images processed"

        features_array = np.array(features_dict['features'])
        with h5py.File(self.features_path, 'w') as f:
            f.create_dataset('features', data=features_array)
            f.create_dataset('filenames', data=np.array(features_dict['filenames'], dtype='S'))
            f.create_dataset('fabric_names', data=np.array(features_dict['fabric_names'], dtype='S'))
            f.create_dataset('regions', data=np.array(features_dict['regions'], dtype='S'))

        with open('model/last_processing.txt', 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return True, f"Successfully processed {processed} images"

def get_last_processing_time():
    try:
        with open('model/last_processing.txt') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
