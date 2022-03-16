# Generated with SMOP  0.41
from smop.libsmop import *
# checkJointAngleBounds.m

    
@function
def checkJointAngleBounds(theta1=None,theta2=None,theta3=None,tolerance=None,*args,**kwargs):
    varargin = checkJointAngleBounds.varargin
    nargin = checkJointAngleBounds.nargin

    if (theta1 < - (90 + tolerance) or theta1 > (90 + tolerance)):
        x=1
# checkJointAngleBounds.m:3
        #disp('theta1 out of bounds')
    else:
        if (theta2 < - (180 + tolerance) or theta2 > (180 + tolerance)):
            x=1
# checkJointAngleBounds.m:6
            #disp('theta2 out of bounds')
        else:
            if ((theta3 < - (90 + tolerance)) or (theta3 > (90 + tolerance))):
                x=1
# checkJointAngleBounds.m:9
                #disp('theta3 out of bounds')
                #disp(theta3)
            else:
                if ((theta1 + theta2) < - tolerance or (theta1 + theta2) > (180 + tolerance)):
                    x=1
# checkJointAngleBounds.m:13
                   # disp('theta1 + theta2 out of bounds')
                else:
                    x=0
# checkJointAngleBounds.m:16
    
    return x
    
if __name__ == '__main__':
    pass
    