# Generated with SMOP  0.41
from smop.libsmop import *
from checkJointAngleBounds import checkJointAngleBounds
# FK.m

    # Forward Kinematics function
# Given some theta1, theta2, theta3, find the end-effector
# position/rotation
# Links are always constant
# for now it is assumed space frame is same position as R joint 1
# but it's easy to update just update the x_s1, y_s1, and z_s1 with these
# coordinates being the position of joint 1 with respect to the space frame
    
    #Inputs:
#theta1 - joint angle of R1 in degrees
#theta2 - joint angle of R2 in degrees
#theta3 - joint angle of R3 in degrees
    
    #Outputs:
#R_sc - the 3x3 rotation matrix of the contact point with respect to the
#space frame
#p_sc - the 1x3 vector that indicates the position of the contact point
#with respect to the space frame
#success - bool if function was successful or not : 0 is success, 10 is fail
    
    
@function
def FK(theta1=None,theta2=None,theta3=None,tolerance=None,*args,**kwargs):
    varargin = FK.varargin
    nargin = FK.nargin

    #error case
    if checkJointAngleBounds(theta1,theta2,theta3,tolerance) == 1:
        R_sc=concat([[0,0,0],[0,0,0],[0,0,0]])
# FK.m:24
        p_sc=concat([[0],[0],[0]])
# FK.m:25
        success=1
# FK.m:26
        #disp('error')
        return R_sc,p_sc,success
    
    
    #define joint angles in radians
    phi_1=deg2rad(theta1)
# FK.m:32
    phi_2=deg2rad(theta2)
# FK.m:33
    phi_3=deg2rad(theta3)
# FK.m:34
    
    L1=0.31685
# FK.m:37
    L2=0.25
# FK.m:38
    L3=0.15352
# FK.m:39
    
    x_s1=0
# FK.m:42
    y_s1=0
# FK.m:43
    z_s1=0
# FK.m:44
    
    
    #define 3x3 identity matrix
    I=concat([[1,0,0],[0,1,0],[0,0,1]])
# FK.m:47
    
    M=concat([[1,0,0,x_s1],[0,1,0,(y_s1 + L1 + L2 + L3)],[0,0,1,z_s1],[0,0,0,1]])
# FK.m:50
    
    #CCW around z-axis) 3x3 matrix
    w_1=concat([[0,1,0],[- 1,0,0],[0,0,0]])
# FK.m:54
    w_2=copy(w_1)
# FK.m:55
    w_3=copy(w_2)
# FK.m:56
    
    # 1x3 vector
    wv_1=concat([[0],[0],[1]])
# FK.m:60
    wv_2=copy(wv_1)
# FK.m:61
    wv_3=copy(wv_2)
# FK.m:62
    
    #1x3 vector
    q_1=concat([[x_s1],[y_s1],[z_s1]])
# FK.m:66
    q_2=concat([[x_s1],[(y_s1 + L1)],[z_s1]])
# FK.m:67
    q_3=concat([[x_s1],[(y_s1 + L1 + L2)],[z_s1]])
# FK.m:68
    
    v_1=cross(wv_1,q_1)
# FK.m:71
    v_2=cross(wv_2,q_2)
# FK.m:72
    v_3=cross(wv_3,q_3)
# FK.m:73
    
    #3x3 matrix
    R_s1=I + dot(sin(phi_1),w_1) + dot(dot((1 - cos(phi_1)),w_1),w_1)
# FK.m:77
    R_12=I + dot(sin(phi_2),w_2) + dot(dot((1 - cos(phi_2)),w_2),w_2)
# FK.m:78
    R_23=I + dot(sin(phi_3),w_3) + dot(dot((1 - cos(phi_3)),w_3),w_3)
# FK.m:79
    
    #1x3 vector
    p_s1=dot((dot(I,phi_1) + dot((1 - cos(phi_1)),w_1) + dot(dot((phi_1 - sin(phi_1)),w_1),w_1)),v_1)
# FK.m:83
    p_12=dot((dot(I,phi_2) + dot((1 - cos(phi_2)),w_2) + dot(dot((phi_2 - sin(phi_2)),w_2),w_2)),v_2)
# FK.m:84
    p_23=dot((dot(I,phi_3) + dot((1 - cos(phi_3)),w_3) + dot(dot((phi_3 - sin(phi_3)),w_3),w_3)),v_3)
# FK.m:85
    
    #4x4 matrix
    T_s1=concat([[R_s1,p_s1],[0,0,0,1]])
# FK.m:89
    T_12=concat([[R_12,p_12],[0,0,0,1]])
# FK.m:90
    T_23=concat([[R_23,p_23],[0,0,0,1]])
# FK.m:91
    
    T_sc=dot(dot(dot(T_s1,T_12),T_23),M)
# FK.m:94
    
    R_sc=T_sc(arange(1,3),arange(1,3))
# FK.m:97
    p_sc=T_sc(arange(1,3),4)
# FK.m:98
    success=0
# FK.m:99
    #disp(T_sc)
    #disp(R_sc)
    #disp(p_sc)
    #disp(success)
    return R_sc,p_sc,success
    
if __name__ == '__main__':
    pass
    
    
    
    