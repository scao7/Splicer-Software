# this file is function that will be called in matlab
print('System start')
print('Note: Turn on the matlab and type matlab.engine.shareEngine')
import matlab.engine
from time import sleep
# from oct2py import Oct2Py
eng = matlab.engine.connect_matlab()
print(matlab.engine.find_matlab())
eng.addpath(r"C:\Program Files (x86)\Bertec\Treadmill\Remote")
eng.workspace['remote'] = eng.eval("tcpip('localhost',4000);")

# start session
eng.eval('fopen(remote)',nargout=0)


eng.eval('tm_set(remote,1,1)',nargout=0)
sleep(5)
eng.eval('tm_set(remote,0.5,1)',nargout=0)

# end session
eng.eval('fclose(remote)',nargout =0)

