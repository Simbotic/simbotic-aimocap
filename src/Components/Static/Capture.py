import numpy as np 
import cv2
from modules.input_reader import VideoReader
from modules.inference_engine_pytorch import InferenceEnginePyTorch
from modules.parse_poses import parse_poses

def load_video(video_path, model):
    stride = 8
    base_height = 256
    net = InferenceEnginePyTorch(model, "GPU")
    poses_2d = []
    frame_provider = VideoReader(video_path)
    counter = 1
    for frame in frame_provider:
        # current_time = cv2.getTickCount()
        if frame is None:
            break
        input_scale = base_height / frame.shape[0]
        scaled_img = cv2.resize(frame, dsize=None, fx=input_scale, fy=input_scale)
        scaled_img = scaled_img[:, 0:scaled_img.shape[1] - (scaled_img.shape[1] % stride)]  # better to pad, but cut out for demo
        # if fx < 0:  # Focal length is unknown
        #     fx = np.float32(0.8 * frame.shape[1])

        inference_result = net.infer(scaled_img)
        poses_3d, poses_2d = parse_poses(inference_result, input_scale, stride, 1, True)
        print("=======================================================")
        print("Data: {}".format(poses_2d))
        print("=======================================================")
        counter += counter
        print(len(poses_2d))
    
    
        #edges = []
        # if len(poses_3d):
        #     poses_3d = rotate_poses(poses_3d, R, t)
        #     poses_3d_copy = poses_3d.copy()
        #     x = poses_3d_copy[:, 0::4]
        #     y = poses_3d_copy[:, 1::4]
        #     z = poses_3d_copy[:, 2::4]
        #     poses_3d[:, 0::4], poses_3d[:, 1::4], poses_3d[:, 2::4] = -z, x, -y

        #     poses_3d = poses_3d.reshape(poses_3d.shape[0], 19, -1)[:, :, 0:3]
        #     edges = (Plotter3d.SKELETON_EDGES + 19 * np.arange(poses_3d.shape[0]).reshape((-1, 1, 1))).reshape((-1, 2))
        # plotter.plot(canvas_3d, poses_3d, edges)
        # cv2.imshow(canvas_3d_window_name, canvas_3d)

        # draw_poses(frame, poses_2d)
        # current_time = (cv2.getTickCount() - current_time) / cv2.getTickFrequency()
        # if mean_time == 0:
        #     mean_time = current_time
        # else:
        #     mean_time = mean_time * 0.95 + current_time * 0.05
        # cv2.putText(frame, 'FPS: {}'.format(int(1 / mean_time * 10) / 10),
        #             (40, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
        # cv2.imshow('ICV 3D Human Pose Estimation', frame)

        # key = cv2.waitKey(delay)
        # if key == esc_code:
        #     break
        # if key == p_code:
        #     if delay == 1:
        #         delay = 0
        #     else:
        #         delay = 1
        # if delay == 0 or not is_video:  # allow to rotate 3D canvas while on pause
        #     key = 0
        #     while (key != p_code
        #            and key != esc_code
        #            and key != space_code):
        #         plotter.plot(canvas_3d, poses_3d, edges)
        #         cv2.imshow(canvas_3d_window_name, canvas_3d)
        #         key = cv2.waitKey(33)
        #     if key == esc_code:
        #         break
        #     else:
        #         delay = 1