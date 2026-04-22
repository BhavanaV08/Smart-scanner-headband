import cv2 import pytesseract import RPi.GPIO as GPIO import time from gtts import gTTS import os

BUTTON_PIN = 17 START_AUDIO = "/home/smartscanner/Desktop/instruction.mp3" OUTPUT_AUDIO = "/home/smartscanner/Desktop/output.mp3" IMAGE_PATH = "/home/smartscanner/Desktop/captured.jpg"

def play_audio(text, audio_file): tts = gTTS(text=text, lang="en") tts.save(audio_file) os.system("amixer set Master 90%") os.system(f"mpg321 -q {audio_file}")

def capture_image(image_path): os.system(f"libcamera-still -o {image_path} --timeout 10000")

def extract_text(image_path): img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] text = pytesseract.image_to_string(img, lang="eng") return text.strip()

GPIO.setmode(GPIO.BCM) GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try: time.sleep(10) play_audio("System is ready. Press the button to start the OCR process.", START_AUDIO)

while True:
    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        play_audio("Capturing image.", START_AUDIO)
        capture_image(IMAGE_PATH)

        extracted_text = extract_text(IMAGE_PATH)

        if extracted_text:
            play_audio("Reading detected text.", START_AUDIO)
            play_audio(extracted_text, OUTPUT_AUDIO)
        else:
            play_audio("No text detected.", START_AUDIO)

        time.sleep(2)

    time.sleep(0.1)
except KeyboardInterrupt: pass

finally: GPIO.cleanup()
