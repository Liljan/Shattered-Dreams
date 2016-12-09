import maya.cmds as cmds
import functools
import voronoiShattering
import ConnectDynamic

def createUI(pWindowTitle, pApplyCallback):

    windowID = "shatterWindowID"

    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(
        windowID, title=pWindowTitle, sizeable=True, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnOffset=[(1, 'right', 3)])

    # add the components

    cmds.text(label="Frame range:")
    startTimeField = cmds.intField(
        value=cmds.playbackOptions(q=True, minTime=True))
    endTimeField = cmds.intField(
        value=cmds.playbackOptions(q=True, maxTime=True))

    cmds.separator(h=10, style='out')
    cmds.separator(h=10, style='out')
    cmds.separator(h=10, style='out')

    cmds.text(label="Shatter pieces:")
    piecesField = cmds.intField(minValue=0, maxValue=100)
    cmds.separator(h=10, style='none')

    cmds.separator(h=10, style='none')
    progressionBool = cmds.checkBox(
        label='Show shatter progression', value=True)
    cmds.separator(h=10, style='none')

    cmds.separator(h=10, style='out')
    cmds.separator(h=10, style='out')
    cmds.separator(h=10, style='out')

    cmds.separator(h=10, style='none')
    cmds.button(label="Apply", command=functools.partial(pApplyCallback,
                                                            startTimeField,
                                                            endTimeField,
                                                            piecesField, progressionBool))

    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

    cmds.button(label="Cancel", command=cancelCallback)

    cmds.showWindow()


def applyCallback(pStartTimeField, pEndTimeField, pPiecesField, pProgressionBool, *pArgs):
    pieces = cmds.intField(pPiecesField, query=True, value=True)
    startTime = cmds.intField(pStartTimeField, query=True, value=True)
    endTime = cmds.intField(pEndTimeField, query=True, value=True)

    showProgress = cmds.checkBox(pProgressionBool, query=True, value=True)

    objs = cmds.ls(selection=True)
    obj = objs


    cmds.cutKey(obj, time=(startTime, endTime))
    selection = cmds.ls(sl=True, transforms=True)
    realLength = len(selection)

    vel = [[0,0,0] for x in range(0,len(selection))]
    hasShattered = [[False] for x in range(0,len(selection))]
    hasAdded = [True for x in range(0,len(selection))]

    for i in range(int(startTime), int(endTime)):

        cmds.currentTime(i)
        id = 0
        for sl in selection: 
            if hasShattered[id] == [False]:
                checkContact(pieces, sl, showProgress, hasShattered,vel,id)
            
            if hasShattered[id] == [True] and hasAdded[id] == True:
                    objects = cmds.ls(sl+"_chunks_"+str(id))
                    array =  cmds.listRelatives(objects)
                    print array
                    for rb in array:
                        cmds.select(rb)
                        cmds.setAttr(rb+'.initialVelocityX', vel[id][0][0] )
                        cmds.setAttr(rb+'.initialVelocityY', vel[id][0][1] )
                        cmds.setAttr(rb+'.initialVelocityZ', vel[id][0][2] )
                        #cmds.setAttr(rb+'.forceX', 10 )
                        #cmds.setAttr(rb+'.forceY',  )
                        #cmds.setAttr(rb+'.forceZ', 10)
                        #cmds.setAttr(rb+'.impulseX', 0.1 )
                        #cmds.setAttr(rb+'.impulseY', 0 )
                        #cmds.setAttr(rb+'.impulseZ', 1)
                        cmds.setAttr(rb+'.impulsePositionX', 0)
                        cmds.setAttr(rb+'.impulsePositionY', 0 )
                        cmds.setAttr(rb+'.impulsePositionZ', 0)
                    hasAdded[id] = False
            
            id = id+1
               
def checkContact(pPieces, selection, pShowProgress, hasShattered,vel,id):

    myRigidBody = "myActiveRigidBody"+str(id)
    contactCount = cmds.getAttr(myRigidBody+".contactCount")
    #print str(id)+' in checkcontackt '+ str(contactCount)
    voronoiShattering.checkColission(vel,contactCount, pPieces, selection,pShowProgress, hasShattered,id)
   



# this is run on start
reload(voronoiShattering)
createUI("Shattering Tool", applyCallback)
