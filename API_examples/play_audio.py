from tkinter import *
import pyaudio
import wave
import sys
import threading


def play_audio():
    global is_playing
    global my_thread
    chunk = 1024
    wf = wave.open('alarm_wav.wav', 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(
        format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True)

    data = wf.readframes(chunk)

    while data and is_playing: # is_playing to stop playing
        stream.write(data)
        data = wf.readframes(chunk)



    stream.stop_stream()
    stream.close()
    p.terminate()



def loop_play():
    while is_playing:
        play_audio()

def press_button_play():
    global is_playing
    global my_thread

    if not is_playing:
        is_playing = True
        my_thread = threading.Thread(target=loop_play)
        my_thread.start()


def press_button_stop():
    global is_playing
    global my_thread

    if is_playing:
        is_playing = False
        my_thread.join()

# main

is_playing = False
my_thread = None

root = Tk()
root.title("WAV-Loop")
root.geometry("400x300")

button_start = Button(root, text="PLAY", command=press_button_play)
button_start.grid()

button_stop = Button(root, text="STOP", command=press_button_stop)
button_stop.grid()

root.mainloop()