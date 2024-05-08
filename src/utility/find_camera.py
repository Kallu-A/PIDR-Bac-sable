from contextlib import redirect_stderr

import cv2


# warning and error display but not important
def get_available_cameras():
    available_cameras = []
    # Check for 5 cameras
    with open('/dev/null', 'w') as f:
        with redirect_stderr(f):
            for i in range(5):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    available_cameras.append(i)
                    cap.release()
    return available_cameras

cameras = get_available_cameras()
if cameras:
    print("------\nAvailable Cameras:", cameras)
else:
    print("No cameras found.")