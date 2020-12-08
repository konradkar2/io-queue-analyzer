import numpy as np

class ColorDetect:
    def __init__(self, box, frame):
        self.box = box
        self.frame = frame

    def detect(self):
        img = self.frame[int((self.box[2] - self.box[0]) / 2 + self.box[0] - 30):int((self.box[2] - self.box[0]) / 2 + self.box[0] + 30),
              int((self.box[3] - self.box[1]) / 2 + self.box[1] - 10):int((self.box[3] - self.box[1]) / 2 + self.box[1] + 10)]

        height, width, _ = np.shape(img)

        # calculate the average color of each row of our image
        avg_color_per_row = np.average(img, axis=0)

        # calculate the averages of our rows
        avg_colors = np.average(avg_color_per_row, axis=0)

        # so, convert that array to integers
        int_averages = np.array(avg_colors, dtype=np.uint8)
        if int_averages[0] > int_averages[1] and int_averages[0] > int_averages[2]:
            color = [(255, 0, 0), "blue"]
        elif int_averages[1] > int_averages[0] and int_averages[1] > int_averages[2]:
            color = [(0, 255, 0), "green"]
        else:
            color = [(0, 0, 255), "red"]

        return color