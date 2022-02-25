% Inverse Kinematics function
% Given the position of the bottle with respect to the space frame, find
% the joint angles

% Links are always constant

% for now it is assumed space frame is same position as R joint 1
% but it's easy to update just update the x_s1, y_s1, and z_s1 with these
% coordinates being the position of joint 1 with respect to the space frame

% we can assume the orientation of the bottle will be the same as the space
% frame

% we can assume the orientation of the end-effector will be the same as the
% space frame (or at least it should)

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
    %error case
    %insert if statement if the ball position is in the arm manipulability
    %circle/ellipsoid also need to code arm manipulability function
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
    
    %define 3x3 identity matrix
    I = [1 0 0; 0 1 0; 0 0 1];
    
    px = p_sc(1);
    py = p_sc(2);
    
    L = sqrt((px - L3)^2 + py^2);
    delta = atan2(py, (px - L3));
    rho = acos((L1^2 + L^2 - L2^2)/(2*L1*L));
    theta1a = 90 - delta*180/pi - rho*180/pi;
    theta1b = 90 - delta*180/pi + rho*180/pi;
    
    omega = acos((L1^2 + L2^2 - L^2)/(2*L1*L2));
    theta2a = 180 - omega*180/pi;
    theta2b = omega*180/pi - 180;
    
    theta3a = 90 - theta1a - theta2a;
    theta3b = 90 - theta1b - theta2b;
    
    
    thetalist_a = [theta1a theta2a theta3a];
    thetalist_b = [theta1b theta2b theta3b];
    
    disp(thetalist_a);
    disp(thetalist_b);
    disp(success);
    
end