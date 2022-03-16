format short

L1 = 0.31685;
L2 = 0.250;
L3 = 0.15352;

% tolerance to compare return values of FK and IK to the thousandth of a degree of rotation
tolerance = 0.001;

%input list for testing FK and IK, the results for both functions should be
%the same
thetalist = [[0 0 90]];  %pass
thetalist = [thetalist; [90 0 0]]; %pass
thetalist = [thetalist; [0 45 45]]; %pass
thetalist = [thetalist; [0 135 -45]]; %pass
thetalist = [thetalist; [0 180 -90]]; %pass
thetalist = [thetalist; [90 -90 90]]; %pass
thetalist = [thetalist; [90 -45 45]]; %pass
thetalist = [thetalist; [-45 45 90]]; %pass
thetalist = [thetalist; [-45 90 45]]; %pass
thetalist = [thetalist; [-45 135 0]]; %pass
thetalist = [thetalist; [-90 90 90]]; %pass
thetalist = [thetalist; [45 45 0]]; %pass
thetalist = [thetalist; [-90 135 45]]; %pass
thetalist = [thetalist; [-90 180 0]]; %pass
thetalist = [thetalist; [5.5933 45 39.4067]]; %pass
thetalist = [thetalist; [45 -45 90]]; %pass

i = size(thetalist);
for j = 1:i
    if (compareFKtoIK(thetalist(j,1:3), tolerance) == 1)
        disp("FKtoIK test " + j + " failed");
    else
        disp("FKtoIK test " + j + " completed");
    end
end

%input list for further testing IK function and workspace
positionlist = [[L3; L1 + L2; 0]]; %pass with joint angles [0 0 90]
positionlist = [positionlist; [L1 + L2 + L3; 0; 0]]; %pass with [90 0 0]
positionlist = [positionlist; [L1 + L3; L2; 0]]; %pass with [90 -90 90]
positionlist = [positionlist; [L1 - L2 + L3; 0; 0]]; %joint angle failure

%this contact position is our zero position but because the orientation is
%incorrect, it's a workspace failure based on our restrictions
positionlist = [positionlist; [0; L1 + L2 + L3; 0]]; %workspace failure

i = size(positionlist)/3;
for j = 1:i
    [thetalist_a, thetalist_b, success] = IK([positionlist(j*3 - 2); positionlist(j*3 - 1); positionlist(j*3)]);
    if (checkJointAngleBounds(thetalist_a(1), thetalist_a(2), thetalist_a(3), tolerance) == 1 ) && (checkJointAngleBounds(thetalist_b(1), thetalist_b(2), thetalist_b(3), tolerance) == 1 ) 
        disp("neither A solution or B solution in bounds");
        success = 1;
    end
    
    if (success == 1)
        disp("IK workspace test " + j + " failed");
    else
        disp("IK workspace test " + j + " completed");
    end
end
