from tkinter import *
from PIL import ImageTk, Image
import pygame
import time
import os
import sys

timeout = 120

id = []
type = []
tt = []
next = [[]]
option = [[]]
score = [[]]
temp1 = []
temp2 = []
temp3 = []
image = []
my_score = 0
next_id = "0"
running = True
prev_image = ""
prev_song = ""

# To create executable
# executable_path = os.path.dirname(sys.executable)
# english_file = os.path.join(executable_path, 'ethicalgame_en.txt')
# italian_file = os.path.join(executable_path, 'ethicalgame_it.txt')

with open("ethicalgame_en.txt") as fp:
    for line in fp:
        if "ID:" in line:
            id.append(line.split(":")[1].replace("\n", ""))
        elif "Type:" in line:
            type.append(line.split(":")[1].replace("\n", ""))
        elif "TT:" in line:
            tt.append(line.split(":")[1].replace("\n", ""))
        elif "Next:" in line:
            temp1.append(line.split("Next:")[1].split("&")[0])
            temp2.append(line.split("Option:")[1].split("&")[0])
            temp3.append(line.split("Score:")[1].replace("\n", ""))
        else:
            next.append(temp1)
            option.append(temp2)
            score.append(temp3)
            temp1 = []
            temp2 = []
            temp3 = []


next.pop(0)
option.pop(0)
score.pop(0)
state = 0
ok = True

button_en = "Continue"
button_it = "Continua"
title_it = "Simulazione Interattiva Testuale – Terremoto a Namila"
title_en = "Interactive Text Simulation - Earthquake in Namila"
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title(title_en)
# icon_path = os.path.join(executable_path, 'icon.ico')
root.iconbitmap("icon.ico")
pygame.mixer.init()

text = ""
top_frame = Frame(root, width=385, height=300)
top_frame.pack(side=TOP)

bottom_frame = Frame(root, width=385, height=460)
bottom_frame.pack(side=BOTTOM)

times = []
tot_time = 0.0
line = 1.0
first_time = True

