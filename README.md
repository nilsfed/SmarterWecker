# SmarterWecker #
Projektarbeit WS 19/20 Thema: Smarter Wecker

## Genutzte Hardware:
* Raspberry Pi 4 (OS: Raspbian Buster)
* Raspberry Pi 7" Touchscreen Display
* Kopfhörer/Lautsprecher (3,5mm Klinke)
* USB-Mikrofon

## Funktionen:
* Uhrzeit
* Alarm/Wecker
* Wetter (OpenWeatherMap)
* Kalender (Google Developer Console: Calendar API, Credentials)
* Speech-To-Text (Mozilla DeepSpeech 0.6.1)
* Alarm per Sprache ausschalten: “Turn off”

## Code:
Einstiegspunkt: smart_clock.py

## Benötigte Apt-Packages auf Raspbian:
* sudo apt-get python-tk
* sudo apt-get install python3-pil python3-pil.imagetk
* sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
* sudo apt-get install python3-pil python3-pil.imagetk
* sudo apt-get install python3-pyaudio

## Applikation geschrieben in Python (3.7.3)

## Genutzte Python Libraries/Pip-Packages:
* Tkinter (GUI)
* pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
* pip3 install deepspeech
* pip3 install pyaudio
* pip3 install scipy
 
## Entwicklung:
* Zunächst SSH-Verbindung
* später Remote Desktop 
  * https://tutorials-raspberrypi.de/raspberry-pi-remote-desktop-verbindung/
  * sudo apt-get install xrdp



## weitere Anregungen:
mit DeepSpeech: zunächst Wake-Word, danach viele weitere Funktionen möglich
