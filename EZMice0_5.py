#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import threading
import datetime
import picamera
import time
from subprocess import call
import os

class EZMiceApp:
    def __init__(self, master):
        self.master = master
        self.master.title('EZMice v0.4.1')

        # Improve the style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Initialize variables
        self.record_duration = tk.StringVar()
        self.chamber_number = tk.StringVar()
        self.animal_tag = tk.StringVar()
        self.save_path = tk.StringVar()
        self.recording = False

        # Build the GUI
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.master, text='Record Duration (s):').grid(row=0, column=0, sticky='w')
        ttk.Label(self.master, text='Chamber Number:').grid(row=1, column=0, sticky='w')
        ttk.Label(self.master, text='Animal Tag:').grid(row=2, column=0, sticky='w')
        ttk.Label(self.master, text='Folder Path:').grid(row=3, column=0, sticky='w')

        self.duration_entry = ttk.Entry(self.master, textvariable=self.record_duration)
        self.duration_entry.grid(row=0, column=1)
        ttk.Entry(self.master, textvariable=self.chamber_number).grid(row=1, column=1)
        ttk.Entry(self.master, textvariable=self.animal_tag).grid(row=2, column=1)
        self.folder_entry = ttk.Entry(self.master, textvariable=self.save_path, state='readonly')
        self.folder_entry.grid(row=3, column=1)
        ttk.Button(self.master, text='Select Folder', command=self.select_folder).grid(row=3, column=2)
        
        self.record_button = ttk.Button(self.master, text='Record', command=self.toggle_record)
        self.record_button.grid(row=4, column=0, sticky='ew')
        ttk.Button(self.master, text='Capture Image', command=self.capture_and_display).grid(row=4, column=2, sticky='ew')

        self.info_label = ttk.Label(self.master, text='')
        self.info_label.grid(row=5, column=0, columnspan=3)

        self.image_label = ttk.Label(self.master)
        self.image_label.grid(row=6, column=0, columnspan=3, sticky='nsew')

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path.set(folder)

    def get_filename(self):
        now = datetime.datetime.now()
        filename = f"/Chamber{self.chamber_number.get()}_Tag{self.animal_tag.get()}_{now.strftime('%Y%m%d_%H%M%S')}"
        return filename

    def toggle_record(self):
        if not self.recording:
            try:
                duration = int(self.record_duration.get())
                self.recording = True
                self.record_thread = threading.Thread(target=self.record_with_preview, daemon=True)
                self.record_thread.start()
                self.record_button.config(text='Stop')
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer for duration.")
        else:
            self.recording = False
            self.record_button.config(text='Record')

    def record_with_preview(self):
        filename = self.save_path.get() + self.get_filename()
        os.chdir(self.save_path.get())
        with picamera.PiCamera() as camera:
            camera.resolution = (1296,972) # 1080p Full HD resolution
            # Set frame rate to 30 fps
            camera.exposure_mode = 'auto' # Auto exposure mode
            camera.awb_mode = 'auto' # Auto white balance mode
            camera.iso = 100 # Set ISO to 100 for clearer image
            
            # Set digital zoom (crop area)
            camera.zoom = (0.25,0.05,1,1) # Adjust these values as needed (x, y, width, height)

            camera.start_preview()
            time.sleep(2)
            camera.start_recording("{0}.h264".format(filename))
            self.info_label.config(text=f"Recording to {filename}")
            start_time = datetime.datetime.now()
            ##try:
                #while (datetime.datetime.now() - start_time).seconds < int(self.record_duration.get()) and self.recording:
            camera.wait_recording(int(self.record_duration.get()))
                   # self.master.update()
           #finally:
            camera.stop_recording()
            camera.stop_preview()
            if self.recording:
                self.info_label.config(text=f"Video saved to {filename}")
            else:
                self.info_label.config(text="Recording stopped.")
            self.recording = False
            self.record_button.config(text='Record')
            command = "MP4Box -add {0}.h264 {1}.mp4".format(filename,filename)
            call([command], shell = True)
            
    def capture_and_display(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (1920, 1080)
            camera.capture('image.jpg')

            image = Image.open('image.jpg')
            image.show()  # Keep a reference.

def main():
    root = tk.Tk()
    app = EZMiceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
