import maya.cmds as cmds
counter = 0;

def test():
    counter = counter+1
    print str(counter)
    

cmds.expression(n='voronoiShatter', s='python(\"test()\")')
