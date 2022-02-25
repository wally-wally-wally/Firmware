L1 = 0.31685;
L2 = 0.250;
L3 = 0.15352;

% tolerance to compare return values of FK and IK to the thousandth of a degree of rotation
tolerance = 0.001;

%test list
thetalist = [[0 0 90]];  %pass
thetalist = [thetalist; [45 45 0]]; %pass
thetalist = [thetalist; [5.5933 45 39.4067]]; %pass
thetalist = [thetalist; [45 -45 90]]; %pass

i = size(thetalist);
for j = 1:i
    if (compareFKtoIK(thetalist(j,1:3), tolerance) == 1)
        disp("test " + j + " failed");
    else
        disp("test " + j + " completed");
    end
end