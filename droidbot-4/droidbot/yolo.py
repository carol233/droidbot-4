import os
import subprocess
from .global_config import *

class YoloException(Exception):
    pass

class YoloDetector():
    BOUNDS = []
    x0 = y0 = x1 = y1 = 0
    CONTAIN_ICON = False
    CONTAIN_ICON_TYPE = []
    CONTAIN_ICONS_INFO = []  #[['info', 0, 0 , 1, 1], ['close', 0, 0, 1, 1]]
    # Because one screenshot may have several icons with the same type

    def __init__(self, pic, bounds):
        self.SCREENSHOT_PATH = pic
        self.filename = os.path.split(pic)[-1]
        self.Prediction_dir = Prediction_dir
        if not os.path.exists(self.Prediction_dir):
            os.mkdir(self.Prediction_dir)
        self.tmp_txt_path = self.SCREENSHOT_PATH + ".txt"
        self.txt_path = os.path.join(self.Prediction_dir, self.filename + ".txt")
        self.after_pre = os.path.join(self.Prediction_dir, self.filename)

        self.BOUNDS = bounds
        self.x0 = bounds[0][0]
        self.y0 = bounds[0][1]
        self.x1 = bounds[1][0]
        self.y1 = bounds[1][1]


    def analyze_result(self, txt_path):
        with open(txt_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip():
                    self.CONTAIN_ICON = True
                    row = line.split(" ")
                    class_name = row[-1]
                    if class_name not in self.CONTAIN_ICON_TYPE:
                        self.CONTAIN_ICON_TYPE.append(class_name)
                    self.CONTAIN_ICONS_INFO.append(row)


    def start(self):
        retval = os.getcwd()
        os.chdir(DARKNET_DIR)
        if not self.filename.endswith(".jpg"):
            return

        """
        ./darknet detect yolov3-voc-test.cfg yolov3-voc_1000.weights $file -out $savename
        """
        try:
            cmd = "./darknet detect yolov3-voc-test.cfg yolov3-voc_1000.weights "\
                + self.SCREENSHOT_PATH + " -out " + self.after_pre
            out_bytes = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            out_bytes = e.output  # Output generated before error
            code = e.returncode  # Return code
        try:
            cmd2 = "mv " + self.tmp_txt_path + " " + self.txt_path
            out_bytes2 = subprocess.check_output(cmd2, shell=True)
        except subprocess.CalledProcessError as e:
            out_bytes2 = e.output  # Output generated before error
            code = e.returncode  # Return code

        self.analyze_result(self.txt_path)
        os.chdir(retval)
        return self.CONTAIN_ICON
