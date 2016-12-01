import maya.cmds as cmds
import random

def checkColission(contactCount, pPieces, selection, pShowProgress):    
    
    object = cmds.ls(sl=True,transforms=True)
    if contactCount > 0:

        for s in selection:
            # todo: get number of shards from user input
            surfaceMaterialLocal = surfaceMaterial(s, 0.5, 0.5, 1)
            voronoiShatter(s, surfaceMaterialLocal, pPieces, pShowProgress)
        #delete original object
        #cmds.delete()

def surfaceMaterial(obj, R, G, B):
    name = (obj + '_shardMaterial')
    if ( cmds.objExists(name) == 0 ):
        cmds.shadingNode( 'lambert', asShader = True, name = name )
        cmds.sets( renderable = True, noSurfaceShader = True, empty = True, name = (name + 'SG'))
        cmds.connectAttr( (name + '.outColor'), (name + 'SG.surfaceShader'), force = True)
        cmds.setAttr((name + '.color'), R, G, B, type = "double3") 
    return name

def voronoiShatter(obj, surfaceMaterialLocal, n, pShowProgress):
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
    
    step = 0
    
    if pShowProgress:
        cmds.progressWindow(title = "Voronoi Calculating", progress = 0, isInterruptable = True, maxValue = n)
     
    cmds.undoInfo(state = False)
    
    for vFrom in vPoints:
        
        if pShowProgress:
            if cmds.progressWindow(q = True, isCancelled=True): break
            if cmds.progressWindow(q = True, progress = True) >= n: break
            step = step + 1
            
            cmds.progressWindow(edit=True, progress = step, status=("Shattering step %d of %d completed..." % (step, n)))
            
        cmds.refresh()
        
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
				#do not apply our shitty surface material to keep the original material.
                #cmds.sets(cutFaces, forceElement = (surfaceMaterialLocal + 'SG'), e=True)
                                
        cmds.xform(tempObj, cp = True)
    
    cmds.xform(shardGroup)
    cmds.undoInfo(state = True)
    cmds.progressWindow(endProgress=1)