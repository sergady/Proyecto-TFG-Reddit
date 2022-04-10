from numpy import empty_like
from ReadSample import storeTextsInArray
import sys
from datetime import datetime

def setFileOutput():
    file_name = 'results/result_'+str(datetime.now().__str__().replace(" ", "_").replace(":","-")[:-7])+'.txt'
    sys.stdout = open(file_name, 'w')


[preprocessedTexts, sample_seed] = storeTextsInArray()
print("Texts loaded!")
print("Semilla de sample_file.txt: " + sample_seed)