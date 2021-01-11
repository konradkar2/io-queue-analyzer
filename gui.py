import tkinter as tk 
import tkinter.ttk as ttk
from tkinter import W,LEFT,filedialog,Checkbutton,Spinbox
import time
import os
from videoManager import VideoManager


class Gui:
    def __init__(self,detector):
        self.root = tk.Tk() 
        self.root.geometry("480x205")
        self.root.title('Queue analyzer') 
        self.root.resizable(False, False)
        self._show_preview = tk.BooleanVar()
        self._set_controls()

        #simple object that is passed to videoManager(running on different thread) to inform him about current settings
        self.settings = {
            'show_preview' : self._show_preview,
            'threshold' : self.spin_threshold
        }
        

        
        self.detector = detector


        

        self.root.mainloop() 
    #sets filename in the object and sets some text gui labels
    def _select_file_handler(self):        
        file_obj = filedialog.askopenfile(mode="r",initialdir = "./",filetypes = (("all files","*.*"),("mp4 files","*.mp4"),("avi files","*.avi*")))
        filename = file_obj.name    
        if filename:
            self.filename = filename
            self.label_path.config(text = "Path: " +filename)
            filesize = os.path.getsize(filename)
            self.label_file_size.config(text ="Size: " + str(round(filesize/1024)) + " KB")

            self.button_start.config(state="normal")
            
    #handler that will take care of updating gui
    def _progress_changed_handler(self,data):
        frame_count = data['frame_count']
        video_length = data['video_length']
        timestamp_begin = data['timestamp_begin']
        timestamp_now = data['timestamp_now']

        _progress = (frame_count/video_length)*100
        self.progress['value'] = _progress
        past_time = timestamp_now - timestamp_begin
        self.label_status.config(text = "Analyzed frame: " + str(frame_count) + '/' + str(video_length) + "\t" + str(round(_progress)) + "%")
        if _progress == 100:
            self.label_status.config(text = "Done!")


        self.label_time_past.config(text = "Time past: " + str(round(past_time)) + " s")

        seconds_left = (1/(_progress/100)* past_time) - past_time
        self.label_time_left.config(text = "Elapsed time left: " + str(round(seconds_left)) + " s")
   
    
    #creates VideoManager object and populates it
    #settings is reference that keeps VideoManager on track with gui settings
    #._progress_changed_handler is handler to update GUI through VideoManager object   
    #starts its on a new thread
    def _begin_analyze_handler(self):   
        VideoManager(self.filename,self.detector,self.settings,lambda progress: self._progress_changed_handler(progress)).start()
       
          

    def _set_controls(self):
        self.button_select = tk.Button(self.root, text='Choose files', width=25, command=self._select_file_handler) 

        self.button_start = tk.Button(self.root,text="Begin analyze",width=25,command=self._begin_analyze_handler)
        self.button_start.config(state="disabled")

        self.label_spin_threshold = tk.Label(self.root,text="Threshold %",anchor=W, justify=LEFT, width=15)
        self.spin_threshold = Spinbox(self.root,from_=0, to=100)
        
        self.check_show_preview = Checkbutton(self.root, text="Show preview" ,variable=self._show_preview,anchor=W, justify=LEFT)
        
        self.label_path = tk.Label(self.root,text="Path: file not selected",anchor=W, justify=LEFT, width=60)
        self.label_file_size = tk.Label(self.root,text="Size: ",anchor=W,justify=LEFT,width=60)
        

        self.progress = ttk.Progressbar(self.root, orient = 'horizontal', 
                    length = 450, mode = 'determinate') 

        self.label_status = tk.Label(self.root,text="Status: ",anchor=W, justify=LEFT, width=60)
        self.label_time_past = tk.Label(self.root,text="Time past: ",anchor=W, justify=LEFT, width=60)
        self.label_time_left = tk.Label(self.root,text="Elapsed time left: ",anchor=W, justify=LEFT, width=60)
        
        self.button_select.grid(row=0,column=0,padx=2,pady=2)
        self.button_start.grid(row=0,column=1,padx=2,pady=2)

        self.label_spin_threshold.grid(row=1,padx=2,columnspan=1,sticky=W)
        self.spin_threshold.grid(row=1,column=0,padx=80,sticky=W,columnspan=2)
       
        self.check_show_preview.grid(row=2,column=0,sticky=W)

        self.label_path.grid(row=3,column=0,padx=2,columnspan=2)
        self.label_file_size.grid(row=4,column=0,padx=2,columnspan=2)
        self.progress.grid(row=5,column=0,padx=2,columnspan=3,)
        self.label_status.grid(row=6,column=0,padx=2,columnspan=2)
        self.label_time_past.grid(row=7,column=0,padx=2,columnspan=2)
        self.label_time_left.grid(row=8,column=0,padx=2,columnspan=2)








