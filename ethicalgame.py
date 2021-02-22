from tkinter import *
from PIL import ImageTk, Image
import pygame

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


def stop():
    pygame.mixer.music.stop()


with open("ethicalgame3.txt") as fp:
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
root.title("Ethical Game")
root.iconbitmap("icon.ico")
pygame.mixer.init()

text = ""
while ok:
    try:
        pygame.mixer.music.load("music/" + str(id[state]) + ".mp3")
        pygame.mixer.music.play(loops=0)
    except:
        pass

    text = text + tt[state] + "\n\n"
    text_widget = Text(root, width=70, font=(None, 16), wrap=WORD)
    scroll_bar = Scrollbar(root, orient='vertical', command=text_widget.yview)
    scroll_bar.pack(anchor=W, fill=Y, side=LEFT, pady=10)
    text_widget.insert(END, text)
    text_widget.config(state=DISABLED)
    text_widget.yview_pickplace("end")
    text_widget.pack(fill=Y, side=LEFT, padx=(0, 10), pady=10)

    try:
        original_image = Image.open("images/" + id[state] + ".jpg")
        prev_image = Image.open("images/" + id[state] + ".jpg")
    except:
        original_image = prev_image
    resized_image = original_image.resize((450, 270), Image.ANTIALIAS)
    final_image = ImageTk.PhotoImage(resized_image)
    img_label = Label(root, image=final_image)
    img_label.pack(padx=20, fill=X, pady=10)

    # print(tt[state])

    if len(option[state]) == 0:
        break

    null = False
    r = IntVar()
    r.set(0)

    radio_buttons = []
    for i in range(len(option[state])):
        if "NULL" in option[state][i]:
            null = True
        else:
            print(str(i) + ": " + option[state][i])
            opt = option[state][i]
            split_opt = ""
            j = 0
            for k in range(len(option[state][i])):
                if k != 0 and k % 55 == 0:
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


            rb = Radiobutton(root, text=split_opt, variable=r, value=i, font=(None, 16))
            radio_buttons.append(rb)
            if i == len(option[state])-1:
                for rb in radio_buttons:
                    rb.pack()

    var = IntVar()
    continue_button = Button(root, text="Continue", padx=10, command=lambda: var.set(1))
    continue_button.pack(padx=10, pady=(20, 40))
    print("Waiting for the button to be clicked")
    continue_button.wait_variable(var)
    value = r.get()
    print(r.get())
    print("Button clicked!")

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
    for rb in radio_buttons:
        rb.destroy()

finished_msg = "Game finished! Your score is: " + str(my_score)
finished = Label(root, text=finished_msg, font=(None, 16))
finished.pack(padx=20, pady=(40, 10))
print(finished_msg)

quit_button = Button(root, text="Exit", command=root.quit)
quit_button.pack(padx=10, pady=20)

root.mainloop()
