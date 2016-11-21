
import maya.cmds as cmds
import random
def checkColission():
    object = cmds.ls(sl=True)
    cmds.setKeyframe(object)
    
    nodes = cmds.keyframe(object,query=True,name=True)
    
    for node in nodes:
        
        myRigidBody = "myActiveRigidBody*";
        
        contactCount = cmds.getAttr(myRigidBody+".contactCount")
            
        if contactCount == 1: 
            voroShatter(object, 50)
      
        
def voroShatter(object, num):
    # Evaluate the bounding box points [minX, minY, minZ, maxX, maxY, maxZ]
    bbPoints = cmds.exactWorldBoundingBox(object) 
    print bbPoints
    
    # Place the random points for polycut, based on the bounding box
    numPoints = num
    voroX = [random.uniform(bbPoints[0], bbPoints[3]) for i in range(numPoints)]
    voroY = [random.uniform(bbPoints[1], bbPoints[4]) for i in range(numPoints)]
    voroZ = [random.uniform(bbPoints[2], bbPoints[5]) for i in range(numPoints)]
    voroPoints = zip(voroX, voroY, voroZ)
    
    cmds.setAttr(object+'.visibility',0)
    chunksGrp = cmds.group( em=True, name = object + '_chunks_1' )
 
    for voroFrom in voroPoints:
        # Duplicate the object to cut as shatters
        workingObj = cmds.duplicate(object)
        cmds.setAttr(str(workingObj[0])+'.visibility',1)
        cmds.parent(workingObj, chunksGrp)
         
        for voroTo in voroPoints:
            if voroFrom != voroTo:
                # Calculate the Perpendicular Bisector Plane
                aim = [(vec1-vec2) for (vec1,vec2) in zip(voroFrom,voroTo)]
                voroCenter = [(vec1 + vec2)/2 for (vec1,vec2) in zip(voroTo,voroFrom)]
                planeAngle = cmds.angleBetween( euler=True, v1=[0,0,1], v2=aim )
                # Bullet Shatter
                cmds.polyCut(workingObj[0], df=True, cutPlaneCenter = voroCenter, cutPlaneRotate = planeAngle)
                cmds.polyCloseBorder(workingObj[0])
         
        cmds.xform(workingObj, cp=True)
        print str(workingObj)
         
    cmds.xform(chunksGrp, cp=True)
         



    
    
    
    
    
    