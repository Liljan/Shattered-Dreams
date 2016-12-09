import maya.cmds as cmds

def addNewRigidBodies():
    srb = cmds.ls('myActiveRigidBody*')
    cmds.delete (srb)
    
    selected = cmds.ls("*_chunks_*")
    
    array =  cmds.listRelatives(selected)

    for rb in array:
        cmds.select(rb)
        
     	
        #cmds.select(rb)
        cmds.connectDynamic(rb,f = 'gravityField*')
        
     
        