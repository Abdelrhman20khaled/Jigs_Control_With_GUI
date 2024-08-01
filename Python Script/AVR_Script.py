"""
Author: Abdelrhman Khaled Sobhi
This code is provided to ELARABY Group Internship, All rights of this code are retained by the author. 
Date: Summer Intership 2024

Description:
This Python script uses the `tkinter` library to create a graphical user interface (GUI) for monitoring three jigs. 
It tracks the running, pausing, and stopping times for each jig. The data is read from a serial port and is used to 
update the GUI in real-time. The running and pausing times are displayed in a dedicated section for each jig. 
The data is also written to a CSV file at a specific time each day.

Modules:
- tkinter: for creating the GUI.
- datetime: for handling date and time operations.
- threading: for running tasks concurrently.
- time: for implementing sleep functionality.
- serial: for reading data from the serial port.
- csv: for writing data to CSV files.
- sys: for handling system-specific parameters and functions.
- PIL (Pillow): for image processing and display.

Constants:
- AVR_COM: The COM port used for serial communication.
- AVR_BUAD_RATE: The baud rate for serial communication.

Variables:
- rtotal1_elapsed_running_time, rtotal2_elapsed_running_time, rtotal3_elapsed_running_time: Total elapsed running 
  times for the jigs.
- ptotal1_elapsed_pause_time, ptotal2_elapsed_pause_time, ptotal3_elapsed_pause_time: Total elapsed pause times for
  the jigs.
- jig1_start_time, jig2_start_time, jig3_start_time: Start times for the jigs.
- jig1_pause_time, jig2_pause_time, jig3_pause_time: Pause times for the jigs.
- jig1_stop_time, jig2_stop_time, jig3_stop_time: Stop times for the jigs.
- rcounter_id_1, rcounter_id_2, rcounter_id_3: Threading.Timer objects for running time counters.
- pcounter_id_1, pcounter_id_2, pcounter_id_3: Threading.Timer objects for pause time counters.

Functions:
- Serial_Start: Starts the serial communication and updates the GUI based on the received data.
- counter_Start: Starts the running time counter for a specified jig.
- counter_Pause: Starts the pause time counter for a specified jig.
- counter_Stop: Stops the counters for a specified jig.
- counter_Pause_Stop: Stops the pause time counter for a specified jig.
- counter_Running_Stop: Stops the running time counter for a specified jig.
- update_Daydate: Updates the current date in the GUI.
- update_Currenttime: Updates the current time in the GUI.
- convert_timeToH_M_S: Converts a timedelta object to a formatted string (HH:MM:SS).
- CSV_WriteData: Writes the running and pause times of the jigs to a CSV file at a specific time each day.

Usage:
Run the script to start the GUI and the serial communication. The GUI will display the running, pausing, 
and stopping times for each jig, and the data will be written to a CSV file daily.

"""
import tkinter
import datetime
import threading
from time import sleep
import serial
import csv
import sys
from PIL import Image, ImageTk

AVR_COM = 'COM6'
AVR_BUAD_RATE = 9600

# Track the total elapsed time separately
rtotal1_elapsed_running_time = datetime.timedelta()
rtotal2_elapsed_running_time = datetime.timedelta()
rtotal3_elapsed_running_time = datetime.timedelta()

ptotal1_elapsed_pause_time = datetime.timedelta()
ptotal2_elapsed_pause_time = datetime.timedelta()
ptotal3_elapsed_pause_time = datetime.timedelta()

jig1_start_time = None
jig2_start_time = None
jig3_start_time = None

jig1_pause_time = None
jig2_pause_time = None
jig3_pause_time = None

jig1_stop_time = None
jig2_stop_time = None
jig3_stop_time = None

rcounter_id_1 = None
rcounter_id_2 = None
rcounter_id_3 = None

pcounter_id_1 = None
pcounter_id_2 = None
pcounter_id_3 = None

