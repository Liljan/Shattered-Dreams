import maya.cmds as cmds
import random
import ConnectDynamic
import insideTest



def checkColission(vel,contactCount, pPieces, selection, pShowProgress, hasShattered,id):    
    
    #object = cmds.ls(sl=True,transforms=True)
    if contactCount >= 1:
        # todo: get number of shards from user input
        #surfaceMaterialLocal = surfaceMaterial(selection, 0.5, 0.5, 1)
        voronoiShatter(selection, pPieces, pShowProgress,id)
        #delete original object
        hasShattered[id] = [True]
        #hasShattered[id] = [[True]]
    if contactCount == 0:   
        vel[id] = cmds.getAttr(selection+'.velocity')


def voronoiShatter(obj, n, pShowProgress,id):
    
    # random point placement for polycut operation


    vPoints = getVoronoiPoints(obj,n) 
          
    # create new group for shards
    cmds.setAttr(obj+'.visibility',0)
    shardGroup = cmds.group( em=True, name = obj + '_chunks_'+str(id) )
    
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
        if tempObj:
            cmds.setAttr(str(tempObj[0]) + '.visibility',1)       
            cmds.parent(tempObj,shardGroup)
            
            for vTo in vPoints:
                if vFrom != vTo:
                    aim = [(v1-v2) for (v1,v2) in zip(vFrom,vTo)]
                    
                    vCenter = [(v1 + v2)/2 for (v1,v2) in zip(vTo,vFrom)]
                    planeAngle = cmds.angleBetween( euler = True, v1=[0,0,1], v2=aim )
                    
                    cmds.polyCut(tempObj[0], df = True, cutPlaneCenter = vCenter, cutPlaneRotate = planeAngle)
                    cmds.polyCloseBorder(tempObj[0], ch = False)
                                    
            cmds.xform(tempObj, cp = True)
        
            
    cmds.xform(shardGroup)
    cmds.undoInfo(state = True)
    cmds.progressWindow(endProgress=1)
    ConnectDynamic.addNewRigidBodies(id)  

def getVoronoiPoints(obj,n):
    bbPos = cmds.exactWorldBoundingBox(obj)
    c = cmds.listRelatives(obj, shapes = True, type='surfaceShape' )
    tempVec = []
    for i in range(n):    
        cutX = random.uniform(bbPos[0] , bbPos[3])
        cutY = random.uniform(bbPos[1] , bbPos[4])
        cutZ = random.uniform(bbPos[2] , bbPos[5])

        while( insideTest.test_if_inside_mesh( (cutX,cutY,cutZ) , c[0] ) == False ):
            cutX = random.uniform(bbPos[0] , bbPos[3])
            cutY = random.uniform(bbPos[1] , bbPos[4])
            cutZ = random.uniform(bbPos[2] , bbPos[5])
        
        tempVec.append( [cutX,cutY,cutZ] )
    return tempVec

reload(ConnectDynamic)