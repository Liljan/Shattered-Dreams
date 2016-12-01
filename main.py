import maya.cmds as cmds
import functools
import voronoiShattering

def createUI(pWindowTitle, pApplyCallback):
    
    windowID = "shatterWindowID"
    
    if cmds.window(windowID, exists = True):
        cmds.deleteUI(windowID)
        
 
    cmds.window(windowID, title = pWindowTitle, sizeable = True, resizeToFitChildren = True)
    cmds.rowColumnLayout(numberOfColumns = 3, columnOffset = [(1,'right',3)])
    
    # add the components

    cmds.text(label = "Frame range:")
    startTimeField = cmds.intField(value = cmds.playbackOptions(q = True, minTime = True))
    endTimeField = cmds.intField(value = cmds.playbackOptions(q = True, maxTime = True))
    
    cmds.separator( h=10, style='out' )
    cmds.separator( h=10, style='out' )
    cmds.separator( h=10, style='out' )
    
    cmds.text(label = "Shatter pieces:")
    piecesField = cmds.intField(minValue = 0, maxValue = 100)
    cmds.separator( h=10, style='none' )
    
    cmds.separator( h=10, style='none' )
    progressionBool = cmds.checkBox( label='Show shatter progression' )
    cmds.separator( h=10, style='none' )
    
    cmds.separator( h=10, style='out' )
    cmds.separator( h=10, style='out' )
    cmds.separator( h=10, style='out' )
    
    cmds.separator( h=10, style='none' )
    cmds.button(label = "Apply", command = functools.partial(pApplyCallback,
                                                            startTimeField,
                                                            endTimeField,
                                                            piecesField, progressionBool)) 
   
    def cancelCallback( *pArgs ):
        if cmds.window( windowID, exists=True ):
            cmds.deleteUI( windowID )  
            
    cmds.button(label = "Cancel" , command = cancelCallback)
    
    cmds.showWindow()
    
def applyCallback(pStartTimeField, pEndTimeField, pPiecesField, pProgressionBool, *pArgs):
    pieces = cmds.intField(pPiecesField, query=True, value = True)
    startTime = cmds.intField(pStartTimeField, query=True, value = True)
    endTime = cmds.intField(pEndTimeField, query=True, value = True)
    
    showProgress = cmds.checkBox(pProgressionBool, query = True, value = True)
    
    objs = cmds.ls(selection=True)
    obj = objs
    
    cmds.cutKey(obj, time=(startTime,endTime))
    selection = cmds.ls(sl=True, transforms=True)
    for i in range(int(startTime), int(endTime)):
	    cmds.currentTime( i )
	    main(pieces, selection, showProgress)

def main(pPieces, selection,pShowProgress):
	myRigidBody = "myActiveRigidBody*"
	contactCount = cmds.getAttr(myRigidBody+".contactCount")
	voronoiShattering.checkColission(contactCount, pPieces, selection,pShowProgress);

# this is run on start
reload(voronoiShattering)
createUI("Shattering Tool", applyCallback)