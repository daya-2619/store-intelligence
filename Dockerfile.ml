FROM python:3.11-slim

WORKDIR /app

# Install CV2 and DB dependencies
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir ultralytics supervision opencv-python-headless pika python-json-logger

COPY . .

CMD ["python", "ml_pipeline/run_all_cameras.py"]
