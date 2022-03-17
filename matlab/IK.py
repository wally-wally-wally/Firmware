# Generated with SMOP  0.41
from smop.libsmop import *
from workspaceBoundsCheck import workspaceBoundsCheck
from numpy import rad2deg, arccos, arctan2
# IK.m

    # Inverse Kinematics function
# Given the position of the bottle with respect to the space frame, find
# the joint angles
    
    # Links are always constant
    
    # for now it is assumed space frame is same position as R joint 1
# but it's easy to update just update the x_s1, y_s1, and z_s1 with these
# coordinates being the position of joint 1 with respect to the space frame
    
    # we can assume the orientation of the bottle will be the same as the space
# frame
    
    # we can assume the orientation of the end-effector will always be a 90
# degree rotation of the space frame in -z-axis [0 -1 0; 1 0 0; 0 0 0]
    
    #Inputs:
#R_sc - the 3x3 rotation matrix of the contact point with respect to the
#space frame
#p_sc - the 1x3 vector that indicates the position of the contact point
#with respect to the space frame
    
    #Outputs:
#theta1 - joint angle of R1 in degrees
#theta2 - joint angle of R2 in degrees
#theta3 - joint angle of R3 in degrees
#success - bool if function was successful or not : 1 is success, 0 is fail
    
    #need to handle case where there's two possible solutions, only one
#solution or no solution
    
@function
def IK(p_sc=None,*args,**kwargs):
    varargin = IK.varargin
    nargin = IK.nargin

    success=0
# IK.m:32
    
    L1=0.258
# IK.m:35
    L2=0.191
# IK.m:36
    L3=0.153521
# IK.m:37
    
    x_s1=0
# IK.m:40
    y_s1=0
# IK.m:41
    z_s1=0
# IK.m:42
    
    #p_s1=concat([[x_s1],[y_s1],[z_s1]])
    p_s1=[x_s1,y_s1,z_s1]
# IK.m:43
    
    #if the contact point is in the workspace but the pose is infeasible,
    #the joint angle error case should catch it instead
    #print(p_sc)
    #print(p_s1)
    # TODO UNCOMMENT
    if workspaceBoundsCheck(p_sc,p_s1) == 1:
        success=1
# IK.m:49
        thetalist_a=concat([[0],[0],[0]])
# IK.m:50
        thetalist_b=concat([[0],[0],[0]])
# IK.m:51
        #disp('contact is outside of arm reach')
        return thetalist_a,thetalist_b,success
    
    
    #define 3x3 identity matrix
    I=concat([[1,0,0],[0,1,0],[0,0,1]])
# IK.m:57
    
    x_1c=p_sc[0] - x_s1
# IK.m:60
    y_1c=p_sc[1] - y_s1
# IK.m:61
    L=sqrt((x_1c - L3) ** 2 + y_1c ** 2)
# IK.m:63
    delta=arctan2(y_1c,(x_1c - L3))
# IK.m:64
    rho_arg = (L1 ** 2 + L ** 2 - L2 ** 2) / (dot(dot(2,L1),L))
    #print('rho_arg ' + str(rho_arg))
    if rho_arg > 1:
        rho_arg = 1
    if rho_arg < -1:
        rho_arg = -1
    rho=arccos(rho_arg)
    #
# IK.m:65
    theta1a=90 - rad2deg(delta) - rad2deg(rho)
# IK.m:66
    theta1b=90 - rad2deg(delta) + rad2deg(rho)
# IK.m:67
    omega_arg = (L1 ** 2 + L2 ** 2 - L ** 2) / (dot(dot(2,L1),L2))
    #print('omega_arg ' + str(omega_arg))
    if omega_arg > 1:
        omega_arg = 1
    if omega_arg < -1:
        omega_arg = -1

    omega=arccos(omega_arg)
    
    #print('omega' + str(omega), flush = True)
# IK.m:69
    theta2a=180 - rad2deg(omega)
# IK.m:70
    theta2b=rad2deg(omega) - 180
# IK.m:71
    theta3a=90 - theta1a - theta2a
# IK.m:73
    theta3b=90 - theta1b - theta2b
# IK.m:74
    thetalist_a=concat([theta1a,theta2a,theta3a])
# IK.m:77
    thetalist_b=concat([theta1b,theta2b,theta3b])
# IK.m:78
   # disp(thetalist_a)
   # disp(thetalist_b)
  # disp(success)
    return thetalist_a,thetalist_b,success
    
if __name__ == '__main__':
    pass
    
