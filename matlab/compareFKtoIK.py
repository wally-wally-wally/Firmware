# Generated with SMOP  0.41
from smop.libsmop import *
from checkJointAngleBounds import checkJointAngleBounds
from FK import FK
from IK import IK
# compareFKtoIK.m

    
@function
def compareFKtoIK(thetalist=None,tolerance=None,*args,**kwargs):
    varargin = compareFKtoIK.varargin
    nargin = compareFKtoIK.nargin

    success=0
# compareFKtoIK.m:2
    theta1=thetalist(1)
# compareFKtoIK.m:3
    theta2=thetalist(2)
# compareFKtoIK.m:4
    theta3=thetalist(3)
# compareFKtoIK.m:5
    R_sc,p_sc,success=FK(theta1,theta2,theta3,tolerance,nargout=3)
# compareFKtoIK.m:7
    if success == 1:
        #disp('FK error')
        return success
    
    philist_a,philist_b,success=IK(p_sc,nargout=3)
# compareFKtoIK.m:13
    if success == 1:
        #disp('IK failure')
        return success
    
    
    useBSolution=1
# compareFKtoIK.m:20
    if checkJointAngleBounds(philist_a(1),philist_a(2),philist_a(3),tolerance) == 1:
        useBSolution=0
# compareFKtoIK.m:23
        #disp('A solution is infeasible')
    
    
    if useBSolution == 1:
        if abs(philist_a(1) - theta1) <= tolerance:
            #disp('theta1 success')
            pass
        else:
            #disp('theta1 failure')
            #disp(philist_a(1))
            #disp(theta1)
            useBSolution=0
# compareFKtoIK.m:34
        if abs(philist_a(2) - theta2) <= tolerance:
            #disp('theta2 success')
            pass
        else:
            #disp('theta2 failure')
            #disp(philist_a(2))
            #disp(theta2)
            useBSolution=0
# compareFKtoIK.m:43
        if abs(philist_a(3) - theta3) <= tolerance:
            #disp('theta3 success')
            pass
        else:
            #disp('theta3 failure')
            #disp(philist_a(3))
            #disp(theta3)
            useBSolution=0
# compareFKtoIK.m:52
    
    
    if useBSolution == 0:
        if checkJointAngleBounds(philist_b(1),philist_b(2),philist_b(3),tolerance) == 1:
            #disp('A solution not feasible and B solution is out of bounds')
            success=1
# compareFKtoIK.m:59
            return success
        if abs(philist_b(1) - theta1) <= tolerance:
            #disp('theta1 success')
            pass
        else:
           # disp('theta1 failure')
           # disp(philist_b(1))
            #disp(theta1)
            success=1
# compareFKtoIK.m:68
            return success
        if abs(philist_b(2) - theta2) <= tolerance:
            #disp('theta2 success')
            pass
        else:
            #disp('theta2 failure')
            #disp(philist_b(2))
            #disp(theta2)
            success=1
# compareFKtoIK.m:78
            return success
        if abs(philist_b(3) - theta3) <= tolerance:
            #disp('theta3 success')
            pass
        else:
            #disp('theta3 failure')
            #disp(philist_b(3))
            #disp(theta3)
            success=1
# compareFKtoIK.m:88
            return success
    