import cv2
import numpy as np
from ml_pipeline.reid import get_embedding, match_embedding

# Dummy crop
crop1 = np.random.randint(0, 255, (100, 50, 3), dtype=np.uint8)
crop2 = np.random.randint(0, 255, (100, 50, 3), dtype=np.uint8)

emb1 = get_embedding(crop1)
emb2 = get_embedding(crop2)

memory = {"GLOBAL_001": emb1}

match, score = match_embedding(emb2, memory, threshold=0.5)

print("Match:", match, "Score:", score)
print("SUCCESS!")
