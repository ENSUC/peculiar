import tellopy
import av
import cv2

# Connect to the drone
drone = tellopy.Tello()
drone.connect()
drone.wait_for_connection(60.0)

# Set the drone to video mode
drone.set_video_encoder_rate(tellopy.VideoBitrate.MBit_2)

# Create a video container and start streaming video from the drone
container = av.open(drone.get_video_stream())

# Navigate to directory and import module
from pathlib import Path
import sys
path = Path("Yolov5/")
sys.path.append(str(path.resolve()))
from detect import run

# Start the object detection on the video stream
run(weights='Yolov5/runs/train/yolov5s_results/weights/best.pt', imgsz = (416, 416), 
        conf_thres=0.4, source=container,save_txt=True, name="video_stream")

# Close the video stream
drone.close_video()

# Disconnect from the drone
drone.disconnect()


import tellopy
import av
import cv2
import keyboard
import numpy

drone = tellopy.Tello()

def on_press(key):
    global drone
    try:
        if key.name == 'q':  # Connect to the drone when 'q' is pressed
            if not drone.connect():
                print("Tello not connected")
            else:
                drone.wait_for_connection(60.0)
                drone.set_video_encoder_rate(tellopy.VideoBitrate.MBit_2)
                container = av.open(drone.get_video_stream())
                print("Tello connected")
                show_video_stream(container)
        elif key.name == 'w':  # Disconnect from the drone when 'w' is pressed
            drone.close_video()
            drone.disconnect()
            print("Tello disconnected")
    except Exception as e:
        print(e)

def show_video_stream(container):
    for frame in container.decode(video=0):
        img = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
        cv2.imshow("Tello Video Stream", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.close_video()
            drone.disconnect()
            break

#Listen for key presses

keyboard.on_press(on_press)


