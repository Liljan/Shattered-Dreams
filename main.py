import maya.cmds as mc
import sys
path = r'C:\Users\Pelle Serander\Documents\maya\2017\scripts'
sys.path.append(path)  

import voronoi 	 
hasHit = True	


def main():
	myRigidBody = "myActiveRigidBody*"
	contactCount = cmds.getAttr(myRigidBody+".contactCount")
	checkColission(contactCount);



objs = cmds.ls(selection=True)
obj = objs


startTime = cmds.playbackOptions(query = True, minTime=True)
endTime = cmds.playbackOptions(query = True, maxTime=True)

cmds.cutKey(obj, time=(startTime,endTime))

for i in range(int(startTime), int(endTime)):
	cmds.currentTime( i )
	main()

    