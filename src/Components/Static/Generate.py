import pyassimp
from pyassimp.postprocess import *
import numpy
class ModelManager():

    def __init__(self, model_path):

        self.height = 1080
        self.width = 1920

        # Load model
        print("Loading model: {} ...".format(model_path))
        # Store in a property
        self.scene = pyassimp.load(model_path)
        
        #print(self.scene)
        print("Meshes: %d" % len(self.scene.meshes))
        print("Total faces: %d" % sum([len(mesh.faces) for mesh in self.scene.meshes]))
        print("Materials: %d" % len(self.scene.materials))
        print("Root node: " + str(self.scene.rootnode))
        print("/*/*/*/*/*/*/*/*")
        anim = self.scene.animations[0]
        print("Number of animations: {}, duration: {}, name: {}, Ticks per second: {}".format(len(self.scene.animations),
                anim.duration, anim.name, anim.tickspersecond))
        print("/*/*/*/*/*/*/*/*")
        #print(dir(self.scene.animations[0].channels[1]))
        self.print_animations(self.scene.animations[0].channels)
        #self.print_nodes(self.scene.rootnode)
        #print(len(self.scene.animations))

        #self.print_animations(self.scene.animations)
        

    def print_nodes(self, node):
        
        if node:
            print("Node: {}, Transform: {}".format(node.name, node.transformation.astype(numpy.float32)))
        else:
            return
        
        for child in node.children:
            self.print_nodes(child)

    def print_animations(self, animations):
        for anim in animations:
            print(anim.nodename.data)
