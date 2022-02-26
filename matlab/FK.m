% Forward Kinematics function
% Given some theta1, theta2, theta3, find the end-effector
% position/rotation
% Links are always constant
% for now it is assumed space frame is same position as R joint 1
% but it's easy to update just update the x_s1, y_s1, and z_s1 with these
% coordinates being the position of joint 1 with respect to the space frame

%Inputs:
%theta1 - joint angle of R1 in degrees
%theta2 - joint angle of R2 in degrees
%theta3 - joint angle of R3 in degrees

%Outputs:
%R_sc - the 3x3 rotation matrix of the contact point with respect to the
%space frame
%p_sc - the 1x3 vector that indicates the position of the contact point
%with respect to the space frame
%success - bool if function was successful or not : 0 is success, 10 is fail

function [R_sc, p_sc, success] = FK(theta1, theta2, theta3, tolerance)
    %error case
    if checkJointAngleBounds(theta1, theta2, theta3, tolerance) == 1
        R_sc = [0 0 0; 0 0 0; 0 0 0];
        p_sc = [0; 0; 0];
        success = 1;
        disp("error");
        return;
    end
    
    %define joint angles in radians
    phi_1 = deg2rad(theta1);
    phi_2 = deg2rad(theta2);
    phi_3 = deg2rad(theta3);
    
    %define lengths of arm links in m
    L1 = 0.31685;
    L2 = 0.250;
    L3 = 0.15352;
    
    %define distance between joint 1 and space frame
    x_s1 = 0;
    y_s1 = 0;
    z_s1 = 0;       %this will probably remain zero because 2-D space
    
    %define 3x3 identity matrix
    I = [1 0 0; 0 1 0; 0 0 1];
    
    %define home position of end-effector
    M = [1 0 0 x_s1; 0 1 0 (y_s1+L1+L2+L3); 0 0 1 z_s1; 0 0 0 1];
    
    %define rotation velocities of joints (all the same because rotating
    %CCW around z-axis) 3x3 matrix
    w_1 = [0 1 0; -1 0 0; 0 0 0];
    w_2 = w_1;
    w_3 = w_2;
    
    %define rotation velocity vector of joints (all the same as well)
    % 1x3 vector
    wv_1 = [0; 0; 1];
    wv_2 = wv_1;
    wv_3 = wv_2;
    
    %define position vectors for each link
    %1x3 vector
    q_1 = [x_s1; y_s1; z_s1];
    q_2 = [x_s1; (y_s1+L1); z_s1];
    q_3 = [x_s1; (y_s1+L1+L2); z_s1];
        
    %calculate linear velocity vector
    v_1 = cross(wv_1, q_1);
    v_2 = cross(wv_2, q_2);
    v_3 = cross(wv_3, q_3);
        
    %calculate rotation matricies based off of input thetas
    %3x3 matrix
    R_s1 = I + sin(phi_1)*w_1 + (1 - cos(phi_1))*w_1*w_1;
    R_12 = I + sin(phi_2)*w_2 + (1 - cos(phi_2))*w_2*w_2;
    R_23 = I + sin(phi_3)*w_3 + (1 - cos(phi_3))*w_3*w_3;
    
    %calculate position vector for each link transform matrix
    %1x3 vector
    p_s1 = (I*phi_1 + (1 - cos(phi_1))*w_1 + (phi_1 - sin(phi_1))*w_1*w_1)*v_1;
    p_12 = (I*phi_2 + (1 - cos(phi_2))*w_2 + (phi_2 - sin(phi_2))*w_2*w_2)*v_2;
    p_23 = (I*phi_3 + (1 - cos(phi_3))*w_3 + (phi_3 - sin(phi_3))*w_3*w_3)*v_3;

    %form link to link transform matricies
    %4x4 matrix
    T_s1 = [R_s1 p_s1; 0 0 0 1];
    T_12 = [R_12 p_12; 0 0 0 1];
    T_23 = [R_23 p_23; 0 0 0 1];
    
    %calculate final transform matrix
    T_sc = T_s1*T_12*T_23*M;
    
    %extract rotation matrix and position matrix
    R_sc = T_sc(1:3,1:3);
    p_sc = T_sc(1:3,4);
    success = 0;
    
    disp(T_sc);
    disp(R_sc);
    disp(p_sc);
    disp(success);
    
end
    
    
    