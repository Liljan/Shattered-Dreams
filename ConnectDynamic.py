import maya.cmds as cmds

def addNewRigidBodies(id):

    srb = cmds.ls('myActiveRigidBody'+str(id))
    cmds.delete (srb)
    
    selected = cmds.ls("*_chunks_"+str(id))
    
    array =  cmds.listRelatives(selected)
    for rb in array:
        cmds.select(rb)
        #cmds.select(rb)
        cmds.connectDynamic(rb,f = 'gravityField*')
        
     
        