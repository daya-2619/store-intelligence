import numpy as np
import cv2
import os


def generate_heatmap(
    points,
    frame_shape,
    layout_path=None
):

    heatmap = np.zeros(
        frame_shape[:2],
        dtype=np.float32
    )

    for x, y in points:

        cv2.circle(
            heatmap,
            (
                int(x),
                int(y)
            ),
            50,
            1,
            -1
        )

    heatmap = cv2.GaussianBlur(
        heatmap,
        (0, 0),
        25
    )
    
    heatmap_normalized = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    heatmap_colored = cv2.applyColorMap(heatmap_normalized, cv2.COLORMAP_JET)
    
    # Check if store layout exists dynamically
    if layout_path and os.path.exists(layout_path):
        layout = cv2.imread(layout_path)
        layout = cv2.resize(layout, (frame_shape[1], frame_shape[0]))
        overlay = cv2.addWeighted(layout, 0.6, heatmap_colored, 0.4, 0)
        return overlay
    
    return heatmap_colored