import speech_recognition as sr
import commandFunctions
import generateURL

#enter the name of usb microphone that you found
#using lsusb
#the following name is only used as an example
mic_name = "HDA Intel PCH: ALC3234 Analog (hw:0,0)"
#Sample rate is how often values are recorded
sample_rate = 48000
#Chunk is like a buffer. It stores 2048 samples (bytes of data)
#here.
#it is advisable to use powers of 2 such as 1024 or 2048
chunk_size = 2048
#Initialize the recognizer
r = sr.Recognizer()

#generate a list of all audio cards/microphones
mic_list = sr.Microphone.list_microphone_names()
#mic_name = "HDA Intel PCH: ALC3234 Analog (hw:0,0)"
mic_name = ''.join(mic_list[0])

#the following loop aims to set the device ID of the mic that
#we specifically want to use to avoid ambiguity.
for i, microphone_name in enumerate(mic_list):
    if microphone_name == mic_name:
        device_id = i

#use the microphone as source for input. Here, we also specify
#which device ID to specifically look for incase the microphone
#is not working, an error will pop up saying "device_id undefined"
with sr.Microphone(device_index = device_id, sample_rate = sample_rate,
                        chunk_size = chunk_size) as source:
    #wait for a second to let the recognizer adjust the
    #energy threshold based on the surrounding noise level
    r.adjust_for_ambient_noise(source)

    text = ""
    while True:
        print("Say Something")
        #listens for the user's input
        audio = r.listen(source)
        print("audio type : ")
        print(type(audio))
        try:
            text = r.recognize_google(audio)
            print("you said: " + text)

        #error occurs when google could not understand what was said

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


        ## take appropriate action according to text
        text_list = text.split()

        if text == "exit":
            break
        elif text == "Browser":
            commandFunctions.open_browser("https://www.google.com")

        if len(text_list) > 1 :
            if (text_list[0] == "Play") or (text_list[0] == "play"):
                    str = ' '.join(text_list[1:])
                    str = ''+generateURL.generateURL(str)
                    commandFunctions.open_browser(str)
