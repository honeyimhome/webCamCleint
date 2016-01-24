
import cv2
import numpy
import os
import time
import requests
import base64
import pyttsx
import json
#from pygame import mixer
from gtts import gTTS

classifierPath = '/opt/opencv/data/haarcascades/haarcascade_frontalface_alt.xml'

baseURL = 'http://hih.maxfresonke.com'
# baseURL = '127.0.0.1:3000'

url = baseURL + '/api/recognizeImage'
houseID = '56a4dab23b5497c00f202da8';
albumName = 'vhuvp5LKlqmsh8SRrw5l6H08eJnDp1MJDr2jsnCe40HSfVS6P9CashHouse'
albumKey = '455f6c8615c31df211293810133e2ee150421f5fbaedf1ac2221a25c643e540c'

shortMode = False

def main():

    while True:
        detectPerson()


def performGreeting(user):
    print user
    print user['_id']

    profile = user['profile']
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
    print 'THIS IS YOUR RESPONSE: ' + r.text

    try:
        potentialUser = json.loads(r.text)
    except:
        return

    if potentialUser['isGuest'] == True:
        say('Unknown guest detected. Sending Picture Message to household.')
        return
    performGreeting(potentialUser['user'])

    if (r.text == "##") or (r.text == "###"):
        return detectPerson()


def say(text):
   path = 'say-temp.mp3'
   tts = gTTS(text=text, lang= 'en')
   tts.save(path)
   os.system("mpg123 "+path)
   os.remove(path)

def playMp3(path):
    os.system("mpg123 "+ path)



def saveFace(imagePath):
    if os.path.isfile(classifierPath) is not True:
        raise '\n\n***********!!!No training file present\n\n'
    counter = 0;

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
            print('counter is ' + str(counter))
            if located is not () and len(located) == 1:
                print located
                # print image
                counter += 1
                if counter >= 20:
                     cv2.imwrite(imagePath, image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                     return
            else:
                counter = 0



def encodeImage(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read())







if __name__ == '__main__':
    main()
