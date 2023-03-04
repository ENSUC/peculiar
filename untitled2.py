import tellopy
import av
import cv2
import keyboard

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
                run_detection(container)
        elif key.name == 'w':  # Disconnect from the drone when 'w' is pressed
            drone.close_video()
            drone.disconnect()
            print("Tello disconnected")
    except Exception as e:
        print(e)

def run_detection(container):
    # Navigate to directory and import module
    from pathlib import Path
    import sys
    path = Path("Yolov5/")
    sys.path.append(str(path.resolve()))
    from detect import run

    # Start the object detection on the video stream
    run(weights='Yolov5/runs/train/yolov5s_results/weights/best.pt', imgsz = (16, 416), 
            conf_thres=0.4, source=container,save_txt=True, name="video_stream")
    #Listen for key presses
    keyboard.on_press(on_press)
    
    #Keep the program running until a key is pressed
    while True:
        pass






