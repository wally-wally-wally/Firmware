function [x] = checkJointAngleBounds(theta1, theta2, theta3)
    if (theta1 < -90 || theta1 > 90 || theta2 < -180 || theta2 > 180 || theta3 < -90 || theta3 > 90 || (theta1 + theta2) < 0 || (theta1 + theta2) > 180)
        x = 1;
    else
        x = 0;
end