# Generated with SMOP  0.41
from smop.libsmop import *
from checkJointAngleBounds import checkJointAngleBounds
from compareFKtoIK import compareFKtoIK
from IK import IK
# testscript.m
if __name__ == '__main__':
    format('short')
    L1=0.31685
# testscript.m:3
    L2=0.25
# testscript.m:4
    L3=0.15352
# testscript.m:5
    # tolerance to compare return values of FK and IK to the thousandth of a degree of rotation
    tolerance=0.001
# testscript.m:8
    #input list for testing FK and IK, the results for both functions should be
#the same
    thetalist=[0,0,90]
# testscript.m:12
    
    thetalist=concat([thetalist,[90,0,0]])
# testscript.m:13
    
    thetalist=concat([thetalist,[0,45,45]])
# testscript.m:14
    
    thetalist=concat([thetalist,[0,135,- 45]])
# testscript.m:15
    
    thetalist=concat([thetalist,[0,180,- 90]])
# testscript.m:16
    
    thetalist=concat([thetalist,[90,- 90,90]])
# testscript.m:17
    
    thetalist=concat([thetalist,[90,- 45,45]])
# testscript.m:18
    
    thetalist=concat([thetalist,[- 45,45,90]])
# testscript.m:19
    
    thetalist=concat([thetalist,[- 45,90,45]])
# testscript.m:20
    
    thetalist=concat([thetalist,[- 45,135,0]])
# testscript.m:21
    
    thetalist=concat([thetalist,[- 90,90,90]])
# testscript.m:22
    
    thetalist=concat([thetalist,[45,45,0]])
# testscript.m:23
    
    thetalist=concat([thetalist,[- 90,135,45]])
# testscript.m:24
    
    thetalist=concat([thetalist,[- 90,180,0]])
# testscript.m:25
    
    thetalist=concat([thetalist,[5.5933, 45, 39.4067]])
# testscript.m:26
    
    thetalist=concat([thetalist,[45,- 45,90]])
# testscript.m:27
    
    i=int(size(thetalist)[1])
# testscript.m:29
    for j in arange(1,i).reshape(-1):
        if (compareFKtoIK(thetalist[j,arange(0,2)].reshape(-1),tolerance) == 1):
            print('FKtoIK test ' + j + ' failed')
        else:
            print('FKtoIK test ' + j + ' completed')
    
    #input list for further testing IK function and workspace
    positionlist=concat([concat([[L3],[L1 + L2],[0]])])
# testscript.m:39
    
    positionlist=concat([[positionlist],[concat([[L1 + L2 + L3],[0],[0]])]])
# testscript.m:40
    
    positionlist=concat([[positionlist],[concat([[L1 + L3],[L2],[0]])]])
# testscript.m:41
    
    positionlist=concat([[positionlist],[concat([[L1 - L2 + L3],[0],[0]])]])
# testscript.m:42
    
    #this contact position is our zero position but because the orientation is
#incorrect, it's a workspace failure based on our restrictions
    positionlist=concat([[positionlist],[concat([[0],[L1 + L2 + L3],[0]])]])
# testscript.m:46
    
    i=size(positionlist) / 3
# testscript.m:48
    for j in arange(1,i).reshape(-1):
        thetalist_a,thetalist_b,success=IK(concat([[positionlist(dot(j,3) - 2)],[positionlist(dot(j,3) - 1)],[positionlist(dot(j,3))]]),nargout=3)
# testscript.m:50
        if (checkJointAngleBounds(thetalist_a(1),thetalist_a(2),thetalist_a(3),tolerance) == 1) and (checkJointAngleBounds(thetalist_b(1),thetalist_b(2),thetalist_b(3),tolerance) == 1):
            print('neither A solution or B solution in bounds')
            success=1
# testscript.m:53
        if (success == 1):
            print('IK workspace test ' + j + ' failed')
        else:
            print('IK workspace test ' + j + ' completed')
    
