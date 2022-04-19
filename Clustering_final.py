from numpy import empty_like
from ReadAndPrepareSample import preprocessTexts
import sys
from datetime import datetime


def setFileOutput():
    file_name = 'results/result_'+str(datetime.now().__str__().replace(" ", "_").replace(":","-")[:-7])+'.txt'
    sys.stdout = open(file_name, 'w')

preprocessedTexts = preprocessTexts() # dict {listTexts:post_ids}
print("Texts loaded!")