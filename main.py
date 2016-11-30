import maya.cmds as cmds
import functools
import sys
path = r'C:\Users\Pelle Serander\Documents\maya\2017\scripts'
sys.path.append(path)
import voronoiShattering


def createUI(pWindowTitle, pApplyCallback):

    windowID = "shatterWindowID"

    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(
        windowID, title=pWindowTitle, sizeable=True, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[
                         (1, 90), (2, 60), (3, 60)], columnOffset=[(1, 'right', 3)])

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

    cmds.separator(h=10, style='out')
    cmds.separator(h=10, style='out')
    cmds.separator(h=10, style='out')

    cmds.separator(h=10, style='none')
    cmds.button(label="Apply", command=functools.partial(pApplyCallback,
                                                         startTimeField,
                                                         endTimeField,
                                                         piecesField))

    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

    cmds.button(label="Cancel", command=cancelCallback)

    cmds.showWindow()


def applyCallback(pStartTimeField, pEndTimeField, pPiecesField, *pArgs):
    pieces = cmds.intField(pPiecesField, query=True, value=True)
    startTime = cmds.intField(pStartTimeField, query=True, value=True)
    endTime = cmds.intField(pEndTimeField, query=True, value=True)

    objs = cmds.ls(selection=True)
    obj = objs

    cmds.cutKey(obj, time=(startTime, endTime))
    
    selection = cmds.ls(sl=True, transforms=True)
    addRigid(selection)

    for i in range(int(startTime), int(endTime)):
        cmds.currentTime(i)
        main(pieces, selection)


def main(pPieces, selection):
    myRigidBody = "myActiveRigidBody*"
    contactCount = cmds.getAttr(myRigidBody+".contactCount")
    voronoiShattering.checkColission(contactCount, pPieces, selection)


def addRigid(obj):
    cmds.rigidSolver(create=True, name='rigidSolver')
    cmds.setAttr('rigidSolver.contactData', True)
    cmds.select(obj[0])
    cmds.rigidBody(
        active=True, solver='rigidSolver1', name='myActiveRigidBody')
    cmds.gravity(pos=(0, 0, 0), m=9.8, dx=0, dy=-1, dz=0, name='gravity')
    cmds.connectDynamic('myActiveRigidBody', f='gravity')


# this is run on start
reload(voronoiShattering)


createUI("Shattering Tool", applyCallback)
