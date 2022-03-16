%not to be confused with the workspace of a 3R arm in general which is just
%a filled in 2D circle with radius L1 + L2 + L3
%workspace of arm poses can be considered to be a 2R semicircle workspace 
%and then offset by the 3R arm

function [success] = workspaceBoundsCheck(p_sc, p_s1)
    %define lengths of arm links in m
    L1 = 0.31685;
    L2 = 0.250;
    L3 = 0.15352;
    
    %define 2R arm outer and inner radii
    R1 = L1 - L2;
    R2 = L1 + L2;
    
    %calculate position vector of the contact point with respect to joint 1
    p_1c = [p_sc(1) - p_s1(1); p_sc(2) - p_s1(2); p_sc(3) - p_s1(3)];
    
    %calculate position vector of joint 3 with respect to joint 1
    p_13 = p_1c;
    p_13(1) = p_1c(1) - L3;
    
    r = sqrt(p_13(1)^2 + p_13(2)^2);
    
    if (r > (R2+eps)) || (r < (R1 - eps))
        success = 1;
    else
        success = 0;
    end
    
end