def Serial_Start():
    global jig1_start_time, jig2_start_time, jig3_start_time
    global jig1_pause_time, jig2_pause_time, jig3_pause_time

    with serial.Serial(AVR_COM, AVR_BUAD_RATE, timeout=2) as serial_port:
        try:
            while True:
                if serial_port.in_waiting > 0:
                    data = serial_port.readline(2).decode('utf-8').rstrip()
                    print(data)
                    sleep(0.1)
                    
                    if '1W' in data:
                        jig1_start_time = datetime.datetime.now()
                        counter_Start(1)
                        counter_Pause_Stop(1)
                        jig1_frame.config(bg="#3CB371")

                    elif '1P' in data:
                        jig1_pause_time = datetime.datetime.now()
                        counter_Pause(1)
                        counter_Running_Stop(1)
                        jig1_frame.config(bg="#E4D96F")

                    elif '1S' in data:
                        counter_Stop(1)
                        jig1_frame.config(bg="#B34234")

                    elif '2W' in data:
                        jig2_start_time = datetime.datetime.now()
                        counter_Start(2)
                        counter_Pause_Stop(2)
                        jig2_frame.config(bg="#3CB371")

                    elif '2P' in data:
                        jig2_pause_time = datetime.datetime.now()
                        counter_Pause(2)
                        counter_Running_Stop(2)
                        jig2_frame.config(bg="#E4D96F")

                    elif '2S' in data:
                        counter_Stop(2)
                        jig2_frame.config(bg="#B34234")   

                    elif '3W' in data:
                        jig3_start_time = datetime.datetime.now()
                        counter_Start(3)
                        counter_Pause_Stop(3)
                        jig3_frame.config(bg="#3CB371")

                    elif '3P' in data:
                        jig3_pause_time = datetime.datetime.now()
                        counter_Pause(3)
                        counter_Running_Stop(3)
                        jig3_frame.config(bg="#E4D96F")

                    elif '3S' in data:
                        counter_Stop(3)
                        jig3_frame.config(bg="#B34234")      

        except serial.SerialException as exc:
            print(f"Serial exception: {exc}")
            root.destroy()
        except Exception as e:
            print(f"Unexpected error: {e}")
            root.destroy()
            sys.exit(1)

def counter_Start(num_of_jeg=0):
    global jig1_start_time, jig2_start_time, jig3_start_time
    global rcounter_id_1, rcounter_id_2, rcounter_id_3
    global rtotal1_elapsed_running_time, rtotal2_elapsed_running_time, rtotal3_elapsed_running_time
    
    rcurrent_time = datetime.datetime.now()

    if num_of_jeg   == 1:
         relapsed_time = rcurrent_time -  jig1_start_time
    elif num_of_jeg == 2:     
         relapsed_time = rcurrent_time -  jig2_start_time
    elif num_of_jeg == 3:     
         relapsed_time = rcurrent_time -  jig3_start_time     
    
    if num_of_jeg == 1:
        rtotal1_elapsed_running_time += relapsed_time
        rtotal_seconds = int(rtotal1_elapsed_running_time.total_seconds())
        jig1_start_time = rcurrent_time
        rhours, rremainder = divmod(rtotal_seconds, 3600)
        rminutes, rseconds = divmod(rremainder, 60)
        rreal_time = "{:02d}:{:02d}:{:02d}".format(rhours, rminutes, rseconds)
        jig1_CurrentRunning_label.config(text=rreal_time)

        rcounter_id_1 = threading.Timer(1, counter_Start, args=[1])
        rcounter_id_1.start()

    elif num_of_jeg == 2:
        rtotal2_elapsed_running_time += relapsed_time
        rtotal_seconds = int(rtotal2_elapsed_running_time.total_seconds())
        jig2_start_time = rcurrent_time
        rhours, rremainder = divmod(rtotal_seconds, 3600)
        rminutes, rseconds = divmod(rremainder, 60)
        rreal_time = "{:02d}:{:02d}:{:02d}".format(rhours, rminutes, rseconds)
        jig2_CurrentRunning_label.config(text=rreal_time)
        rcounter_id_2 = threading.Timer(1, counter_Start, args=[2])
        rcounter_id_2.start()

    elif num_of_jeg == 3:
        rtotal3_elapsed_running_time += relapsed_time
        rtotal_seconds = int(rtotal3_elapsed_running_time.total_seconds())
        jig3_start_time = rcurrent_time
        rhours, rremainder = divmod(rtotal_seconds, 3600)
        rminutes, rseconds = divmod(rremainder, 60)
        rreal_time = "{:02d}:{:02d}:{:02d}".format(rhours, rminutes, rseconds)
        jig3_CurrentRunning_label.config(text=rreal_time)

        rcounter_id_3 = threading.Timer(1, counter_Start, args=[3])
        rcounter_id_3.start()
        
