from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_people(frame):

    results = model(
        frame,
        classes=[0],
        conf=0.4,
        verbose=False
    )

    return results[0]