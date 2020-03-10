import numpy as np
import json, math

body_edges = np.array(
    [[0, 1],  # neck - nose
     [1, 16], [16, 18],  # nose - l_eye - l_ear
     [1, 15], [15, 17],  # nose - r_eye - r_ear
     [0, 3], [3, 4], [4, 5],     # neck - l_shoulder - l_elbow - l_wrist
     [0, 9], [9, 10], [10, 11],  # neck - r_shoulder - r_elbow - r_wrist
     [0, 6], [6, 7], [7, 8],        # neck - l_hip - l_knee - l_ankle
     [0, 12], [12, 13], [13, 14]])  # neck - r_hip - r_knee - r_ankle

name_body_parts = dict([(0, "neck_01"), (1, "head"), (16, "Left Eye"), (18, "Left Ear"), (15, "Right Eye"), (17, "Right Ear"),
                        (3, "upperarm_l"), (4, "lowerarm_l"), (5,
                                                               "hand_l"), (9, "upperarm_r"), (10, "lowerarm_r"),
                        (11, "hand_r"), (6, "thigh_l"), (7, "calf_l"), (8,
                                                                        "foot_l"), (12, "thigh_r"), (13, "calf_r"),
                        (14, "foot_r")])
mapped_skeletal = dict()

SKELETON_EDGES = np.array([[11, 10], [10, 9], [9, 0], [0, 3], [3, 4], [4, 5], [0, 6], [6, 7], [7, 8], [0, 12],
                           [12, 13], [13, 14], [0, 1], [1, 15], [15, 16], [1, 17], [17, 18]])


def set_rotation(theta=3.1415/4, phi=-3.1415/6):
    sin, cos = math.sin, math.cos
    return np.array([
        [cos(theta),  sin(theta) * sin(phi)],
        [-sin(theta),  cos(theta) * sin(phi)],
        [0,                       -cos(phi)]
    ], dtype=np.float32)  # transposed


def output_poses(poses_2d, frame_number):
    for pose_id in range(len(poses_2d)):
        pose = np.array(poses_2d[pose_id][0:-1]).reshape((-1, 3)).transpose()
        was_found = pose[2, :] > 0
        for edge in body_edges:
            if was_found[edge[0]] and was_found[edge[1]]:

                mapped_skeletal[name_body_parts[edge[0]]] = {
                    "x": int(pose[0:2, edge[0]][0]), "y": int(pose[0:2, edge[0]][1])}
                mapped_skeletal[name_body_parts[edge[1]]] = {
                    "x": int(pose[0:2, edge[1]][0]), "y": int(pose[0:2, edge[1]][1])}

    save_results(frame_number)
    print(mapped_skeletal)


def output_poses3d(poses_3d, frame_number, edges):
    R = set_rotation()
    canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
    canvas_size = canvas.shape[:2]
    origin = np.array([0.5 * canvas_size[1], 0.5 * canvas_size[0]], dtype=np.float32)
    if len(edges) != 0:
        vertices_2d = np.dot(poses_3d, R)
        edges_vertices = vertices_2d.reshape((-1, 2))[edges] * np.float32(1) + origin
        for edge_vertices in edges_vertices:
            edge_vertices = edge_vertices.astype(int)
            #cv2.line(img, tuple(edge_vertices[0]), tuple(edge_vertices[1]), (255, 255, 255), 1, cv2.LINE_AA)
            print("edge_vertices: {},{}".format(edge_vertices[0], edge_vertices[1]))

def save_results(frame_number):

    filename = "models/data/frame_{}.json".format(frame_number)
    with open(filename, 'w') as output_file:
        json.dump(mapped_skeletal, output_file, indent=4, sort_keys=True)
