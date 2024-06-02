from tkinter import *
from tkinter import messagebox
from database import *
import customtkinter as ctk
from datetime import datetime, date
import sqlite3 as sq3
from sqlite3 import IntegrityError, ProgrammingError
import requests
import os
import sys
from tkinter import font as tkfont
from pygments import lex
from pygments.lexers.sql import SqlLexer
from pygments.styles import get_style_by_name
from pygments.token import Token

title_img = 'Title.png'
ip_file = 'ipaddress.txt'
port = '80'

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

title_path = os.path.join(application_path, title_img)
ip_file_path = os.path.join(application_path, ip_file)

with open('ipaddress.txt') as ip_file:
    server_ip = ip_file.read()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

url_local = "http://127.0.0.1:80/log"
url_server = f"http://{server_ip}:{port}/log"

time_taken = [0 for i in range(10)]
is_solved = [False for i in range(10)]
temp_text = ["" for i in range(10)]
last_time = None

current_question_index = 0

name = ""
pc_no = 0
start_time = datetime.now()
times = dict

class Window(ctk.CTk):

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.wm_title("Break The Query!")
        self.geometry("600x600")
        self.resizable(False, False)

        self.frames = dict()

        for F in (HomeFrame, DetailsPage, StartPage, QuestionPage, FinalPage):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relheight=1, relwidth=1)
        
        self.show_frame(HomeFrame)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    
