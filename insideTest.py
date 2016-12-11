import maya.cmds as cmds
import maya.OpenMaya as om 

def test_if_inside_mesh(point, obj):
    dir=(0.0, 0.0, 1.0)
    
    sel = om.MSelectionList()
    dag = om.MDagPath()

    #replace torus with arbitrary shape name
    sel.add(obj)
    sel.getDagPath(0,dag)

    mesh = om.MFnMesh(dag)

    point = om.MFloatPoint(*point)
    dir = om.MFloatVector(*dir)
    farray = om.MFloatPointArray()

    mesh.allIntersections(
            point, dir,
            None, None,
            False, om.MSpace.kWorld,
            10000, False,
            None,
            False,
            farray,
            None, None,
            None, None,
            None
        ) 
<<<<<<< HEAD
    return farray.length()%2 == 1   
=======
    return farray.length()%2 == 1
>>>>>>> bbafde0c2e3dc21e577a31e548847e11e1a11997
