from gui import Gui
from detector import DetectorAPI




modelPath = 'model3.pb'
threshold = 0.3
detector = DetectorAPI(modelPath)


gui = Gui(detector)
