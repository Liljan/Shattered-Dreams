import maya.cmds as cmds
import random

def surfaceMaterial(obj, R, G, B):
    name = (obj + '_shardMaterial')
    if ( cmds.objExists(name) == 0 ):
        cmds.shadingNode( 'lambert', asShader = True, name = name )
        cmds.sets( renderable = True, noSurfaceShader = True, empty = True, name = (name + 'SG'))
        cmds.connectAttr( (name + '.outColor'), (name + 'SG.surfaceShader'), force = True)
        cmds.setAttr((name + '.color'), R, G, B, type = "double3") 
    return name

def voronoiShatter(obj, n):
    bbPos = cmds.exactWorldBoundingBox(obj)
    
    # random point placement for polycut operation
    cutX = [random.uniform(bbPos[0] , bbPos[3]) for i in range(n)]
    cutY = [random.uniform(bbPos[1] , bbPos[4]) for i in range(n)]
    cutZ = [random.uniform(bbPos[2] , bbPos[5]) for i in range(n)]
    vPoints = zip(cutX,cutY,cutZ)  
          
    # create new group for shards
    cmds.setAttr(obj+'.visibility',0)
    shardGroup = cmds.group( em=True, name = obj + '_chunks_1' )
    
    cmds.undoInfo(state = False)
    cmds.setAttr(str(obj) + '.visibility',0)
    
    for vFrom in vPoints:
        
        #cmds.refresh()
         
        tempObj = cmds.duplicate(obj)
        cmds.setAttr(str(tempObj[0]) + '.visibility',1)       
        cmds.parent(tempObj,shardGroup)
        
        for vTo in vPoints:
            if vFrom != vTo:
                aim = [(v1-v2) for (v1,v2) in zip(vFrom,vTo)]
                vCenter = [(v1 + v2)/2 for (v1,v2) in zip(vTo,vFrom)]
                planeAngle = cmds.angleBetween( euler = True, v1=[0,0,1], v2=aim )
                                
                cmds.polyCut(tempObj[0], df = True, cutPlaneCenter = vCenter, cutPlaneRotate = planeAngle)
                
                originalFaces = cmds.polyEvaluate(tempObj[0], face = True)
                cmds.polyCloseBorder(tempObj[0], ch = False)
                afterFaces = cmds.polyEvaluate(tempObj[0], face = True)
                newFaces = afterFaces - originalFaces;
                
                cutFaces = ('%s.f[ %d ]' % (tempObj[0], (afterFaces + newFaces - 1)))
                cmds.sets(cutFaces, forceElement = (surfaceMaterial + 'SG'), e=True)
                                
        cmds.xform(tempObj, cp = True)
    
    cmds.xform(shardGroup)
    cmds.undoInfo(state = True)
        
    # this part is run when the function is run

#cmds.scriptEditorInfo(ch=True)
selection = cmds.ls(sl=True, transforms=True)

for s in selection:
    # todo: get number of shards from user input
    surfaceMaterial = surfaceMaterial(sel, 0.5, 0.5, 1)
    voronoiShatter(s, 5)