def counter_Pause(num_of_jeg=0):
    global jig1_pause_time, jig2_pause_time, jig3_pause_time
    global ptotal1_elapsed_pause_time, ptotal2_elapsed_pause_time,ptotal3_elapsed_pause_time
    global pcounter_id_1, pcounter_id_2,pcounter_id_3

    pcurrent_time = datetime.datetime.now()
    if num_of_jeg == 1 : 
        pelapsed_time = pcurrent_time - jig1_pause_time 
    elif num_of_jeg == 2 :
        pelapsed_time = pcurrent_time -  jig2_pause_time
    elif num_of_jeg == 3 :
        pelapsed_time = pcurrent_time -  jig3_pause_time        
    
    if num_of_jeg == 1:
        ptotal1_elapsed_pause_time += pelapsed_time
        ptotal_seconds = int(ptotal1_elapsed_pause_time.total_seconds())
        jig1_pause_time = pcurrent_time
        phours, premainder = divmod(ptotal_seconds, 3600)
        pminutes, pseconds = divmod(premainder, 60)
        rreal_time = "{:02d}:{:02d}:{:02d}".format(phours, pminutes, pseconds)
        jig1_CurrentResuming_label.config(text=rreal_time)
        
        pcounter_id_1 = threading.Timer(1, counter_Pause, args=[1])
        pcounter_id_1.start()

    elif num_of_jeg == 2:
        ptotal2_elapsed_pause_time += pelapsed_time
        ptotal_seconds = int(ptotal2_elapsed_pause_time.total_seconds())
        jig2_pause_time = pcurrent_time
        phours, premainder = divmod(ptotal_seconds, 3600)
        pminutes, pseconds = divmod(premainder, 60)
        rreal_time = "{:02d}:{:02d}:{:02d}".format(phours, pminutes, pseconds)
        jig2_CurrentResuming_label.config(text=rreal_time)
        
        pcounter_id_2 = threading.Timer(1, counter_Pause, args=[2])
        pcounter_id_2.start()

    elif num_of_jeg == 3:
        ptotal3_elapsed_pause_time += pelapsed_time
        ptotal_seconds = int(ptotal3_elapsed_pause_time.total_seconds())
        jig3_pause_time = pcurrent_time
        phours, premainder = divmod(ptotal_seconds, 3600)
        pminutes, pseconds = divmod(premainder, 60)
        rreal_time = "{:02d}:{:02d}:{:02d}".format(phours, pminutes, pseconds)
        jig3_CurrentResuming_label.config(text=rreal_time)
        
        pcounter_id_3 = threading.Timer(1, counter_Pause, args=[3])
        pcounter_id_3.start()

def counter_Stop(num_of_jeg=0):
    global stop_jig_1, stop_jig_2, stop_jig_3 
    
    if num_of_jeg == 1:
        stop_jig_1 = datetime.datetime.now().strftime("%I:%M:%S %p")
        jig1_CurrentStopping_label.config(text= stop_jig_1)
        counter_Running_Stop(1)
        counter_Pause_Stop(1)
    elif num_of_jeg == 2:
        stop_jig_2 = datetime.datetime.now().strftime("%I:%M:%S %p")
        jig2_CurrentStopping_label.config(text= stop_jig_2)    
        counter_Running_Stop(2)
        counter_Pause_Stop(2)
    elif num_of_jeg == 3:
        stop_jig_3 = datetime.datetime.now().strftime("%I:%M:%S %p")
        jig3_CurrentStopping_label.config(text= stop_jig_3)    
        counter_Running_Stop(3)
        counter_Pause_Stop(3)

