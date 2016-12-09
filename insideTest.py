import maya.cmds as cmd
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
    return farray.length()%2 == 1   

#test
#cmd.polyTorus()

obj = cmds.ls(sl = True)
c = cmds.listRelatives(obj, shapes = True, type='surfaceShape' )
print c[0]

p = (0,0,0)

print test_if_inside_mesh(p,c[0])