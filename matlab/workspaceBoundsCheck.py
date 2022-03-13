# Generated with SMOP  0.41
from smop.libsmop import *
# workspaceBoundsCheck.m

    #not to be confused with the workspace of a 3R arm in general which is just
#a filled in 2D circle with radius L1 + L2 + L3
#workspace of arm poses can be considered to be a 2R semicircle workspace 
#and then offset by the 3R arm
    
    
@function
def workspaceBoundsCheck(p_sc=None,p_s1=None,*args,**kwargs):
    varargin = workspaceBoundsCheck.varargin
    nargin = workspaceBoundsCheck.nargin

    #define lengths of arm links in m
    L1=0.31685
# workspaceBoundsCheck.m:8
    L2=0.25
# workspaceBoundsCheck.m:9
    L3=0.15352
# workspaceBoundsCheck.m:10
    
    R1=L1 - L2
# workspaceBoundsCheck.m:13
    R2=L1 + L2
# workspaceBoundsCheck.m:14
    
    p_1c=concat([[p_sc(1) - p_s1(1)],[p_sc(2) - p_s1(2)],[p_sc(3) - p_s1(3)]])
# workspaceBoundsCheck.m:17
    
    p_13=copy(p_1c)
# workspaceBoundsCheck.m:20
    p_13[1]=p_1c(1) - L3
# workspaceBoundsCheck.m:21
    r=sqrt(p_13(1) ** 2 + p_13(2) ** 2)
# workspaceBoundsCheck.m:23
    if (r > (R2 + eps)) or (r < (R1 - eps)):
        success=1
# workspaceBoundsCheck.m:26
    else:
        success=0
# workspaceBoundsCheck.m:28
    
    
    return success
    
if __name__ == '__main__':
    pass
    