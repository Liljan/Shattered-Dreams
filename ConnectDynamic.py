import maya.cmds as cmds

srb = cmds.ls('myActiveRigidBody*')
print str(srb)
cmds.delete (srb)

selected = cmds.ls(sl = True)

for rb in selected:
    cmds.connectDynamic(rb,f = 'gravityField1')
    