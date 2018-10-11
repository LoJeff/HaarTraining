import os
import re
from subprocess import call
from subprocess import Popen
import keyboard
import random

maxNumNegatives = 12345
numStages = 3
bg = "negativesBaseBall.dat"

def merge_vec():
    #Merging vector files
    print("\nPress m to merge vecs, n for no")
    while True:
        try:
            if keyboard.is_pressed('m'):
                print("Merging positive vector files...")
                process = Popen('python mergevec.py -v posVec -o samples.vec')
                process.wait()
                return True
            elif keyboard.is_pressed('n'):
                return False
        except:
            break

def train_cascade(numPos):
    #Train Cascade
    print("\nPress t to train cascade, n for no")
    while True:
        try:
            if keyboard.is_pressed('t'):
                print("Training Cascade...")
                process = Popen('opencv_traincascade.exe -data haarcascade -vec samples.vec -bg ' + bg + ' -numStages ' + str(numStages) + ' -minhitrate 0.999 -maxfalsealarm 0.5 -numPos ' + str(int(numPos - 1) * 100) + ' -numNeg ' + str(int(numPos - 1) * 50) + ' -w 20 -h 20 -nonsym True -mem 512 -mode ALL')
                return True
            elif keyboard.is_pressed('n'):
                return False
        except:
            break

if __name__ == "__main__":
    #Get all paths
    curDir = os.getcwd()
    os.chdir(curDir + "\openCVTraining")
    curDir = os.getcwd()
    pos_path = curDir + "/positives"
    posOld_path = curDir + "/positivesOld"

    #Opening text document to update count
    f = open('numSamples.txt', 'r+')
    fDat = f.read()
    fDatNum = [int(s) for s in fDat.split() if s.isdigit()]
    fDatOld = list(fDatNum)
    fDatSplit = fDat.split('\n')

    #Converting any pictures in positives to vec files and putting it into positivesOld if requested
    for path,dirs,files in os.walk(pos_path):
        for filename in files:
            ranSeed1 = random.randrange(0, maxNumNegatives)
            ranSeed2 = random.randrange(0, maxNumNegatives)
            os.rename(pos_path + '/' + filename, posOld_path + '/' + filename)
            filestr = filename.split('.')
            process = Popen('opencv_createsamples.exe -img positivesOld/' + filename + ' -num 50 -bg ' + bg + ' -vec posVec/' + filestr[0] + '0.vec -maxxangle 0.6 -maxyangle 0 -maxzangle 0.3 -maxidev 100 -bgcolor 0 -bgthresh 0 -w 20 -h 20 -rngseed ' + str(ranSeed1))
            process = Popen('opencv_createsamples.exe -img positivesOld/' + filename + ' -num 50 -bg ' + bg + ' -vec posVec/' + filestr[0] + '1.vec -maxxangle 0.6 -maxyangle 0 -maxzangle 0.3 -maxidev 100 -bgcolor 0 -bgthresh 0 -w 20 -h 20 -rngseed ' + str(ranSeed2))
            process.wait()
            fDatNum[0] += 1

    #Updating text document
    fDatSplit[0] = str(fDatSplit[0]).replace(str(fDatOld[0]), str(fDatNum[0]), 1)

    print(fDatSplit[0])

    f.seek(0)
    f.write(fDatSplit[0])
    f.truncate()

    merge_vec()
    train_cascade(fDatNum[0])
