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
%p_sb - the 1x3 vector that indicates the position of the bottle with
%respect to the space frame 1x3 vector

%Outputs:
%theta1 - joint angle of R1 in degrees
%theta2 - joint angle of R2 in degrees
%theta3 - joint angle of R3 in degrees
%success - bool if function was successful or not - 1 is success, 0 is fail

function [theta1, theta2, theta3, success] = IK(p_sb)
    %error case
    %insert if statement if the ball position is in the arm manipulability
    %circle/ellipsoid also need to code arm manipulability function
    
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
   
    %consider link 3 offset to calculate position of joint 3 with respect
    %to the space frame
    p_s3 = p_sb;
    %orientation of end-effector is same as space-frame as well as link 3
    %being in parallel to x-axis hence the offset is always in the x-axis
    p_s3(1) = p_sb(1) - L3;
    
    disp(p_s3);
    
    %apply cosine law to find righty/lefty solutions for joint angles
    px = (-1)*p_s3(1);
    py = p_s3(2);
    
    gamma = atan2(py,px);   %calculate sum of joint angles in radians
    beta = acos((L1^2 + L2^2 - px^2 - py^2)/(2*L1*L2));
    alpha = acos((px^2 + py^2 + L1^2 - L2^2)/(2*L1*sqrt(px^2 + py^2)));
    
    phi_1a = gamma - alpha;
    phi_1b = gamma + alpha;
    
    phi_2a = pi - beta;
    phi_2b = beta - pi;
    
    theta1 = phi_1a*180/pi;
    theta2 = phi_2a*180/pi;
    theta3 = -1*(theta1 + theta2);
    theta1 = theta1 - 90; %reference taken from y-axis
    
    %determine if righty or lefty solution is within joint angle bounds
    if checkJointAngleBounds(theta1, theta2, theta3) == 1
        theta1 = phi_1b*180/pi;
        theta2 = phi_2b*180/pi;
        theta3 = -1*(theta1 + theta2);
        theta1 = theta1 - 90; %reference taken from y-axis
    end
    
    
    success = 1;
    
    disp(theta1);
    disp(theta2);
    disp(theta3);
    disp(success);
    
end