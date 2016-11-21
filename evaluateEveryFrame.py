import maya.cmds as cmds

def test():
    print ("hej")
    

cmds.expression(n='voronoiShatter', s='python("test()")')
