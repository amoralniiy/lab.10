import pyttsx3
import requests
import speech_recognition

class VoiceAssistant:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""

class Weather:
    def __init__(self, city, temp, speed):
        self.city = city
        self.temp = temp
        self.speed = speed


def weather_recognition():
    try:
        res = requests.get("https://wttr.in/Saint-Petersburg?format=4")
        string = res.text
        cityIndex = string.find(':')
        temperatureIndex = string.find('C')
        speedIndex = string.find('km/h')
        city = string[0:cityIndex]
        temp = string[temperatureIndex - 5:temperatureIndex + 1]
        speed = string[speedIndex - 2:speedIndex + 4]
        return Weather(city, temp, speed)

    except Exception as e:
        print("Exception :", e)
        pass


def setup_assistant_voice():
    voices = ttsEngine.getProperty("voices")

    if assistant.speech_language == "en":
        assistant.recognition_language = "en-US"
        if assistant.sex == "female":
            ttsEngine.setProperty("voice", voices[1].id)
        else:
            ttsEngine.setProperty("voice", voices[2].id)
    else:
        assistant.recognition_language = "ru-RU"
        ttsEngine.setProperty("voice", voices[0].id)

def record_and_recognize_audio(*args: tuple):

    with microphone:

        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")

        return recognized_data

def play_voice_assistant_speech(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()

if __name__ == "__main__":
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    ttsEngine = pyttsx3.init()

    assistant = VoiceAssistant()
    assistant.name = "Anny"
    assistant.sex = "female"
    assistant.speech_language = "en"

    setup_assistant_voice()

    while True:

        voice_input = record_and_recognize_audio()
        print(voice_input)
        command = voice_input

        if command == "привет":
            play_voice_assistant_speech("Hello")

        if command == "какая погода":
            weather = weather_recognition()
            play_voice_assistant_speech(weather.temp)

        if command == "скорость ветра":
            weather = weather_recognition()
            play_voice_assistant_speech(weather.speed)

        if command == "город":
            weather = weather_recognition()
            play_voice_assistant_speech(weather.city)

        if command == "выведи погоду":
            weather = weather_recognition()
            print(weather.city + weather.temp + weather.speed)


        if command == "пока":
            play_voice_assistant_speech("See you later, goodbye!")
            ttsEngine.stop()
            quit()