import cv2
import numpy as np
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

from global_var import get_ratio_pixel_cm


# Function to update the video feed
def update_frame():
    ret, frame = cap.read()
    if ret:
        # Convert the frame to an image format suitable for Tkinter
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the canvas with the new frame
        canvas.imgtk = imgtk
        canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

        # Draw the text on the canvas
        y_position = frame_height + 10
        for line in text_lines:
            canvas.create_text(10, y_position, anchor=tk.NW, text=line, fill="black", font=("Helvetica", 16))
            y_position += line_height

    canvas.after(10, update_frame)

# Initialize the main window
root = tk.Tk()
root.title("Video with Text")

# Open the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Get the width and height of the video frame
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the text and calculate required height
text = "This is the first line\nThis is the second line\nThis is the third line " + str(get_ratio_pixel_cm())
text_lines = text.split('\n')
line_height = 30  # Approximate height of one line of text
text_height = line_height * len(text_lines)

# Create a canvas to display the video and text
canvas = Canvas(root, width=frame_width, height=frame_height + text_height + 20)  # Extra height for text and padding
canvas.pack()

# Start the video update loop
update_frame()

# Start the Tkinter main loop
root.mainloop()

# Release the capture when everything is done
cap.release()