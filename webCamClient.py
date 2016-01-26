
import cv2
import numpy
import os
import time
import requests
import base64
import pyttsx
import json
import platform
#from pygame import mixer
from gtts import gTTS

classifierPath = None
mp3PlayProgram = None

baseURL = 'http://hih.maxfresonke.com'
# baseURL = '127.0.0.1:3000'

url = baseURL + '/api/recognizeImage'
houseID = '56a4dab23b5497c00f202da8';
albumName = 'vhuvp5LKlqmsh8SRrw5l6H08eJnDp1MJDr2jsnCe40HSfVS6P9CashHouse'
albumKey = '455f6c8615c31df211293810133e2ee150421f5fbaedf1ac2221a25c643e540c'

shortMode = False

def main():
    configProgram()

    while True:
        detectPerson()

def configProgram():
    global classifierPath
    global mp3PlayProgram
    system = platform.system()
    print 'System is Running on ' + system
    if system == 'Darwin':
        mp3PlayProgram = 'afplay'
        classifierPath = "/usr/local/Cellar/opencv/2.4.12_2/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
    else:
        mp3PlayProgram = 'mpg123'
        print "I see you're not running on Darwin. Please be sure to set the classifierPath correctly in the python file."
        classifierPath = "/opt/opencv/data/haarcascades/haarcascade_frontalface_alt.xml"

def performGreeting(user):
    profile = user['profile']

    print '\nUser ' + profile['name'] + ' Detected!\n'
    say(profile['greeting'])
    if not shortMode:
        say('The weather is looking chilly outside! Better stay warm!')
        say('I am adjusting the temperature to your preferred' + str(profile['temperature']) + 'degrees fahrenheit')
    time.sleep(3)

    if 'Nicolas' == profile['name']:
        say('I will now play ' + str(profile['song']))
        playMp3('/home/max/Desktop/webCamCleint/FrankSinatraNewYorkNewYork.mp3.mp3')

    if 'song' in profile and profile['song'] == "all along the watchtower" and not shortMode:
        say('I will now play' + str(profile['song']))
        playMp3('/home/max/Desktop/webCamCleint/AllAlongTheWatchtowerAudio.mp3.mp3')



def detectPerson():
    imagePath = 'temp-image.jpg'
    saveFace(imagePath)
    imageB64 = encodeImage(imagePath)

    payload = {'image': imageB64, 'albumName': albumName, 'albumKey': albumKey, 'houseID': houseID}
    r = requests.post(url, data=payload)
    #print 'Server Res: ' + r.text

    try:
        potentialUser = json.loads(r.text)
    except:
        print 'Server Returned: ' + r.text
        return

    if potentialUser['isGuest'] == True:
        print '\nUnknown  Guest Detected.\n'
        say('Unknown guest detected. Sending Picture Message to household.')
        return
    performGreeting(potentialUser['user'])

    if (r.text == "##") or (r.text == "###"):
        return detectPerson()


def say(text):
   path = 'text.mp3'
   tts = gTTS(text=text, lang= 'en')
   tts.save(path)
   playMp3(path)
   os.remove(path)

def playMp3(path):
    os.system(mp3PlayProgram + " " + path)

def saveFace(imagePath):
    print "Classifier Path is: " + classifierPath
    if os.path.isfile(classifierPath) is not True:
        raise '\n\n***********!!!No training file present\n\n'
    counter = 0;
    state = -1;
    lastUserNum = -1

    face_cascade =     cv2.CascadeClassifier(classifierPath)
    # print loadedCasca deClassifier

    camera = cv2.VideoCapture(0)
    while camera.isOpened():
            _, image = camera.read()
            # cv2.imshow('Original', image)

            try:
                greyimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);
            except:
                continue

            # cv2.imshow('greyImage', greyimage)
            located = face_cascade.detectMultiScale(
                greyimage,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                #flags = cv2.cv.CV_HAAR_SCALE_IMAGE
            )

            if located is not () and len(located) == 1:
                state = 1
                print 'Detected Person! Located at ' + str(located)
                counter += 1
                if counter >= 20:
                     cv2.resize(image, (0,0), fx=0.5, fy=0.5)
                     cv2.imwrite(imagePath, image, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
                     return
            elif len(located) > 1:
                counter = 0
                if state != 2 or lastUserNum != len(located):
                    lastUserNum = len(located)
                    state = 2
                    print 'Detected ' + str(len(located)) + ' People in Frame!'
            else:
                if state != 3:
                    state = 3
                    print 'No People Detected.'
                counter = 0

def encodeImage(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read())







if __name__ == '__main__':
    main()