while ok:
    if first_time:
        intro_widget = Label(top_frame, text=title_en, font=(None, 20, 'bold'))
        intro_widget.pack(padx=20, pady=(80, 10))

        guide_en = "The interactive text simulation you are about to read includes short texts followed by questions." \
                   "The aim of this simulation is to encourage those who work with search and rescue drones in " \
                   "disaster operations, whether researchers or pilots, to reflect on the ethical issues that can " \
                   "emerge in connection with their deployment. The problems presented are actual issues that are " \
                   "described in the literature.\n\n" \
                   "Some useful information:\n" \
                   "1. The story unfolds differently depending on how you answer the questions.\n" \
                   "2. New text appears under the dashed line.\n" \
                   "3. You can navigate within the text using your cursor.\n" \
                   "4. Once you have pressed “Continue” you can no longer change your answer nor return to the text " \
                   "that comes before that question.\n" \
                   "5. None of the answers are completely right or completely wrong. Some of the answers are better, " \
                   "and will earn you a 0 score, others worse, and they will earn you either a -2 or a -4 score, " \
                   "depending on how much worse they are. The best possible score is therefore 0, the worst is -12."

        guide_it = "La simulazione interattiva testuale che ti appresti a leggere è costituita da brevi testi " \
                   "accompagnati da domande. L’obiettivo di questa simulazione è di incoraggiare chi si occupa a vario " \
                   "titolo di droni di soccorso, in particolare nel contesto di disastri o calamità, a riflettere " \
                   "sulle questioni etiche che possono essere legate al loro utilizzo. Le questioni che ti verranno " \
                   "proposte riflettono problemi reali e concreti che sono stati identificati nella letteratura.\n\n" \
                   "Alcune indicazioni utili:\n" \
                   "1. La storia si svolge in maniera diversa a seconda delle risposte che dai alle domande.\n" \
                   "2. Il testo nuovo è riportato ogni volta sotto la riga tratteggiata.\n" \
                   "3. Puoi navigare all’interno del testo utilizzando il touchpad.\n" \
                   "4. Una volta che hai cliccato su “Continua” non puoi più modificare la tua risposta né ritornare " \
                   "al testo che precede quella domanda.\n" \
                   "5. Non ci sono risposte giuste o sbagliate. Ci sono invece risposte migliori, cui viene attribuito " \
                   "un punteggio di 0, e risposte peggiori, cui viene attribuito un punteggio di -2 o -4. Il miglior " \
                   "punteggio possibile è quindi 0, quello peggiore -12."

        txt_widg = Text(top_frame, height=17, width=65, font=(None, 18), wrap=WORD)
        txt_widg.insert(END, guide_en)
        txt_widg.config(state=DISABLED)
        txt_widg.yview_pickplace("end")
        txt_widg.pack(side=TOP, padx=(30, 20), pady=(30, 40))

        var = IntVar()
        button = Button(bottom_frame, text=button_en, padx=10, command=lambda: var.set(1), font=(None, 16))
        button.config(height=2, width=5)
        button.pack(side=TOP, pady=40)

        # print("Waiting for the button to be clicked")
        button.wait_variable(var)
        button.destroy()
        intro_widget.destroy()
        txt_widg.destroy()
        first_time = False
    else:
        start = time.time()
        # try:
        #     pygame.mixer.music.load("music/" + str(id[state]) + ".mp3")
        #     pygame.mixer.music.play(loops=10)
        # except:
        #     pass

        question = False
        if "Question" not in type[state]:
            if text != "":
                text = text + "\n-------------------------------------------------------------------------------------" \
                              "----\n" + tt[state]
            else:
                text = text + tt[state]
        else:
            question = True

        text_widget = Text(top_frame, height=17, width=65, font=(None, 18), wrap=WORD)
        scroll_bar = Scrollbar(top_frame, orient='vertical', command=text_widget.yview)
        scroll_bar.pack(side=LEFT, padx=(30, 0), anchor=NW, pady=32, fill=Y)
        text_widget.insert(END, text)
        text_widget.config(state=DISABLED)
        text_widget.yview_pickplace("end")
        text_widget.pack(side=LEFT, anchor=NW, padx=(0, 20), pady=30)
        try:
            # img_folder = os.path.join(executable_path, 'images/')
            original_image = Image.open("images/" + id[state] + ".jpg")
            prev_image = Image.open("images/" + id[state] + ".jpg")
        except:
            original_image = prev_image
        resized_image = original_image.resize((520, 300), Image.ANTIALIAS)
        final_image = ImageTk.PhotoImage(resized_image)
        img_label = Label(top_frame, image=final_image)
        img_label.pack(side=LEFT, anchor=NE, pady=(55, 0), padx=(0, 30))

        if len(option[state]) == 0:
            break

        null = False
        r = IntVar()
        r.set(0)

        question_widget = Label(bottom_frame, text="", font=(None, 16))
        if question:
            question = tt[state]
            question_widget = Label(bottom_frame, text=question, font=(None, 16), wraplength=1200)
            question_widget.pack(anchor=NW, padx=20, pady=10)

        radio_buttons = []
        for i in range(len(option[state])):
            # print(option[state])
            if "NULL" in option[state][i]:
                null = True
            else:
                print(str(i) + ": " + option[state][i])
                opt = option[state][i]
                split_opt = ""
                j = 0
                for k in range(len(option[state][i])):
                    if k != 0 and k % 160 == 0:
                        j = k
                        count = 0
                        while option[state][i][j] != " " and j < len(option[state][i])-1:
                            count = count + 1
                            split_opt = split_opt + option[state][i][j]
                            j = j + 1
                        split_opt = split_opt + "\n"
                    else:
                        if k > j:
                            split_opt = split_opt + option[state][i][k]

                rb = Radiobutton(bottom_frame, text=split_opt, variable=r, value=i, font=(None, 16))
                radio_buttons.append(rb)
                if i == len(option[state])-1:
                    for rb in radio_buttons:
                        rb.pack(side=TOP, anchor=NW)

        var = IntVar()
        continue_button = Button(bottom_frame, text=button_en, padx=10, command=lambda: var.set(1),
                                 font=(None, 16))
        continue_button.config(height=2, width=5)
        continue_button.pack(side=TOP, pady=30)

        # print("Waiting for the button to be clicked")
        continue_button.wait_variable(var)
        end = time.time()
        elapsed_time = end - start

        times.append((id[state], elapsed_time))
        tot_time = tot_time + elapsed_time
        value = r.get()
        print(r.get())
        # if "NULL" not in option[state][r.get()]:
        #     text = text + "\nHai scelto: " + option[state][r.get()]
        # print("Button clicked!")
        pygame.mixer.music.stop()

        next_id = next[state][int(value)]
        my_score = my_score + int(score[state][int(value)])

        for i in range(len(id)):
            if next_id == id[i]:
                state = i
                found = True
                break
        continue_button.destroy()
        text_widget.destroy()
        scroll_bar.destroy()
        img_label.destroy()
        if question:
            question_widget.destroy()
        for rb in radio_buttons:
            rb.destroy()

finished_msg_en = "Game completed! Your score is: "
finished_msg_it = "Gioco completato! Il tuo punteggio è: "
finished_msg = finished_msg_en + str(my_score)
finished = Label(bottom_frame, text=finished_msg, font=(None, 16))
finished.pack(padx=20, pady=(40, 10))
print("\n" + finished_msg + "\n")

print("Time for each state: ", times)
print("Total time: ", tot_time)
exit_button_en = "Exit"
exit_button_it = "Esci"
quit_button = Button(bottom_frame, text=exit_button_en, command=root.quit, font=(None, 16))
quit_button.config(height=2, width=5)
quit_button.pack(padx=10, pady=20)

root.mainloop()
