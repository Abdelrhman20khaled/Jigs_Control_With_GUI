Jig Monitoring GUI
Author: Abdelrhman Khaled Sobhi
Date: Summer Internship 2024
This code is provided to ELARABY Group Internship. All rights of this code are retained by the author.

Description
This Python script uses the tkinter library to create a graphical user interface (GUI) for monitoring three jigs. It tracks the running, pausing, and stopping times for each jig. The data is read from a serial port and is used to update the GUI in real-time. The running and pausing times are displayed in a dedicated section for each jig. The data is also written to a CSV file at a specific time each day.

Modules
tkinter: for creating the GUI.
datetime: for handling date and time operations.
threading: for running tasks concurrently.
time: for implementing sleep functionality.
serial: for reading data from the serial port.
csv: for writing data to CSV files.
sys: for handling system-specific parameters and functions.
PIL (Pillow): for image processing and display.
Constants
AVR_COM: The COM port used for serial communication.
AVR_BUAD_RATE: The baud rate for serial communication.
Variables
rtotal1_elapsed_running_time, rtotal2_elapsed_running_time, rtotal3_elapsed_running_time: Total elapsed running times for the jigs.
ptotal1_elapsed_pause_time, ptotal2_elapsed_pause_time, ptotal3_elapsed_pause_time: Total elapsed pause times for the jigs.
jig1_start_time, jig2_start_time, jig3_start_time: Start times for the jigs.
jig1_pause_time, jig2_pause_time, jig3_pause_time: Pause times for the jigs.
jig1_stop_time, jig2_stop_time, jig3_stop_time: Stop times for the jigs.
rcounter_id_1, rcounter_id_2, rcounter_id_3: threading.Timer objects for running time counters.
pcounter_id_1, pcounter_id_2, pcounter_id_3: threading.Timer objects for pause time counters.
Functions
Serial_Start: Starts the serial communication and updates the GUI based on the received data.
counter_Start: Starts the running time counter for a specified jig.
counter_Pause: Starts the pause time counter for a specified jig.
counter_Stop: Stops the counters for a specified jig.
counter_Pause_Stop: Stops the pause time counter for a specified jig.
counter_Running_Stop: Stops the running time counter for a specified jig.
update_Daydate: Updates the current date in the GUI.
update_Currenttime: Updates the current time in the GUI.
convert_timeToH_M_S: Converts a timedelta object to a formatted string (HH:MM
).
CSV_WriteData: Writes the running and pause times of the jigs to a CSV file at a specific time each day.
Usage
Run the script to start the GUI and the serial communication. The GUI will display the running, pausing, and stopping times for each jig, and the data will be written to a CSV file daily.