def counter_Pause_Stop(num_of_jeg=0):
    global pcounter_id_1, pcounter_id_2, pcounter_id_3
    if num_of_jeg == 1:
        if pcounter_id_1 is not None:
            pcounter_id_1.cancel()
            pcounter_id_1 = None
    elif num_of_jeg == 2:
        if pcounter_id_2 is not None:
            pcounter_id_2.cancel()
            pcounter_id_2 = None
    elif num_of_jeg == 3:
        if pcounter_id_3 is not None:
            pcounter_id_3.cancel()
            pcounter_id_3 = None

def counter_Running_Stop(num_of_jeg=0):
    global rcounter_id_1, rcounter_id_2, rcounter_id_3
    if num_of_jeg == 1:
        if rcounter_id_1 is not None:
            rcounter_id_1.cancel()
            rcounter_id_1 = None
    elif num_of_jeg == 2:
        if rcounter_id_2 is not None:
            rcounter_id_2.cancel()
            rcounter_id_2 = None
    elif num_of_jeg == 3:
        if rcounter_id_3 is not None:
            rcounter_id_3.cancel()
            rcounter_id_3 = None

def update_Daydate():
    genral_day_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    date_now_label.config(text=genral_day_date)
    root.after(1000, update_Daydate)

def update_Currenttime():
    genral_current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    time_now_label.config(text=genral_current_time)

    root.after(1000, update_Currenttime)

