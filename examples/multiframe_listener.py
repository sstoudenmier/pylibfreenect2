# coding: utf-8

import numpy as np
import cv2
from pylibfreenect2 import Freenect2, FrameMap, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame


fn = Freenect2()
device = fn.openDefaultDevice()

listener = SyncMultiFrameListener(
    FrameType.Color | FrameType.Ir | FrameType.Depth)

# Register listeners
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)

device.start()

# NOTE: must be called after device.start()
registration = Registration(device.getIrCameraParams(),
                            device.getColorCameraParams())

undistorted = Frame(512, 424, 4)
registered = Frame(512, 424, 4)

while True:
    frames = FrameMap()
    listener.waitForNewFrame(frames)

    color = frames["color"]
    ir = frames["ir"]
    depth = frames["depth"]

    registration.apply(color, depth, undistorted, registered)

    cv2.imshow("ir", ir.asarray() / 65535.)
    cv2.imshow("depth", depth.asarray() / 4500.)
    cv2.imshow("color", cv2.resize(color.asarray(), (512, 424)))
    cv2.imshow("registered", registered.astype(np.uint8))

    listener.release(frames)

    key = cv2.waitKey(delay=1)
    if key == ord('q'):
        break

device.stop()
device.close()
