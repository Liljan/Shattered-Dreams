import maya.cmds as cmds

def addNewRigidBodies():
    srb = cmds.ls('myActiveRigidBody*')
    cmds.delete (srb)
    
    selected = cmds.ls("*_chunks_*")
    
    array =  cmds.listRelatives(selected)
    print selected
    print array
    
    for rb in array:
        print "Lasse"
        cmds.select(rb)
        cmds.connectDynamic(rb,f = 'gravityField*')