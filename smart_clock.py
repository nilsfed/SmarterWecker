from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

import time, datetime

import audio_alarm, weather, calendar_quickstart
import threading

from deepspeech import Model
import scipy.io.wavfile as wav
import sys
import pyaudio
import wave

# Initial Values

city_of_interest = "Karlsruhe,de"
alarm_time_hrs = 11
alarm_time_min = 00
alarm_setting = False

#default forecast for debugging/offline
forecast = {'coord': {'lon': 8.4, 'lat': 49.01}, 'weather': [{'id': 701, 'main': 'Mist', 'description': 'sun', 'icon': '50n'}], 'base': 'stations', 'main': {'temp': 1.37, 'feels_like': -1.11, 'temp_min': -0.56, 'temp_max': 4, 'pressure': 1027, 'humidity': 100}, 'visibility': 1400, 'wind': {'speed': 1}, 'clouds': {'all': 90}, 'dt': 1578326220, 'sys': {'type': 1, 'id': 1314, 'country': 'DE', 'sunrise': 1578295188, 'sunset': 1578325422}, 'timezone': 3600, 'id': 2892794, 'name': 'Karlsruhe', 'cod': 200}
weather_icon = None
tk_image = None
model_retval = None

# ------------------FUNCTIONS-----------------------

# ---- CLOCK ----
def tick():
    global alarm_time_hrs, alarm_time_min, alarm_setting
    current_time = time.strftime('%H:%M:%S') 
    if current_time != clock_label["text"]:
        clock_label["text"] = current_time
    now = datetime.datetime.now()
    if alarm_setting == True:
        if ((alarm_time_hrs == now.hour) & (alarm_time_min == now.minute)):
            audio_alarm.play()
            messagebox.showinfo("ALARM!", "It's {:02d}:{:02d}".format(alarm_time_hrs, alarm_time_min))
            audio_alarm.stop()
            alarm_setting = False
            update_alarm()
    
    clock_label.after(200, tick)

def update_alarm():
    global alarm_time_hrs
    global alarm_time_min
    
    alarm_string= "Alarm:\n{:02d}:{:02d}".format(alarm_time_hrs, alarm_time_min)
    alarm_label["text"] = alarm_string
    if alarm_setting == True:
        but_enable_alarm["text"] = "enabled"
        but_enable_alarm.configure(fg="green") 
    else:
        but_enable_alarm["text"] = "disabled"
        but_enable_alarm.configure(fg="red") 
    
def inc_hrs():
    global alarm_time_hrs
    alarm_time_hrs =(alarm_time_hrs + 1)% 24
    update_alarm()

def dec_hrs():
    global alarm_time_hrs
    alarm_time_hrs = (alarm_time_hrs - 1)% 24
    update_alarm()

def inc_min():
    global alarm_time_min
    alarm_time_min =(alarm_time_min + 1)% 60
    update_alarm()
    
def dec_min():
    global alarm_time_min
    alarm_time_min =(alarm_time_min - 1)% 60
    update_alarm()

def toggle_alarm():
    global alarm_setting
    alarm_setting = not alarm_setting
    update_alarm()

# ---- AUDIO ----
# imported from audio_alarm.py

# ---- DeepSpeech
def load_model():

    models = "models/output_graph.tflite"    #.tflite
    lm = "models/lm.binary"    # lm.binary
    trie = "models/trie"  # trie

    BEAM_WIDTH = 500
    LM_ALPHA = 0.75
    LM_BETA = 1.85

    ds = Model(models, BEAM_WIDTH)

    ds.enableDecoderWithLM(lm, trie, LM_ALPHA, LM_BETA)

    sample_rate = ds.sampleRate()

    return [ds, sample_rate]


def analyze_wav_file():
    global model_retval
    fs, audio = wav.read("./tmp/speech.wav")
    print("sample rate wav file: ", fs)
    print("sample rate model:", model_retval[1])

    processed_data = model_retval[0].stt(audio)

    print(processed_data)

    with open('./tmp/data.txt', 'w') as f:

        f.write(processed_data)

    return processed_data

def initialize_DeepSpeech():
    global model_retval
    model_retval = load_model()

def run_DeepSpeech():

    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 16000 # 44.1kHz sampling rate for deepspeech: 16k
    chunk = 4096 # 2^12 samples for buffer
    record_secs = 5 # seconds to record
    dev_index = 2 # device index found by p.get_device_info_by_index(ii)
    wav_output_filename = './tmp/speech.wav' # name of .wav file

    audio = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("recording")
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("finished recording")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    analyze_wav_file()


# ---- WEATHER ----
# imported from weather.py

