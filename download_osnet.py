import urllib.request
import os

url = "https://raw.githubusercontent.com/KaiyangZhou/deep-person-reid/master/torchreid/models/osnet.py"
dest = "ml_pipeline/osnet.py"

print(f"Downloading {url} to {dest}...")
urllib.request.urlretrieve(url, dest)
print("Done!")

url2 = "https://raw.githubusercontent.com/KaiyangZhou/deep-person-reid/master/torchreid/utils/feature_extractor.py"
dest2 = "ml_pipeline/feature_extractor.py"
# Actually we don't even need feature_extractor, we can just instantiate osnet and load weights!
