from gui import Gui
from detector import DetectorAPI



#define path to model, currently its in the app folder
modelPath = 'model3.pb'
threshold = 0.3
detector = DetectorAPI(modelPath)


gui = Gui(detector)
