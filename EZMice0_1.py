#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import picamera
import datetime

win = Tk() # initialize window

# Configuration
record_duration = StringVar()  # recording time in second, change for testing
save_path = filedialog.askdirectory()
#save_path = "/home/genglab1/Desktop/videos/"  # Update this path as needed
chamber_number = StringVar() # Example chamber number
animal_tag = StringVar()  # Animal tag number; update this as needed

def get_filename():
    """Generate a filename with chamber number, animal tag, current date and time."""
    now = datetime.datetime.now()
    filename = "/ Chamber{}_Tag{}_{}.h264".format(chamber_number.get(), animal_tag.get(), now.strftime("%Y%m%d_%H%M%S"))
    return filename

def record_video(duration, filename):
    """Record video for a given duration and save to a file."""
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)  # HD resolution; adjust as needed
        camera.start_recording(filename)
        camera.wait_recording(duration)
        camera.stop_recording()
    
    print(f"Video saved to {filename}")

def main():
    duration = int(record_duration.get())
    full_path = save_path + get_filename()
    record_video(duration, full_path)

win.title('EZMice v0.1')

ttk.Entry(win, textvariable = record_duration).grid(column = 2, row = 1)
ttk.Entry(win, textvariable = chamber_number).grid(column = 2, row = 2)
ttk.Entry(win, textvariable = animal_tag).grid(column = 2, row = 3)
ttk.Label(win, text = save_path).grid(column = 2, row = 4)

ttk.Button(win, text = 'Record', command = main).grid(column = 2, row = 5)

ttk.Label(win, text = 'record duration').grid(column = 1, row = 1)
ttk.Label(win, text = 'chamber number').grid(column = 1, row = 2)
ttk.Label(win, text = 'animal tag').grid(column = 1, row = 3)
ttk.Label(win, text = 'folder path').grid(column =1, row = 4)

%if __name__ == "__main__":
    #main()
    win.mainloop()