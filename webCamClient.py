
import cv2
import numpy
import os
import time
import requests
import base64
import pyttsx
from pygame import mixer
from gtts import gTTS

classifierPath = '/home/nicolas/opencv-2.4.11/data/haarcascades/haarcascade_frontalface_alt.xml'


def getFrame():
    if os.path.isfile(classifierPath) is not True:
        print '\n\n***********!!!No training file present\n\n'
        return;

    face_cascade =     cv2.CascadeClassifier(classifierPath)
    # print loadedCasca deClassifier

    camera = cv2.VideoCapture(1)
    while camera.isOpened():
            _, image = camera.read()
            # cv2.imshow('Original', image)

            greyimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);

            # cv2.imshow('greyImage', greyimage)
            located = face_cascade.detectMultiScale(
                greyimage,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.cv.CV_HAAR_SCALE_IMAGE
            )

            if located is not ():
                print located
                # print image
                return image



def postToServer(urlVal, albumName, albumKey):


    frame = getFrame()
    cv2.imwrite('image.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])

    with open("image.jpg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())

    with open("image.jpg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())

    payload = {'image': encoded_image, 'albumName': albumName, 'albumKey': albumKey}
    r = requests.post(urlVal, data=payload)

    if (r.text == "##") or (r.text == "###"):
        return postToServer(urlVal, albumName, albumKey)


    return r.text

def speak(text):
    engine = pyttsx.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'english-us')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    engine.say(text)
    engine.runAndWait()

    for voice in voices:
        print voice

def playMP3(path):
    mixer.init()
    mixer.music.load(path)
    mixer.music.play()
    while mixer.music.get_busy():
          print time.clock()



def main():
    url = 'http://localhost:3000/api/recognizeImage'
    albumName = '4QadXMfQOBmshnqPYVNW17aGXPUBp1rFl9jjsnfdUCjJbfqUMyNEWTESTALBUM'
    albumKey = '24af1768cc902f65191c51ecf757e549bba56c441700c8fae7eb3180783f6fa3'

    # text = postToServer(url, albumName, albumKey);
    #
    # #toDelete
    # # jsonGrab = {'name': text, 'timeOfDay': albumName, 'albumKey': albumKey}
    #
    # print text
    textToSpeak = 'Welcome home Nicolas, I am setting the temperature to 72 degrees. Have a great evening'
    tts = gTTS(text= textToSpeak, lang= 'en')
    tts.save('hello.mp3')
    path = '/home/nicolas/Downloads/Frank Sinatra - New York New York Song --Lyrics-- [HD].mp3'

    playMP3('hello.wav')
    playMP3(path)


if __name__ == '__main__':
    main()
