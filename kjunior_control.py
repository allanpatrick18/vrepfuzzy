import vrep # access all the VREP elements
import vrepConst as const
import time
import numpy as np         #array library

vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # start a connection
if clientID!=-1:
    print("Connected to remote API server")
    kjunior = vrep.simxGetObjectHandle(clientID, 'KJunior', const.simx_opmode_oneshot_wait)
    proxSensorHandles = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    lightSensorHandles = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    erro_code, KJunior_motorLeft = vrep.simxGetObjectHandle(clientID, 'KJunior_motorLeft', vrep.simx_opmode_oneshot_wait)
    erro_code, KJunior_motorRight = vrep.simxGetObjectHandle(clientID, 'KJunior_motorRight', const.simx_opmode_oneshot_wait)




        # errorCode, sensor_light_handl e=  vrep.simxGetObjectHandle('KJunior_lightSensor'+str(i), vrep.simx_opmode_oneshot_wait)
        # lightSensorHandles.append(sensor_light_handle);


t = time.time()

while (time.time() - t) < 60:
        for i in range(0, 10):
                errorCode, sensor_handle = vrep.simxGetObjectHandle(clientID, 'KJunior_proxSensor' + str(i + 1),vrep.simx_opmode_oneshot_wait)
            if(errorCode!=0):
                print("erro connection sensor")
            print(sensor_handle)

        proxSensorHandles[i] = sensor_handle
        results = [int(i) for i in proxSensorHandles]

        sensor_sq =0
        for x in range(3,7):
            results[x]= results[x]*results[x]

        min_ind = np.where(results == np.min(results))

        min_ind = min_ind[0][0]

        if results[min_ind] < 0.2:
            steer = -1
        else:
            steer = 0

        v = 5  # forward velocity
        kp = 0.5  # steering gain
        vl = v + kp * steer
        vr = v - kp * steer
        print("V_l =", vl)
        print("V_r =", vr)

        erro_code = vrep.simxSetJointTargetVelocity(clientID, KJunior_motorLeft, vl, vrep.simx_opmode_streaming)
        erro_code = vrep.simxSetJointTargetVelocity(clientID, KJunior_motorRight, vr, vrep.simx_opmode_streaming)
        time.sleep(0.2)  # loop executes once every 0.2 seconds (= 5 Hz)


else:
    print("Not connected to remote API server")
   # sys.exit("Could not connect")
