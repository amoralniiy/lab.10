import speech_recognition
import pyttsx3
import requests
import json
import webbrowser

class VoiceAssistant:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""

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
            recognized_data = recognizer.recognize_google(audio, language="en").lower()

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
        voice_input = voice_input.split(" ")
        command = voice_input[0]

        if command == "hey":
            play_voice_assistant_speech("Hey! How can i help you?")

        if command == "find":
            try:
                comm = voice_input[1]
                res = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + comm)
                data = res.json()[0]

                while True:
                    voice_input1 = record_and_recognize_audio()
                    print(voice_input1)
                    command1 = voice_input1

                    if command1 == "example":
                        for i in data["meanings"][0]["definitions"]:
                            try:
                                response = i["example"]
                                break
                            except:
                                pass
                        play_voice_assistant_speech(response)

                    if command1 == "definition":
                        for i in data["meanings"][0]["definitions"]:
                            try:
                                response = i["definition"]
                                break
                            except:
                                pass
                        play_voice_assistant_speech(response)

                    if command1 == "antonyms":
                        response = data["meanings"][0]["antonyms"]
                        response = ", ".join(response)
                        play_voice_assistant_speech(response)

                    if command1 == "synonyms":
                        response = data["meanings"][0]["synonyms"]
                        response = ", ".join(response)
                        play_voice_assistant_speech(response)

                    if command1 == "link":
                        url = res.json()[0]["phonetics"][0]["sourceUrl"]
                        print(url)
                        play_voice_assistant_speech("Here you are")
                        webbrowser.get().open(url)

                    if command1 == "phonetic":
                        phonetic = res.json()[0]["phonetics"][0]["phonetic"]
                        print(phonetic)
                        play_voice_assistant_speech("Here you are")


                    if command1 == "okay":
                        play_voice_assistant_speech("Stopping finding")
                        break

            except Exception as e:
                print("Exception :", e)
                pass
        if command == "thanks":
            play_voice_assistant_speech("You welcome")

        if command == "bye":
            play_voice_assistant_speech("See you later, goodbye!")
            ttsEngine.stop()
            quit()