from threading import Thread
import time
import cv2
import numpy as np
from detector import DetectorAPI
from datetime import datetime
from colors import ColorDetect
from collections import Counter



class VideoManager(Thread):
    def __init__(self,filename, detector, gui_settings, gui_handler):
        Thread.__init__(self)
        self.filename = filename
        self.detector = detector
        self.gui_settings = gui_settings
        self.gui_handler = gui_handler
    
    def run(self):        
        print('File name: ' + self.filename)
        self.timestamp_begin = time.time()
        self.analyze_and_save_frames()
        print('Finished loading contents from file')
    
   
    def analyze_and_save_frames(self):
        # load video capture from file
        video = cv2.VideoCapture(self.filename)
        #get attributes from file
        self.video_length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))

        #create output files names and open them
        filename_date = datetime.now().strftime("%d%m%Y-%H%M%S")

        file_output_path =  "output/" + filename_date + ".avi"
        out = cv2.VideoWriter(file_output_path, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                      60, (frame_width, frame_height))
      
       
        file_output_log_path = "output/log-" + filename_date + ".txt" 

        log_file_out = open(file_output_log_path, 'a')
        log_file_out.write("frame, people_num, blue, green, red \n")


        frame_count = 0
        #analyze video frame by frame
        while video.isOpened():
            # Read video capture

            ret, frame = video.read()

            if frame is None:
                cv2.destroyAllWindows()
                video.release()
                return
            
            #handle frame in tensorflow
            boxes, scores = self.detector.processFrame(frame)
            person_color = []
            for i in range(len(boxes)):
                try:
                    #check each box produced by detector for threshold
                    #threshold value is fetched from gui
                    threshold = int(self.gui_settings['threshold'].get())
                    threshold = threshold/100
                    if threshold < 0.1:
                        threshold = 0.1
                #simple exception so threshold stays> 0
                except:
                    threshold = 0.1
                if scores[i] < threshold:
                    continue
                box = boxes[i]
                colorDef = ColorDetect(box, frame)
                color = colorDef.detect()
                cv2.rectangle(frame, (box[1], box[0]), (box[3], box[2]), color[0], 2)
                person_color.append(color[1])

            color_val= [0,0,0]
            for i, val in enumerate(person_color):
                if person_color[i] == "blue":
                    color_val[0] +=1
                elif person_color[i] == "green":
                    color_val[1] +=1
                else:
                    color_val[2] +=1


            log_file_out.write(
                str(frame_count) + ", " +
                str(len(boxes)) + ", " +
                str(color_val[0]) + ", " +
                str(color_val[1]) + ", " +
                str(color_val[2]) + "\n")

            if ret == True:
                out.write(frame)

                #show preview depending on current gui settings
                if self.gui_settings['show_preview'].get():
                    cv2.imshow("preview", frame)
                else:
                    cv2.destroyAllWindows()
                
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break

            
                frame_count = frame_count +1;  
                #create metadata for gui progress(progress bar, time left, etc.)    
                data = {
                    "frame_count" : frame_count,
                    "video_length" : self.video_length,
                    "timestamp_begin": self.timestamp_begin,
                    "timestamp_now": time.time()
                }
                #pass it to gui
                self.gui_handler(data)
              

        log_file_out.close()
        # Release capture object
        video.release()
        cv2.destroyAllWindows()


        # Exit and destroy all windows
       


