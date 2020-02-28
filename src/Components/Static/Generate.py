import pyassimp
from pyassimp.postprocess import *

class ModelManager():

    def __init__(self, model_path):

        self.height = 1080
        self.width = 1920

        # Load model
        print("Loading model: {} ...".format(model_path))
        # Store in a property
        self.scene = pyassimp.load(model_path)
        
        #print(self.scene)
        # print("Meshes: %d" % len(self.scene.meshes))
        # print("Total faces: %d" % sum([len(mesh.faces) for mesh in self.scene.meshes]))
        # print("Materials: %d" % len(self.scene.materials))
        # print("Root node: " + str(self.scene.rootnode))

if __name__ == '__main__':
   manager = ModelManager("SK_Mannequin.FBX")