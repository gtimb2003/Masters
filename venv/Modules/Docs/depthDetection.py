import pyrealsense2 as rs


# Create a context object. This object owns the handles to all connected realsense devices
pipeline = rs.pipeline()
pipeline.start()

def inter(Input, InputLow, InputHigh, OutputLow, OutputHigh):
    interpolate = ((Input - InputLow) / (InputHigh - InputLow)) * (OutputHigh - OutputLow) + OutputLow
    return (interpolate)

while True:
    # This call waits until a new coherent set of frames is available on a device
    # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
    frames = pipeline.wait_for_frames()
    depth = frames.get_depth_frame()

    # Read the location of the QR Code
    filepathX = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\xCoor.txt"
    xFile = open(filepathX, "r+")
    filepathtY = "C:\\Users\\geo_t\\PycharmProjects\\xArm\\venv\\Modules\\Docs\\yCoor.txt"
    yFile = open(filepathtY, "r+")
    x = int(xFile.read())
    y = int(yFile.read())
    xInt = round(inter(x, 0, 1280, 0, 640))
    yInt = round(inter(y, 0, 720, 0, 480))
    dist = depth.get_distance(xInt, yInt)
    
    print(dist)
