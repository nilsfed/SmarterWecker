from tkinter import *
from tkinter import messagebox

import time, datetime

root = Tk()
root.title("Smart Clock v1")
root.geometry("800x480")

# create the main sections of the layout, 
# and lay them out
top = Frame(root, bg="black")
top.pack(side=TOP, fill=BOTH, expand=True)

bottom = Frame(root, bg="black")
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

alarm_settings = Frame(bottom, bg="black")
alarm_settings.pack(fill = BOTH, expand=True, side=BOTTOM)

alarm_settings_hrs = Frame(alarm_settings, bg="black")
alarm_settings_hrs.pack(fill = BOTH, expand=True, side=LEFT)

alarm_settings_min = Frame(alarm_settings, bg="black")
alarm_settings_min.pack(fill = BOTH, expand=True, side=RIGHT)



alarm_time_hrs = 11
alarm_time_min = 00
alarm_setting = False

def tick():
    global alarm_time_hrs, alarm_time_min, alarm_setting
    current_time = time.strftime('%H:%M:%S') 
    if current_time != clock_label["text"]:
        clock_label["text"] = current_time
    now = datetime.datetime.now()
    if alarm_setting == True:
        if ((alarm_time_hrs == now.hour) & (alarm_time_min == now.minute)):
            messagebox.showinfo("ALARM!", "It's {:02d}:{:02d}".format(alarm_time_hrs, alarm_time_min))
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
    else:
        but_enable_alarm["text"] = "disabled"
    
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
    
clock_label = Label(root, font=('times', 32, 'bold'), bg='black', fg="white")
clock_label.pack(in_=top, fill=BOTH, expand=1)

alarm_label = Label(root, font=('times', 24, 'bold'), bg='black', fg="white")
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

tick()
update_alarm()
root.mainloop()
