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
    
    cmds.text(label="velocity slider [0,2]")
    velSlider = cmds.floatSlider( min=0, max=2, value=0.5, step=0.01 )
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
                                                            piecesField, 
                                                            progressionBool,
                                                            velSlider))

    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

    cmds.button(label="Cancel", command=cancelCallback)

    cmds.showWindow()


def applyCallback(pStartTimeField, pEndTimeField, pPiecesField, pProgressionBool, pVelSlider, *pArgs):
    pieces = cmds.intField(pPiecesField, query=True, value=True)
    startTime = cmds.intField(pStartTimeField, query=True, value=True)
    endTime = cmds.intField(pEndTimeField, query=True, value=True)
    sliderValue = cmds.floatSlider(pVelSlider, query=True, value=True)
    print sliderValue

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
        for sl in selection:
            count = 0

            id = getId(sl,count,realLength)
            if( id != -1): 
                if hasShattered[id] == [False]:
                    checkContact(pieces, sl, showProgress, hasShattered,vel,id)
                
                if hasShattered[id] == [True] and hasAdded[id] == True:
                        objects = cmds.ls(sl+"_chunks_"+str(id))
                        array =  cmds.listRelatives(objects)
                        for rb in array:
                            cmds.select(rb)
                            cmds.setAttr(rb+'.initialVelocityX', sliderValue*vel[id][0][0] )
                            cmds.setAttr(rb+'.initialVelocityY', sliderValue*vel[id][0][1] )
                            cmds.setAttr(rb+'.initialVelocityZ', sliderValue*vel[id][0][2] )
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
            count = count+1
               
def checkContact(pPieces, selection, pShowProgress, hasShattered,vel,id):

    myRigidBody = "myActiveRigidBody"+str(id)
    contactCount = cmds.getAttr(myRigidBody+".contactCount")
    #print str(id)+' in checkcontackt '+ str(contactCount)
    voronoiShattering.checkColission(vel,contactCount, pPieces, selection,pShowProgress, hasShattered,id)
   

def getId(sl,count,length):
    thisObjShapes = cmds.listRelatives(sl)
    thisRigidBodyName = 'myActiveRigidBody'
    temp = ''
    for shapes in thisObjShapes:
        if str(thisRigidBodyName) in str(shapes):
            temp = str(shapes)
    
        
    if length < 11:
        length = 1
    elif length < 101:
        length = 2
    elif length < 1001:
        length = 3
    if temp is not '':
        id = temp[-length:]

        while is_number(str(id)) == False:
            length = length-1 
            id = str[-length:]

        return int(id)
    else:
        return -1;

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# this is run on start
reload(voronoiShattering)
createUI("Shattering Tool", applyCallback)