def update_weather():
    global forecast, weather_icon, tk_image

    try:
        forecast = weather.city_forecast(city_of_interest)
    except:
        print("no new weather data received")
    

    weather_label["text"] = forecast["weather"][0]["description"]
    temperature_label["text"] = "{:.1f}°C   Max: {:.1f}°C   Min: {:.1f}°C".format(forecast["main"]["temp"], forecast["main"]["temp_max"], forecast["main"]["temp_min"])
    icon_id = forecast["weather"][0]["icon"]
    icon_url = "https://openweathermap.org/img/wn/"+icon_id+"@2x.png"

    try:
        weather_icon = weather.weather_icon(icon_id).resize((60, 60), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(weather_icon)
        canvas.itemconfigure(weather_picture, image = tk_image)
    except:
        print("no image received")

    threading.Timer(3600, update_weather).start()


# ------ CALENDAR ------
# imported from calendar.py

def update_calendar():
    calendar_string = "Calendar entries: "
    events = calendar_quickstart.get_events(results=6)


    if not events:
        calendar_string+=('No upcoming events found.')
    for event in events:
        start = str(event['start'].get('dateTime', event['start'].get('date')))
        calendar_string+= ("\n" + start[5:10] +", " + start[11:16] + " " +event['summary'])

    calendar_label["justify"]="left"
    calendar_label["text"] = calendar_string

    threading.Timer(3600, update_calendar).start()


# ------------------GUI-----------------------

root = Tk()
root.title("Smart Clock v1")
root.geometry("800x480")

# create the main sections of the layout, 
# and lay them out
top = Frame(root, bg="black")
top.pack(side=TOP, fill=BOTH, expand=True)

top_left = Frame(top, bg="black")
top_left.pack(side=LEFT, fill = BOTH, expand= True)

top_right = Frame(top, bg="black")
top_right.pack(side=RIGHT, fill = BOTH, expand= True)

bottom = Frame(root, bg="black")
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

clock_label = Label(root, font=('TkDefaultFont', 32, 'bold'), bg='black', fg="white")
clock_label.pack(in_=bottom, fill=BOTH, expand=1)

alarm_settings = Frame(bottom, bg="black")
alarm_settings.pack(fill = BOTH, expand=True, side=BOTTOM)

alarm_settings_hrs = Frame(alarm_settings, bg="black")
alarm_settings_hrs.pack(fill = BOTH, expand=True, side=LEFT)

alarm_settings_min = Frame(alarm_settings, bg="black")
alarm_settings_min.pack(fill = BOTH, expand=True, side=RIGHT)

alarm_label = Label(root, font=('TkDefaultFont', 20, 'bold'), bg='black', fg="white")
alarm_label.pack (in_=bottom, fill= BOTH, expand=1)


but_inc_min = Button(root, text="+ min",bg='black', fg="white", width=10, height=2, command=inc_min)
but_dec_min = Button(root, text="- min",bg='black', fg="white", width=10, height=2, command=dec_min)
but_inc_hrs = Button(root, text="+ hrs",bg='black', fg="white", width=10, height=2, command=inc_hrs)
but_dec_hrs = Button(root, text="- hrs",bg='black', fg="white", width=10, height=2, command=dec_hrs)

but_inc_min.pack(in_=alarm_settings_min)
but_dec_min.pack(in_=alarm_settings_min)
but_inc_hrs.pack(in_=alarm_settings_hrs)
but_dec_hrs.pack(in_=alarm_settings_hrs)

but_enable_alarm = Button(root, text="disabled",bg='black', fg="white", width=20, height=2, command=toggle_alarm)
but_enable_alarm.pack(in_=alarm_settings)

but_speech = Button(root, text="DeepSpeech",bg='black', fg="violet", width=20, height=2, command=run_DeepSpeech)
but_speech.pack(in_=alarm_settings)

city_label = Label(root, bg='black', fg="white",font=('TkDefaultFont', 18))
city_label["text"] = "Weather in: " + city_of_interest
city_label.pack(in_=top_right)

temperature_label = Label(root, bg='black', fg="white",font=('TkDefaultFont', 15))
temperature_label.pack(in_=top_right)

canvas = Canvas(root, width=60, height=60, bg="grey")
canvas.pack(in_=top_right)

weather_picture = canvas.create_image(30, 30, image=tk_image)

weather_label = Label(root, bg='black', fg="white", font=('TkDefaultFont', 18))
weather_label.pack(in_=top_right)

calendar_label = Label(root, bg='black', fg="white", font=('TkDefaultFont', 14), anchor= "w")
calendar_label.pack(in_=top_left)

initialize_DeepSpeech()
tick()
update_alarm()
update_weather()
update_calendar()

root.mainloop()