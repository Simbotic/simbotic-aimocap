import numpy as np
import matplotlib.pyplot as plt
import cv2
from modules.input_reader import VideoReader
from modules.inference_engine_pytorch import InferenceEnginePyTorch
from modules.parse_poses import parse_poses
from Components.Static.Map import output_poses3d, output_poses, SKELETON_EDGES

extrinsics = {
    "R": [
        [
            0.1656794936,
            0.0336560618,
            -0.9856051821
        ],
        [
            -0.09224101321,
            0.9955650135,
            0.01849052095
        ],
        [
            0.9818563545,
            0.08784972047,
            0.1680491765
        ]
    ],
    "t": [
         [
             17.76193366
         ],
        [
             126.741365
         ],
        [
             286.3860507
         ]
    ]
}

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

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
        scaled_img = cv2.resize(
            frame, dsize=None, fx=input_scale, fy=input_scale)
        scaled_img = scaled_img[:, 0:scaled_img.shape[1] -
                                (scaled_img.shape[1] % stride)]

        inference_result = net.infer(scaled_img)
        poses_3d, poses_2d = parse_poses(
            inference_result, input_scale, stride, 1, True)
        if len(poses_3d):
            poses_3d = rotate_poses(poses_3d)
            poses_3d_copy = poses_3d.copy()
            x = poses_3d_copy[:, 0::4]
            y = poses_3d_copy[:, 1::4]
            z = poses_3d_copy[:, 2::4]
            poses_3d[:, 0::4], poses_3d[:, 1::4], poses_3d[:, 2::4] = -z, x, -y
            #print("Shape: {}".format(poses_3d.shape))
            poses_3d = poses_3d.reshape(poses_3d.shape[0], 19, -1)[:, :, 0:3]
            #print("Shape: {}".format(poses_3d.shape))
            edges = (SKELETON_EDGES + 19 * np.arange(poses_3d.shape[0]).reshape((-1, 1, 1))).reshape((-1, 2))
            #output_poses3d(poses_3d, counter, edges)
            plot_keypoints(poses_3d)
            
            print("/*/**/**/**/*/*/*/**/**/*/*/*/*")
            counter += 1
            #print(poses_3d)
        break
        #output_poses(poses_2d, counter)
        #counter += 1


def rotate_poses(poses_3d):
    R_inv = np.linalg.inv(extrinsics["R"])
    for pose_id in range(len(poses_3d)):
        pose_3d = poses_3d[pose_id].reshape((-1, 4)).transpose()
        pose_3d[0:3, :] = np.dot(R_inv, pose_3d[0:3, :] - extrinsics["t"])
        poses_3d[pose_id] = pose_3d.transpose().reshape(-1)

    return poses_3d

# Helper Function, will be deleted later.

def plot_keypoints(poses_3d):
    #print(poses_3d[0][0])
    counter = 1
    #array = poses_3d[0]

    #print(len(array))
    #print("X: {}, Y: {}, Z: {}".format(array[0][0],array[0][1],array[0][2]))
    #print("Shape: {}".format(poses_3d.shape))
    for pose in poses_3d[0]:    
        print(counter)
        ax.scatter(pose[0], pose[1], pose[2], marker="^")    
        counter += 1
        
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    plt.show()
