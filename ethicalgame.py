from tkinter import *
from PIL import ImageTk, Image
import pygame
import time

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


with open("ethicalgame_it.txt") as fp:
    for line in fp:
        if "ID:" in line:
            id.append(line.split(':')[1].replace("\n", ""))
        elif "Type:" in line:
            type.append(line.split(':')[1].replace("\n", ""))
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

root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Simulazione Interattiva Testuale – Terremoto a Namila")
root.iconbitmap("icon.ico")
pygame.mixer.init()

text = ""
bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)

times = []
tot_time = 0.0
line = 1.0
first_time = True

while ok:
    if first_time:
        title = "Simulazione Interattiva Testuale – Terremoto a Namila"
        intro_widget = Label(root, text=title, font=(None, 20, 'bold'))
        intro_widget.pack(padx=20, pady=(80, 10))

        guide = "1. La storia si svolge in maniera diversa a seconda delle risposte che dai alle domande.\n" \
                "2. Il testo nuovo è riportato ogni volta sotto la riga di asterischi.\n" \
                "3. Una volta che hai cliccato su “Continua” non puoi più modificare la tua risposta.\n" \
                "4. Ci sono risposte migliori, cui viene attribuito un punteggio di 0, e risposte peggiori, " \
                "cui viene attribuito un punteggio di -2 o -4. Il miglior punteggio possibile è quindi 0.\n" \
                "5. Ti consigliamo di usare le cuffie."
        txt_widg = Text(root, height=15, width=65, font=(None, 18), wrap=WORD)
        txt_widg.insert(END, guide)
        txt_widg.config(state=DISABLED)
        txt_widg.yview_pickplace("end")
        txt_widg.pack(side=TOP, padx=(30, 20), pady=(30, 40))

        var = IntVar()
        button = Button(bottomframe, text="Continua", padx=10, command=lambda: var.set(1), font=(None, 16), bg="#62cf38")
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
        try:
            pygame.mixer.music.load("music/" + str(id[state]) + ".mp3")
            pygame.mixer.music.play(loops=1)
        except:
            pass

        question = False
        if "Question" not in type[state]:
            if text != "":
                text = text + "\n*******************************************************************************" \
                              "**********\n" + tt[state]
            else:
                text = text + tt[state]
        else:
            question = True

        text_widget = Text(root, height=17, width=65, font=(None, 18), wrap=WORD)
        scroll_bar = Scrollbar(root, orient='vertical', command=text_widget.yview)
        # scroll_bar.pack(side=LEFT, anchor=NW, pady=30)
        text_widget.insert(END, text)
        text_widget.config(state=DISABLED)
        text_widget.yview_pickplace("end")
        text_widget.pack(side=LEFT, anchor=NW, padx=(30, 20), pady=(30, 40))
        try:
            original_image = Image.open("images/" + id[state] + ".jpg")
            prev_image = Image.open("images/" + id[state] + ".jpg")
        except:
            original_image = prev_image
        resized_image = original_image.resize((520, 300), Image.ANTIALIAS)
        final_image = ImageTk.PhotoImage(resized_image)
        img_label = Label(root, image=final_image)
        img_label.pack(side=LEFT, anchor=NE, pady=(55, 0), padx=(0, 30))

        if len(option[state]) == 0:
            break

        null = False
        r = IntVar()
        r.set(0)

        question_widget = Label(bottomframe, text="", font=(None, 16))
        if question:
            question = tt[state]
            question_widget = Label(bottomframe, text=question, font=(None, 16))
            question_widget.pack(anchor=NW, padx=20, pady=(40, 10))

        radio_buttons = []
        for i in range(len(option[state])):
            print(option[state])
            if "NULL" in option[state][i]:
                null = True
            else:
                print(str(i) + ": " + option[state][i])
                opt = option[state][i]
                split_opt = ""
                j = 0
                for k in range(len(option[state][i])):
                    if k != 0 and k % 150 == 0:
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

                rb = Radiobutton(bottomframe, text=split_opt, variable=r, value=i, font=(None, 16))
                radio_buttons.append(rb)
                if i == len(option[state])-1:
                    for rb in radio_buttons:
                        rb.pack(side=TOP, anchor=NW)

        var = IntVar()
        continue_button = Button(bottomframe, text="Continua", padx=10, command=lambda: var.set(1),
                                 font=(None, 16), bg="#62cf38")
        continue_button.config(height=2, width=5)
        continue_button.pack(side=TOP, pady=40)

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

finished_msg = "Gioco completato! Il tuo punteggio è: " + str(my_score)
finished = Label(bottomframe, text=finished_msg, font=(None, 16))
finished.pack(padx=20, pady=(40, 10))
print("\n" + finished_msg + "\n")

print("Time for each state: ", times)
print("Total time: ", tot_time)
quit_button = Button(bottomframe, text="Esci", command=root.quit, font=(None, 16), bg="#62cf38")
quit_button.config(height=2, width=5)
quit_button.pack(padx=10, pady=20)

root.mainloop()
