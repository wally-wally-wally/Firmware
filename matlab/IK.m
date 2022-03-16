% Inverse Kinematics function
% Given the position of the bottle with respect to the space frame, find
% the joint angles

% Links are always constant

% for now it is assumed space frame is same position as R joint 1
% but it's easy to update just update the x_s1, y_s1, and z_s1 with these
% coordinates being the position of joint 1 with respect to the space frame

% we can assume the orientation of the bottle will be the same as the space
% frame

% we can assume the orientation of the end-effector will always be a 90
% degree rotation of the space frame in -z-axis [0 -1 0; 1 0 0; 0 0 0]

%Inputs:
%R_sc - the 3x3 rotation matrix of the contact point with respect to the
%space frame
%p_sc - the 1x3 vector that indicates the position of the contact point
%with respect to the space frame

%Outputs:
%theta1 - joint angle of R1 in degrees
%theta2 - joint angle of R2 in degrees
%theta3 - joint angle of R3 in degrees
%success - bool if function was successful or not : 1 is success, 0 is fail

%need to handle case where there's two possible solutions, only one
%solution or no solution
function [thetalist_a, thetalist_b, success] = IK(p_sc)
    success = 0;
    
    %define lengths of arm links in m
    L1 = 0.31685;
    L2 = 0.250;
    L3 = 0.15352;
    
    %define distance between joint 1 and space frame
    x_s1 = 0;
    y_s1 = 0;
    z_s1 = 0;       %this will probably remain zero because 2-D space
    p_s1 = [x_s1; y_s1; z_s1];
    
    %workspace error case
    %if the contact point is in the workspace but the pose is infeasible,
    %the joint angle error case should catch it instead
    if workspaceBoundsCheck(p_sc, p_s1) == 1
        success = 1;
        thetalist_a = [0; 0; 0];
        thetalist_b = [0; 0; 0];
        disp("contact is outside of arm reach");
        return;
    end
    
    %define 3x3 identity matrix
    I = [1 0 0; 0 1 0; 0 0 1];
    
    %calculate distance between joint 1 and contact point
    x_1c = p_sc(1) - x_s1;
    y_1c = p_sc(2) - y_s1;
    
    L = sqrt((x_1c - L3)^2 + y_1c^2);
    delta = atan2(y_1c, (x_1c - L3));
    rho = acos((L1^2 + L^2 - L2^2)/(2*L1*L));
    theta1a = 90 - rad2deg(delta) - rad2deg(rho);
    theta1b = 90 - rad2deg(delta) + rad2deg(rho);
    
    omega = acos((L1^2 + L2^2 - L^2)/(2*L1*L2));
    theta2a = 180 - rad2deg(omega);
    theta2b = rad2deg(omega) - 180;
    
    theta3a = 90 - theta1a - theta2a;
    theta3b = 90 - theta1b - theta2b;
    
    
    thetalist_a = [theta1a theta2a theta3a];
    thetalist_b = [theta1b theta2b theta3b];
    
    disp(thetalist_a);
    disp(thetalist_b);
    disp(success);
    
end