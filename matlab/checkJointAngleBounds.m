%{
function [x] = checkJointAngleBounds(theta1, theta2, theta3)
    if (theta1 < -90 || theta1 > 90 || theta2 < -180 || theta2 > 180 || theta3 < -90 || theta3 > 90 || (theta1 + theta2) < 0 || (theta1 + theta2) > 180)
        x = 1;
    else
        x = 0;
    end
end

%}

function [x] = checkJointAngleBounds(theta1, theta2, theta3, tolerance)
    if (theta1 < -(90 + tolerance) || theta1 > (90 + tolerance))
        x = 1;
        disp("theta1 out of bounds");
    elseif (theta2 < -(180 + tolerance) || theta2 > (180 + tolerance))
        x = 1;
        disp("theta2 out of bounds");
    elseif ((theta3 < -(90 + tolerance)) || (theta3 > (90 + tolerance)))
        x = 1;
        disp("theta3 out of bounds");
        disp(theta3);
    elseif ((theta1 + theta2) < -tolerance || (theta1 + theta2) > (180 + tolerance))
        x = 1;
        disp("theta1 + theta2 out of bounds");
    else
        x = 0;
    end
end