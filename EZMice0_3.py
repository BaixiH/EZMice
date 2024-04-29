#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog
import picamera
import datetime
from PIL import Image

class EZMiceApp:
    def __init__(self, master):
        self.master = master
        self.master.title('EZMice v0.2')

        # Initialize variables
        
        self.record_duration = tk.StringVar()
        self.chamber_number = tk.StringVar()
        self.animal_tag = tk.StringVar()
        self.save_path = tk.StringVar()
        self.recording = False
        #self.captured_image = None

        # GUI elements
        self.create_widgets()
    
    #def color_change(self):
     #       self.button.configure(bg="red")

    def create_widgets(self):
        ttk.Label(self.master, text='Record Duration').grid(row=0, column=0, sticky='w')
        ttk.Label(self.master, text='Chamber Number').grid(row=1, column=0, sticky='w')
        ttk.Label(self.master, text='Animal Tag').grid(row=2, column=0, sticky='w')
        ttk.Label(self.master, text='Folder Path').grid(row=3, column=0, sticky='w')

        self.duration_entry = ttk.Entry(self.master, textvariable=self.record_duration)
        self.duration_entry.grid(row=0, column=1)
        ttk.Entry(self.master, textvariable=self.chamber_number).grid(row=1, column=1)
        ttk.Entry(self.master, textvariable=self.animal_tag).grid(row=2, column=1)
        self.folder_entry = ttk.Entry(self.master, textvariable=self.save_path, state='readonly')
        self.folder_entry.grid(row=3, column=1)
        ttk.Button(self.master, text='Select Folder', command=self.select_folder).grid(row=3, column=2)
        self.button = tk.Button(self.master, text='Record', command=self.toggle_record, bg='green')
        self.button.grid(row=4, column=1)
        ttk.Button(self.master, text='Capture Image', command=self.capture_and_display).grid(row=4, column=2)

        self.info_label = ttk.Label(self.master, text='')
        self.info_label.grid(row=5, columnspan=3)

        self.image_label = ttk.Label(self.master)
        self.image_label.grid(row=6, columnspan=3)

    def select_folder(self):
        self.save_path.set(filedialog.askdirectory())

    def get_filename(self):
        now = datetime.datetime.now()
        filename = f"/Chamber{self.chamber_number.get()}_Tag{self.animal_tag.get()}_{now.strftime('%Y%m%d_%H%M%S')}.h264"
        return filename

    def toggle_record(self):
        #if self.recording:
        self.button.config(activebackground="red")
            #self.recording = False
            #self.blinking()
        self.record()
        #self.button.config(bg="white")
        #else:
            #self.recording = True
            #self.capture_image()

    def record(self):
        duration = int(self.record_duration.get())
        filename = self.save_path.get() + self.get_filename()

        with picamera.PiCamera() as camera:
            camera.resolution = (1920, 1080)
            camera.start_recording(filename)
            camera.wait_recording(duration)
            camera.stop_recording()

        self.info_label.config(text=f"Video saved to {filename}")

    def capture_and_display(self):
    	# Initialize the PiCamera
    	with picamera.PiCamera() as camera:
        	# Set camera resolution
        	camera.resolution = (640, 480)
        
        	# Capture an image
        	camera.start_preview()
        	#time.sleep(2)  # Give the camera some time to adjust to light
        	camera.capture('image.jpg')
        	camera.stop_preview()
    
    	# Display the captured image
    	image = Image.open('image.jpg')
    	image.show()

def main():
    root = tk.Tk()
    app = EZMiceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()