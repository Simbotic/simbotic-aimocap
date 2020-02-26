import numpy as np
import json

body_edges = np.array(
    [[0, 1],  # neck - nose
     [1, 16], [16, 18],  # nose - l_eye - l_ear
     [1, 15], [15, 17],  # nose - r_eye - r_ear
     [0, 3], [3, 4], [4, 5],     # neck - l_shoulder - l_elbow - l_wrist
     [0, 9], [9, 10], [10, 11],  # neck - r_shoulder - r_elbow - r_wrist
     [0, 6], [6, 7], [7, 8],        # neck - l_hip - l_knee - l_ankle
     [0, 12], [12, 13], [13, 14]])  # neck - r_hip - r_knee - r_ankle

name_body_parts = dict([(0, "Neck"), (1, "Nose"), (16, "Left Eye"), (18, "Left Ear"), (15, "Right Eye"), (17, "Right Ear"),
                        (3, "Left Shoulder"), (4, "Left Elbow"), (5, "Left Wrist"), (9, "Right Shoulder"), (10, "Right Elbow"), 
                        (11, "Right Wrist"), (6, "Left Hip"), (7, "Left Knee"), (8, "Left Ankle"), (12, "Right Hip"), (13, "Right Knee"), 
                        (14, "Right Ankle")])
mapped_skeletal = dict()

def output_poses(poses_2d, frame_number):
    for pose_id in range(len(poses_2d)):
        pose = np.array(poses_2d[pose_id][0:-1]).reshape((-1, 3)).transpose()
        was_found = pose[2, :] > 0
        for edge in body_edges:
            if was_found[edge[0]] and was_found[edge[1]]:
                
                mapped_skeletal[name_body_parts[edge[0]]] = { "x": int(pose[0:2, edge[0]][0]), "y": int(pose[0:2, edge[0]][1])}
                mapped_skeletal[name_body_parts[edge[1]]] = { "x": int(pose[0:2, edge[1]][0]), "y": int(pose[0:2, edge[1]][1])}
    
    save_results(frame_number)
    print(mapped_skeletal)


def save_results(frame_number):

    filename = "models/data/frame_{}.json".format(frame_number)
    with open(filename, 'w') as output_file:
        json.dump(mapped_skeletal, output_file, indent=4, sort_keys=True)
