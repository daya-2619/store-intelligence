import torch
import torchvision.transforms as T
import torch.nn.functional as F
import cv2
import numpy as np

# Use local OSNet instead of full torchreid package
from ml_pipeline.osnet import osnet_x1_0

device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    extractor = osnet_x1_0(pretrained=True, num_classes=1000)
    extractor.eval()
    extractor.to(device)
    print("Local OSNet Loaded.")
except Exception as e:
    print(f"Error loading OSNet: {e}")
    extractor = None

def get_extractor():
    return extractor

def get_embedding(crop):
    """
    Given an OpenCV image crop (numpy array), returns a normalized 1D numpy array embedding.
    """
    ext = get_extractor()
    if ext is None:
        return None
        
    # Ensure crop is valid
    if crop is None or crop.size == 0 or crop.shape[0] == 0 or crop.shape[1] == 0:
        return None
        
    # Convert crop (BGR) to RGB
    crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    
    # OSNet expects 256x128 input
    crop_resized = cv2.resize(crop_rgb, (128, 256))
    
    # To Tensor and Normalize (ImageNet stats)
    transform = T.Compose([
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    input_tensor = transform(crop_resized).unsqueeze(0).to(device)
    
    with torch.no_grad():
        features = ext(input_tensor)
        
    embedding = features.cpu().numpy()[0]
    
    # Normalize the embedding
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm
        
    return embedding

def match_embedding(query_emb, global_memory_bank, threshold=0.85):
    """
    Compares the query embedding against all embeddings in the global memory bank using Cosine Similarity.
    Returns (matched_global_id, max_similarity) if a match > threshold is found, else (None, 0).
    """
    if query_emb is None or not global_memory_bank:
        return None, 0.0
        
    max_sim = -1.0
    best_id = None
    
    for gid, stored_emb in global_memory_bank.items():
        stored_emb_np = np.array(stored_emb)
        sim = np.dot(query_emb, stored_emb_np)
        if sim > max_sim:
            max_sim = sim
            best_id = gid
            
    if max_sim > threshold:
        return best_id, max_sim
        
    return None, max_sim
