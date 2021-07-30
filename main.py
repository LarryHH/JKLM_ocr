import numpy as np
import pytesseract
import cv2
import configparser
import re
import json
from PIL import ImageGrab
import random
from time import sleep
import pyautogui
import keyboard

  
def config_load(fp):
    config = configparser.ConfigParser()
    config.read(fp)
    return str(config.get('PATH', 'path'))

def dictionary_load(fp):
    with open(fp) as f:
        data = json.load(f)
    return data

def word_finder(dictionary, substring):
    potential_words = [word for word in dictionary if substring in word]
    return potential_words[random.randrange(len(potential_words))] if potential_words else None

def autotyper(x, y, word):
    pyautogui.click(x, y)
    pyautogui.write(word, interval=0.05)
    keyboard.wait('enter')

def imToString(tesseract_fp, dictionary):
    pytesseract.pytesseract.tesseract_cmd = tesseract_fp
    while(True):
        if keyboard.is_pressed('esc') == True:
            break
        sleep(0.3)
        if keyboard.is_pressed('esc') == True:
            break
        cap = ImageGrab.grab(bbox =(1250, 735, 1310, 775))
        #cap = ImageGrab.grab(bbox =(1220, 700, 1350, 800))
        #cap.show()
        substring = pytesseract.image_to_string(
                cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2GRAY), 
                lang ='eng')
        substring = re.sub(r'\W+', '', substring).lower()
        print(substring)
        if ((substring is None) or (not substring.isalpha())):
            print("YOU PLAY GAME NOW!!!!!!!!!!!!!!!!!!")
            keyboard.wait('enter')

        potential_word = word_finder(dictionary, substring)
        print(potential_word)

        if (potential_word is None):
            print("YOU PLAY GAME NOW!!!!!!!!!!!!!!!!!!")
            keyboard.wait('enter')
        else:
            autotyper(1300, 1350, word_finder(dictionary, potential_word))

def main():
    dictionary = dictionary_load('words.json')
    imToString(config_load('tesseract_path.ini'), dictionary)

if __name__ == "__main__":
    main()