class HomeFrame(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        # title_path = os.path.join(os.path.dirname(sys.executable), 'Title.png')

        title_label = ctk.CTkLabel(self, image=PhotoImage(file=title_path), text="", font=("Helvetica", 35, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        description_label = ctk.CTkLabel(self, text="Welcome to the SQL challenge where you'll showcase your skills in breaking down complex queries! Are you ready to break the query?", wraplength=400, font=("Helvetica", 24))
        description_label.place(relx=0.15, rely=0.4, relheight=0.2, relwidth=0.7)

        def start_challenge():
            master.show_frame(DetailsPage)

        start_button = ctk.CTkButton(self, text="START CHALLENGE", font=("Helvetica", 24, "bold"), command=start_challenge)
        start_button.place(relx=0.25, rely=0.7, relheight=0.1, relwidth=0.5)


class DetailsPage(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        title_label = ctk.CTkLabel(self, text="Enter Your Details", font=("Helvetica", 35, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        form = ctk.CTkFrame(self)
        form.place(relx=0.5, rely=0.4, anchor='center')

        ctk.CTkLabel(form, text="Name:", font=("Helvetica", 18, "bold")).grid(row=0, column=0, padx = (10, 10), pady=(10, 10))
        ctk.CTkLabel(form, text="PC No.:", font=("Helvetica", 18)).grid(row=1, column=0, padx = (10, 10), pady=(0, 10))

        name_input = ctk.CTkEntry(form)
        name_input.grid(row=0, column=1, padx = (10, 10), pady=(10, 10))

        pc_no_input = ctk.CTkEntry(form)
        pc_no_input.grid(row=1, column=1, padx = (10, 10), pady=(0, 10))

        def submit_info():
            player_name = name_input.get()
            try:
                pc_number = int(pc_no_input.get())
                if pc_number < 0 or  pc_number > 20:
                    raise ValueError('Invalid PC Number! Please enter a number between 1 and 20')
            except Exception as e:
                messagebox.showerror('Error', 'Invalid PC Number! Please enter a valid number.')
                return None
            if player_name == "":
                messagebox.showerror("No Name", "Please Enter Your Name")
                return None
            for i in "!\"#$%&'()*+,-./:;<=>?[\\]^`{|}~":
                if i in player_name:
                    messagebox.showerror("Name Error","Names cannot contain any of the following characters")
                    return None
            
            global name
            name = player_name
            global pc_no
            pc_no = pc_number

            master.show_frame(StartPage)


        submit_button = ctk.CTkButton(self, text="SUBMIT DETAILS", font=("Helvetica", 24, "bold"), command=submit_info)
        submit_button.place(relx=0.25, rely=0.7, relheight=0.1, relwidth=0.5)




class StartPage(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        title_label = ctk.CTkLabel(self, text="Do You Want To Start The Game?", wraplength=400,font=("Helvetica", 35, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        def start():
            print(pc_no)
            print(name)

            global last_time
            last_time = datetime.now()

            master.show_frame(QuestionPage)

        start_button = ctk.CTkButton(self, text="START GAME", font=("Helvetica", 24, "bold"), command=start)
        start_button.place(relx=0.25, rely=0.7, relheight=0.1, relwidth=0.5)


class QuestionPage(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        questions = get_questions()
        # idx = 0

        frame = ctk.CTkFrame(self)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        qnovar = ctk.StringVar()
        qno_label = ctk.CTkLabel(frame, textvariable=qnovar, font=("Helvetica", 15), wraplength=380)
        qno_label.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.05)

        # Question label
        question_var = ctk.StringVar()
        question_label = ctk.CTkLabel(frame, textvariable=question_var, font=("Helvetica", 15), wraplength=380)
        question_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.25)

        query_entry = ctk.CTkTextbox(master=frame, wrap=WORD)
        query_entry.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.3)
        

        status_var = ctk.StringVar()
        status_window = ctk.CTkLabel(frame, textvariable=status_var, font=("Helvetica", 15), wraplength=380)
        status_window.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.1)
        

        def add_time():
            global current_question_index
            global last_time
            global time_taken
            global temp_text

            current_time = datetime.now()
            time_taken[current_question_index] += (current_time-last_time).total_seconds()
            last_time = current_time

            temp_text[current_question_index] = query_entry.get('1.0', 'end-0c')


        def check_query_():
            global is_solved

            user_input = query_entry.get('1.0', 'end-0c')
            result = check_query(questions[current_question_index], user_input)
            if result['match'] is True:
                add_time()
                data = {
                    "name": name,
                    "pc_number": pc_no,
                    "question_number": current_question_index,
                    "time_taken": time_taken[current_question_index]
                }
                try:
                    requests.post(url_server, json=data)
                except Exception:
                    try:
                        requests.post(url_local, json=data)
                    except Exception:
                        messagebox.showerror('Error', 'Http Connection Error!')
                        return None
                
                is_solved[current_question_index] = 1
                execute_button.configure(state=DISABLED)
            status_var.set(result['response'])


        def show_question(index):
            question_var.set(questions[index]['question'])
            qnovar.set(f"Question: {str(index+1)}")

            query_entry.delete('1.0', END)
            query_entry.insert('1.0', temp_text[current_question_index])

            status_var.set("")

        show_question(current_question_index)

        def next_question():
            global current_question_index

            add_time()

            current_question_index += 1 

            if current_question_index == 9:
                next_button.configure(text="SUBMIT")

            if current_question_index == 10:
                master.show_frame(FinalPage)
                return None
            
            show_question(current_question_index)

            if is_solved[current_question_index] == 1:
                execute_button.configure(state=DISABLED)
                status_var.set("Question Solved")
            else:
                execute_button.configure(state=NORMAL)
            
            prev_button.configure(state=NORMAL)


        def prev_question():
            global current_question_index

            add_time()

            current_question_index -= 1 #(current_question_index-1)
            show_question(current_question_index)

            if is_solved[current_question_index] == 1:
                execute_button.configure(state=DISABLED)
                status_var.set("Question Solved")
            else:
                execute_button.configure(state=NORMAL)
            
            if next_button.cget('text') != "NEXT":
                next_button.configure(text="NEXT")

            if current_question_index == 0:
                prev_button.configure(state=DISABLED)


        # Execute button
        execute_button = ctk.CTkButton(frame, text="TRY", command=check_query_)
        execute_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

        # Next button
        next_button = ctk.CTkButton(frame, text="NEXT", command=next_question, state=NORMAL)#DISABLED
        next_button.place(relx=0.65, rely=0.85, relwidth=0.2, relheight=0.1)
        
        # Previous button
        prev_button = ctk.CTkButton(frame, text="PREV", command=prev_question, state=DISABLED)#DISABLED
        prev_button.place(relx=0.15, rely=0.85, relwidth=0.2, relheight=0.1)

    

class FinalPage(ctk.CTkFrame):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)

        congrats_label = ctk.CTkLabel(self, text="Congratulations!\n\nYou have successfully completed Break the Query!", font=("Helvetica", 16), wraplength=380)
        congrats_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.6)

        # OK button to close the window
        ok_button = ctk.CTkButton(self, text="OK", command=master.destroy)
        ok_button.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.1)
                

app = Window()
app.mainloop()