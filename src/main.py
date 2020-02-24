import numpy as np 
import cv2
# Pose3D Application
from modules.draw import Plotter3d

from Components.Static import Capture

if __name__ == '__main__':

    Capture.dummy_func()
    canvas_3d = np.zeros((720, 1280, 3), dtype=np.uint8)
    plotter = Plotter3d(canvas_3d.shape[:2])
    canvas_3d_window_name = 'Canvas 3D'
    cv2.namedWindow(canvas_3d_window_name)
    cv2.setMouseCallback(canvas_3d_window_name, Plotter3d.mouse_callback)
    cv2.imshow(canvas_3d_window_name, canvas_3d)