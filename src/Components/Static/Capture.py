import numpy as np 
import cv2
from modules.input_reader import VideoReader
from modules.inference_engine_pytorch import InferenceEnginePyTorch
from modules.parse_poses import parse_poses
from Components.Static.Map import output_poses

def load_video(video_path, model):
    stride = 8
    base_height = 256
    net = InferenceEnginePyTorch(model, "GPU")
    poses_2d = []
    frame_provider = VideoReader(video_path)
    counter = 1
    for frame in frame_provider:
        
        if frame is None:
            break
        input_scale = base_height / frame.shape[0]
        scaled_img = cv2.resize(frame, dsize=None, fx=input_scale, fy=input_scale)
        scaled_img = scaled_img[:, 0:scaled_img.shape[1] - (scaled_img.shape[1] % stride)]

        inference_result = net.infer(scaled_img)
        poses_3d, poses_2d = parse_poses(inference_result, input_scale, stride, 1, True)
        print("/*/**/**/**/*/*/*/**/**/*/*/*/*")
        output_poses(poses_2d, counter)
        counter += 1 

