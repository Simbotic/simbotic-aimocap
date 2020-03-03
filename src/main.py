from argparse import ArgumentParser
# Main Application
from Components.Static import Capture
from Components.Static.Generate import ModelManager
# import Componets.Static.Generate.ModelManager
if __name__ == '__main__':

    parser = ArgumentParser(description="Motion Capture using AI 3d Pose Estimation")
    parser.add_argument('-m', '--model',
                        help='Required. Path to checkpoint with a trained model ',
                        type=str, required=True)
    parser.add_argument('--video', help='Optional. Path to video file or camera id.', type=str, default='', required=True)
    args = parser.parse_args()
    if args.video == "" :
        raise ValueError("--video has to be provided")

    #TODO Static model path
    manager = ModelManager("3DModel/input/worker03_lumberjack.fbx")

    # Start Frame analysis
    #Capture.load_video(args.video, args.model)
    

