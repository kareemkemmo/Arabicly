from ast import Index
from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
cur_word = {}
pressed = False

# -------------------------- Data ---------------------------- #
data = pandas.read_csv("words.csv")
data_list = data.to_dict(orient="records")
try:
    save = pandas.read_csv("words_to_learn.csv")
    words_to_learn = save.to_dict(orient="records")
except FileNotFoundError:
    words_to_learn = data_list.copy()

# -------------------------- Flip Card ----------------------- #
def Flipcard():
    global pressed
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(lang, text="English", fill="white")
    canvas.itemconfig(word, text=f"{cur_word["English"]}", fill="white")
    pressed = False

# -------------------------- Right Button -------------------- #
def Right():
    global cur_word,flip
    window.after_cancel(flip)
    if len(words_to_learn) != 0:
        words_to_learn.remove(cur_word)
        if len(words_to_learn) != 0:
            cur_word = random.choice(words_to_learn)
            canvas.itemconfig(card, image=card_front)
            canvas.itemconfig(lang, text="Arabic", fill="black")
            canvas.itemconfig(word, text=f"{cur_word["Arabic"]}", fill="black")
        pandas.DataFrame(words_to_learn).to_csv("words_to_learn.csv", index=False)
        flip = window.after(3000, func=Flipcard)

# -------------------------- Left Button ---------------------- #
def Left():
    global cur_word,flip
    window.after_cancel(flip)
    if len(words_to_learn) != 0:
        cur_word = random.choice(words_to_learn)
        canvas.itemconfig(card, image=card_front)
        canvas.itemconfig(lang, text="Arabic", fill="black")
        canvas.itemconfig(word, text=f"{cur_word["Arabic"]}", fill="black")
        flip = window.after(3000, func=Flipcard)

# -------------------------- UI Setup ------------------------ #
window = Tk()
window.title("Arabicly")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip = window.after(3000, func=Flipcard)

canvas = Canvas(width=800, height=576, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 276, image=card_front)
lang = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"), fill="black")
word = canvas.create_text(400, 276, text="", font=("Arial", 60, "bold"), fill="black")
canvas.grid(column=0, row=0, columnspan=2)

tick = PhotoImage(file="images/right.png")
button = Button(image=tick, highlightbackground=BACKGROUND_COLOR, command=Right)
button.grid(column=1, row=1)

cross = PhotoImage(file="images/wrong.png")
button = Button(image=cross, highlightbackground=BACKGROUND_COLOR, command=Left)
button.grid(column=0, row=1)

Left()

window.mainloop()