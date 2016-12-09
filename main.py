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
    vel = [[0,0,0]]
    hasShattered = [False]
    hasAdded = True;
    for i in range(int(startTime), int(endTime)):
        cmds.currentTime(i)

        if hasShattered[0] == False:
            checkContact(pieces, selection, showProgress, hasShattered,vel)
        if hasShattered[0] == True and hasAdded == True:
            objects = cmds.ls("*_chunks_*")
            array =  cmds.listRelatives(objects)
            velTemp = [0,0,0]
            for rb in array:
                cmds.select(rb)
                #cmds.select(rb)
                velTemp = vel[0];
                print rb
                cmds.setAttr(rb+'.velocityX', velTemp[0][0] )
                cmds.setAttr(rb+'.velocityY', velTemp[0][1] )
                cmds.setAttr(rb+'.velocityZ', velTemp[0][2])
                #cmds.setAttr(rb+'.forceX', 10 )
                #cmds.setAttr(rb+'.forceY',  )
                #cmds.setAttr(rb+'.forceZ', 10)
                cmds.setAttr(rb+'.impulseX', 0.01 )
                #cmds.setAttr(rb+'.impulseY', 0 )
                #cmds.setAttr(rb+'.impulseZ', 1)
                cmds.setAttr(rb+'.impulsePositionX', 0)
                cmds.setAttr(rb+'.impulsePositionY', 0 )
                cmds.setAttr(rb+'.impulsePositionZ', 0)
            hasAdded = False
            print 'hasrun'

def checkContact(pPieces, selection, pShowProgress, hasShattered,vel):
    myRigidBody = "myActiveRigidBody*"
    contactCount = cmds.getAttr(myRigidBody+".contactCount")
    voronoiShattering.checkColission(vel,contactCount, pPieces, selection,pShowProgress, hasShattered)
    print str(vel[0])

# this is run on start
reload(voronoiShattering)
createUI("Shattering Tool", applyCallback)
