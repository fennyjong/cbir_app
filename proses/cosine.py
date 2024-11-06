import os
import numpy as np
from keras.applications.resnet import ResNet50, preprocess_input
from keras.preprocessing.image import load_img, img_to_array
from models import SongketFeatures, SongketDataset
from flask import url_for

# Modified CBIRModel class
class CBIRModel:
    def __init__(self, upload_folder, batch_size=1000, min_similarity=0.5):
        self.upload_folder = upload_folder
        self.batch_size = batch_size
        self.img_size = (255, 255)
        self.min_similarity = min_similarity  # Add minimum similarity threshold
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
        """Find similar images based on feature similarity and return detailed results."""
        if not isinstance(n_results, int) or n_results <= 0:
            n_results = 10  # Fallback to default if invalid input
            
        db_features = []
        image_names = []
        
        # Process dataset in batches to manage memory efficiently
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
        
        # Get indices where similarity is above threshold
        valid_indices = np.where(similarities >= self.min_similarity)[0]
        
        if len(valid_indices) == 0:
            return []  # Return empty list if no images meet the threshold
        
        # Sort valid indices by similarity
        top_indices = valid_indices[np.argsort(similarities[valid_indices])[-n_results:][::-1]]
        
        results = []
        for idx in top_indices:
            image_name = image_names[idx]
            
            # Query additional information from SongketDataset table
            songket_data = SongketDataset.query.filter_by(image_filename=image_name).first()
            if songket_data:
                fabric_name = songket_data.fabric_name
                region = songket_data.region
            else:
                fabric_name = "Unknown"
                region = "Unknown"
            
            # Generate the URL for the image
            image_url = url_for('user.serve_upload', filename=image_name, _external=True)
            
            results.append({
                'image': image_url,
                'fabric_name': fabric_name,
                'region': region,
                'similarity': float(similarities[idx])
            })
        
        return results[:n_results]