import tinyik
import numpy as np

arm = tinyik.Actuator([[0., 0., 1.], 'x', [0., 0., 1.], 'z', [0., 0., 1.], 'x', [1., 0., 0.], 'z', [0., 0., -1.], 'x', [0., 0., 1.], 'z', [0., 0., 1.], 'x', [0., 0., 1.]])

#arm.angles = np.deg2rad([0, 64, 0, 120, 0, 55, 0])
#print(arm.ee)

arm.ee = [0.43837115, 0.89879405, 5.        ]
print(np.round(np.rad2deg(arm.angles)))

