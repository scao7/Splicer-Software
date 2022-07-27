% treadmil control author: Shengting Cao
webcamlist
cam = webcam(2);

pyExec = 'C:\Users\chrli\anaconda3\';
pyRoot = fileparts(pyExec);
p = getenv('PATH');
p = strsplit(p, ';');
addToPath = {
   pyRoot
   fullfile(pyRoot, 'Library', 'mingw-w64', 'bin')
   fullfile(pyRoot, 'Library', 'usr', 'bin')
   fullfile(pyRoot, 'Library', 'bin')
   fullfile(pyRoot, 'Scripts')
   fullfile(pyRoot, 'bin')
};
p = [addToPath(:); p(:)];
p = unique(p, 'stable');
p = strjoin(p, ';');
setenv('PATH', p);

!conda activate openpose
!python D:\Shengting\mount2matlab.py

pyenv('Version','version')

% net = importKerasNetwork("D:\Shengting\utmb_resnet50v2.h5")

% while true
% 
% img = snapshot(cam);
% image(img)
%  
% end

  

% 
% % Open the connection (do it only once at start of the control session)
% remote = tcpclient('localhost', 4000);
% fopen(remote);
% 
% % Set speed to 1m/s, with 0.1m/s^2 acceleration, on all belts
% tm_set(remote, 0, 1);
% 
% % Close the connection (do it only once at the end of the control session)
% clear remote
% % fclose(remote);