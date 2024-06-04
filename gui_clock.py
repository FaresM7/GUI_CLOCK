# Name: Fares Elbermawy
# Description: Implementing a GUI clock. Firstly, it displays the current date and time. It mainly has two features.
# The first one is the timer "aka stopwatch" which simply starts counting the time whenever you press the button.
# After you stop the timer it stores the start, end time and duration in a file of your choice. If you did not
# choose a file it will create a new file called "timer.txt" and store the result in it.
# The second one is the countdown. You specify the hours, minutes, seconds and it counts until it finishes.

import tkinter as tk
import time
from datetime import datetime
from tkinter import messagebox, filedialog
import threading


class GUIclock:
    def __init__(self, root):
        # Creating the root gui with initial dimentions of 700x500
        self.root = root
        self.root.title("GUI Clock")
        self.root.geometry("700x500")

        # A label to display current time
        self.time_label = tk.Label(self.root, font=('calibri', 40, 'bold'), background='blue', foreground='white')
        self.time_label.pack(anchor='center')
        self.update_time()

        # A label to display current date
        self.date_label = tk.Label(self.root, font=('calibri', 20), background='blue', foreground='white')
        self.date_label.pack(anchor='center')
        self.update_date()
        # A label to display how many minutes, seconds has passed since the start of the timer
        self.timer_count = tk.Label(self.root, font=('calibri', 30))
        self.timer_count.pack(anchor='center')
        self.timer_count.config(text="00:00")
        # Initialising the start time by none and a boolean stating if the timer is running.
        self.timer_running = False
        self.timer_start_time = None
        # The timer button.
        self.timer_button = tk.Button(root, text="Start Timer", command=self.toggle_timer, font=('calibri', 20), bg="green")
        self.timer_button.pack(anchor='center')
        # An enty for the file path required and the button to submit it.
        self.file_path = tk.StringVar()
        self.file_entry = tk.Entry(root, textvariable=self.file_path, width=40, font=('calibri', 12))
        self.file_entry.pack(anchor='center')
        self.file_button = tk.Button(root, text="Select File", command=self.select_file, font=('calibri', 12))
        self.file_button.pack(anchor='center')
        # Making a frame for the countdown elements so that they can be beside each other.
        self.countdown_frame = tk.Frame(root)
        self.countdown_frame.pack(anchor='center', pady=40)
        # Making labels and entries for the hours, minutes, and seconds.
        self.hours_label = tk.Label(self.countdown_frame, text="Hours")
        self.hours_entry = tk.Entry(self.countdown_frame, width=7)
        self.minutes_label = tk.Label(self.countdown_frame, text="Minutes")
        self.minutes_entry = tk.Entry(self.countdown_frame, width=7)
        self.seconds_label = tk.Label(self.countdown_frame, text="Seconds")
        self.seconds_entry = tk.Entry(self.countdown_frame, width=7)
        # Positioning them so they can be beside each other.
        self.hours_label.grid(row=0, column=0, padx=5)
        self.hours_entry.grid(row=1, column=0, padx=5)
        self.minutes_label.grid(row=0, column=1, padx=5)
        self.minutes_entry.grid(row=1, column=1, padx=5)
        self.seconds_label.grid(row=0, column=2, padx=5)
        self.seconds_entry.grid(row=1, column=2, padx=5)
        # Initializing an entry for each of them by zero.
        self.hours_entry.insert(0, '0')
        self.minutes_entry.insert(0, '0')
        self.seconds_entry.insert(0, '0')
        # The button which starts the countdown
        self.countdown_button = tk.Button(root, text="Start countdown", command=self.countdown_start)
        self.countdown_button.pack()
        # Initializing the time of the countdown and if it is running or not.
        self.countdown_time = None
        self.countdown_running = False

    # A function that updates the time every second for the display
    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    # Same thing but with date. it updates it by the current date.
    def update_date(self):
        now = datetime.now()
        current_date = now.strftime("%A, %B %d, %Y")
        self.date_label.config(text=current_date)

    # This is for when the timer button is clicked. If it was not running then it calls the start function else the stop one.
    def toggle_timer(self):
        if self.timer_running:
            self.stop_timer()
        else:
            self.start_timer()

    # The function that starts the timer and turns the button into red when called and state the starting time.
    def start_timer(self):
        self.timer_running = True
        self.timer_start_time = datetime.now()
        self.timer_button.config(text="Stop Timer", bg="red")
        self.update_timer()

    # Function which stops the timer.
    def stop_timer(self):
        self.timer_running = False
        end_time = datetime.now()
        duration = end_time - self.timer_start_time
        self.timer_button.config(text="Start Timer", bg="green")
        self.timer_count.config(text="00:00")
        self.save_file(self.timer_start_time, end_time, duration)

    # This function is to update the timer counter. it calculates the time passed and display it in means of min and sec.
    def update_timer(self):
        if self.timer_running:
            elapsed_time = datetime.now() - self.timer_start_time
            minutes, seconds = divmod(elapsed_time.seconds, 60)
            self.timer_count.config(text=f"{minutes:02}:{seconds:02}")
            self.root.after(1000, self.update_timer)

    # Saving the timer function. It takes the start, end and duration time and put it in a folder. It creates one of the stated file is not there.
    def save_file(self, start, end, duration):
        # If the user did not specify a path. It will create a txt file and notify them that the file will be stored in the current directory.
        if not self.file_path.get():
            messagebox.showwarning("File Path", "No file has been chosen. The file will be stored in the current folder.")
            self.file_path.set("timer.txt")
        with open(self.file_path.get(), 'a') as file:
            file.write(f"Start: {start}, End: {end}, Duration: {duration}\n")

    # Function to select the file path
    def select_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path.set(file_path)

    # Starting the countdown and checking if one of the inputs are invalid.
    def countdown_start(self):
        try:
            hours = int(self.hours_entry.get())
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())
            self.countdown_time = (hours * 60 * 60) + (minutes * 60) + seconds
            if self.countdown_time <= 0:
                messagebox.showwarning("Countdown", "Please enter a valid countdown time.")
                return
            if not self.countdown_running:
                self.countdown_running = True
                threading.Thread(target=self.countdown_run).start()
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numbers for hours, minutes and seconds.")

    # Running the countdown until the time is zero.
    def countdown_run(self):
        while self.countdown_time > 0 and self.countdown_running:
            hours, remainder = divmod(self.countdown_time, 3600)
            mins, secs = divmod(self.countdown_time, 60)
            self.hours_entry.delete(0, tk.END)
            self.hours_entry.insert(0, str(hours))
            self.minutes_entry.delete(0, tk.END)
            self.minutes_entry.insert(0, str(mins))
            self.seconds_entry.delete(0, tk.END)
            self.seconds_entry.insert(0, str(secs))
            time.sleep(1)
            self.countdown_time -= 1
        if self.countdown_running:
            messagebox.showinfo("Countdown", "Countdown has ended!")
        self.countdown_running = False


root = tk.Tk()
clock = GUIclock(root)
root.mainloop()
