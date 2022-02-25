function [success] = compareFKtoIK(thetalist, tolerance)
    success = 0;
    theta1 = thetalist(1);
    theta2 = thetalist(2);
    theta3 = thetalist(3);
    
    [R_sc, p_sc, success] = FK(theta1, theta2, theta3);
    if success == 1
        disp("FK error");
        return;
    end

    [philist_a, philist_b, success] = IK(p_sc);

    if success == 1
        disp("IK failure");
        return;
    end
    
    useBSolution = 1;
    
    if checkJointAngleBounds(philist_a(1), philist_a(2), philist_a(3)) == 1
        useBSolution = 0;
    end
    
    if abs(philist_a(1) - theta1) <= tolerance
        disp("theta1 success");
    else
        disp("theta1 failure");
        disp(philist_a(1));
        disp(theta1);
        useBSolution = 0;
    end

    if abs(philist_a(2) - theta2) <= tolerance
        disp("theta2 success");
    else
        disp("theta2 failure");
        disp(philist_a(2));
        disp(theta2);
        useBSolution = 0;
    end

    if abs(philist_a(3) - theta3) <= tolerance
        disp("theta3 success");
    else
        disp("theta3 failure");
        disp(philist_a(3));
        disp(theta3);
        useBSolution = 0;
    end
    
    if useBSolution == 0
        if checkJointAngleBounds(philist_a(1), philist_a(2), philist_a(3)) == 1
            disp("A solution not feasible and B solution is out of bounds");
            return;
        end
        if abs(philist_b(1) - theta1) <= tolerance
            disp("theta1 success");
        else
            disp("theta1 failure");
            disp(philist_b(1));
            disp(theta1);
            success = 1;
            return;
        end

        if abs(philist_b(2) - theta2) <= tolerance
            disp("theta2 success");
        else
            disp("theta2 failure");
            disp(philist_b(2));
            disp(theta2);
            success = 1;
            return;
        end

        if abs(philist_b(3) - theta3) <= tolerance
            disp("theta3 success");
        else
            disp("theta3 failure");
            disp(philist_b(3));
            disp(theta3);
            success = 1;
            return;
        end
end