def convert_timeToH_M_S(totalElapsedTime):
    total_seconds = int(totalElapsedTime.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    rminutes, seconds = divmod(remainder, 60)
    real_time = "{:02d}:{:02d}:{:02d}".format(hours, rminutes, seconds)
    return real_time


def CSV_WriteData():
    jig1_list = []
    jig2_list = []
    jig3_list = []
    global ptotal1_elapsed_pause_time, ptotal2_elapsed_pause_time, ptotal3_elapsed_pause_time
    global rtotal1_elapsed_running_time, rtotal2_elapsed_running_time, rtotal3_elapsed_running_time
    global stop_jig_1, stop_jig_2, stop_jig_3 
    CSV_writeTD = datetime.datetime.now()
    if CSV_writeTD.hour == 16 and CSV_writeTD.minute == 30:
        with open('month_data.csv', 'a', newline='') as file_csv:
            csv_writer = csv.writer(file_csv)
            jig1_list = [CSV_writeTD.month, CSV_writeTD.day, CSV_writeTD.year, CSV_writeTD.strftime("%I:%M:%S %p"), "Jig1",convert_timeToH_M_S( rtotal1_elapsed_running_time) , convert_timeToH_M_S(ptotal1_elapsed_pause_time), stop_jig_1]
            csv_writer.writerow(jig1_list)
            jig2_list = [CSV_writeTD.month, CSV_writeTD.day, CSV_writeTD.year, CSV_writeTD.strftime("%I:%M:%S %p"), "Jig2", convert_timeToH_M_S(rtotal2_elapsed_running_time), convert_timeToH_M_S(ptotal2_elapsed_pause_time), stop_jig_2]
            csv_writer.writerow(jig2_list)
            jig3_list = [CSV_writeTD.month, CSV_writeTD.day, CSV_writeTD.year, CSV_writeTD.strftime("%I:%M:%S %p"), "Jig3", convert_timeToH_M_S(rtotal3_elapsed_running_time), convert_timeToH_M_S(ptotal3_elapsed_pause_time),  stop_jig_3]
            csv_writer.writerow(jig3_list)
    
    root.after(60000, CSV_WriteData)
# Medium Sea Green Code    : #3CB371
# Medium Sea Red Code      : #B34234
# Medium Sea Yellow Code   : #E4D96F

root = tkinter.Tk()
root.title("Jig Monitoring")
root.geometry("1320x500")


pic_frame = tkinter.Frame(root, width=300, height=300)
pic_frame.grid(row=0, column=1, padx=10, pady=10)
image = Image.open("Logo.jpg")

image = image.resize((400, 150))

photo = ImageTk.PhotoImage(image)

label = tkinter.Label(pic_frame, image=photo)
label.image = photo
label.pack()

#===============================================================================================================================================

#bottom_frame = tkinter.Frame(root, width=1290, height=150)
#bottom_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
#
#bt_image = Image.open("Logo.jpg")
#
#frame_width = bottom_frame.winfo_reqwidth()
#frame_height = bottom_frame.winfo_reqheight()
#resized_image = bt_image.resize((frame_width, frame_height))
#bt_photo = ImageTk.PhotoImage(resized_image)
#
#bt_label = tkinter.Label(bottom_frame, image=bt_photo)
#bt_label.image = bt_photo
#bt_label.pack()


#===============================================================================================================================================

current_date_frame = tkinter.Frame(root)
current_date_frame.grid(row=0, column=0, padx=10, pady=10)

date_label = tkinter.Label(current_date_frame, text="Day Date",font=("Impact", 25))
date_label.grid(row=0, column=1)

date_now_label = tkinter.Label(current_date_frame, text="", font=("Arial", 18),bg="black",fg="white")
date_now_label.grid(row=0, column=2, padx=10)

#===============================================================================================================================================

current_time_frame = tkinter.Frame(root)
current_time_frame.grid(row=0, column=2, padx=10, pady=10)

time_label = tkinter.Label(current_time_frame, text="Current Time",font=("Impact", 25))
time_label.grid(row=0, column=1)

time_now_label = tkinter.Label(current_time_frame, text="", font=("Arial", 18),bg="black",fg="white")
time_now_label.grid(row=0, column=2, padx=10)

#===============================================================================================================================================

jig1_frame = tkinter.Frame(root,width=150,height=150,bg="#B34234",border="10px", borderwidth=2)
jig1_frame.grid(row=1, column=0,padx=10, pady=10)

jig1_Running_label  = tkinter.Label(jig1_frame,width=15,height=1 , text="Running Time", font=("Impact", 20)).grid(row = 0, column = 0,padx=10, pady=10)
jig1_CurrentRunning_label  = tkinter.Label(jig1_frame, width=10,height=1 , text="00:00:00", font=("Arial", 20))
jig1_CurrentRunning_label.grid(row = 0, column = 1,padx=10, pady=10)

jig1_Resuming_label = tkinter.Label(jig1_frame, width=15,height=1, text="Pausing Time", font=("Impact", 20)).grid(row = 1, column = 0,padx=10, pady=10)
jig1_CurrentResuming_label = tkinter.Label(jig1_frame,width=10,height=1 , text="00:00:00", font=("Arial", 20))
jig1_CurrentResuming_label.grid(row = 1, column = 1,padx=10, pady=10)


jig1_Stopping_label = tkinter.Label(jig1_frame, width=15,height=1, text="Stopping Time", font=("Impact", 20)).grid(row = 2, column = 0,padx=10, pady=10)
jig1_CurrentStopping_label = tkinter.Label(jig1_frame, width=10,height=1 ,text="00:00:00 --", font=("Arial", 20))
jig1_CurrentStopping_label.grid(row = 2, column = 1,padx=10, pady=10)  


#===============================================================================================================================================

jig2_frame = tkinter.Frame(root,width=150,height=150,bg="#B34234",border="10px", borderwidth=2)
jig2_frame.grid(row=1, column=1,padx=10, pady=10)

jig2_Running_label  = tkinter.Label(jig2_frame,width=15,height=1 , text="Running Time", font=("Impact", 20)).grid(row = 0, column = 0,padx=10, pady=10)
jig2_CurrentRunning_label  = tkinter.Label(jig2_frame, width=10,height=1 , text="00:00:00", font=("Arial", 20))
jig2_CurrentRunning_label.grid(row = 0, column = 1,padx=10, pady=10)

jig2_Resuming_label = tkinter.Label(jig2_frame, width=15,height=1, text="Pausing Time", font=("Impact", 20)).grid(row = 1, column = 0,padx=10, pady=10)
jig2_CurrentResuming_label = tkinter.Label(jig2_frame,width=10,height=1 , text="00:00:00", font=("Arial", 20))
jig2_CurrentResuming_label.grid(row = 1, column = 1,padx=10, pady=10)


jig2_Stopping_label = tkinter.Label(jig2_frame, width=15,height=1, text="Stopping Time", font=("Impact", 20)).grid(row = 2, column = 0,padx=10, pady=10)
jig2_CurrentStopping_label = tkinter.Label(jig2_frame, width=10,height=1 ,text="00:00:00 --", font=("Arial", 20))
jig2_CurrentStopping_label.grid(row = 2, column = 1,padx=10, pady=10)  

#===============================================================================================================================================

jig3_frame = tkinter.Frame(root,width=150,height=150,bg="#B34234",border="10px", borderwidth=2)
jig3_frame.grid(row=1, column=2,padx=10, pady=10)

jig3_Running_label  = tkinter.Label(jig3_frame,width=15,height=1 , text="Running Time", font=("Impact", 20)).grid(row = 0, column = 0,padx=10, pady=10)
jig3_CurrentRunning_label  = tkinter.Label(jig3_frame, width=10,height=1 , text="00:00:00", font=("Arial", 20))
jig3_CurrentRunning_label.grid(row = 0, column = 1,padx=10, pady=10)

jig3_Resuming_label = tkinter.Label(jig3_frame, width=15,height=1, text="Pausing Time", font=("Impact", 20)).grid(row = 1, column = 0,padx=10, pady=10)
jig3_CurrentResuming_label = tkinter.Label(jig3_frame,width=10,height=1 , text="00:00:00", font=("Arial", 20))
jig3_CurrentResuming_label.grid(row = 1, column = 1,padx=10, pady=10)


jig3_Stopping_label = tkinter.Label(jig3_frame, width=15,height=1, text="Stopping Time", font=("Impact", 20)).grid(row = 2, column = 0,padx=10, pady=10)
jig3_CurrentStopping_label = tkinter.Label(jig3_frame, width=10,height=1 ,text="00:00:00 --", font=("Arial", 20))
jig3_CurrentStopping_label.grid(row = 2, column = 1,padx=10, pady=10) 

#===============================================================================================================================================

# Create a frame to hold the jig names
jig1_names = tkinter.Frame(root,width=150,height=150,bg="black")
jig1_names.grid(row=2, column=0, pady=10)  # Adjust grid placement as needed

# Create labels for each jig and add them to the frame
jig1_name = tkinter.Label(jig1_names, text="Jig 1", font=("Impact", 25))
jig1_name.grid(row=0, column=0, padx=5, pady=5)

# Create a frame to hold the jig names
jig2_names = tkinter.Frame(root,width=150,height=150,bg="black")
jig2_names.grid(row=2, column=1, pady=10)  # Adjust grid placement as needed

# Create labels for each jig and add them to the frame
jig2_name = tkinter.Label(jig2_names, text="Jig 2", font=("Impact", 25))
jig2_name.grid(row=0, column=0, padx=5, pady=5)

# Create a frame to hold the jig names
jig3_names = tkinter.Frame(root,width=100,height=150,bg="black")
jig3_names.grid(row=2, column=2, pady=10)  # Adjust grid placement as needed

# Create labels for each jig and add them to the frame
jig3_name = tkinter.Label(jig3_names, text="Jig 3", font=("Impact", 25))
jig3_name.grid(row=0, column=0, padx=5, pady=5)

#Call all functions used in this script
#serial_thread = threading.Thread(target=Serial_Start)
#serial_thread.start()

CSV_File_thread = threading.Thread(target=CSV_WriteData)
CSV_File_thread.start()

update_Currenttime()

update_Daydate()

root.mainloop()
