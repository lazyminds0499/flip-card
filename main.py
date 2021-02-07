from tkinter import *
import pandas
from random import choice
BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
# ------------------------------ BUTTON FUNCTIONALITY -------------------#
try:
    data = pandas.read_csv("words_to_learn.csv")
    to_learn = data.to_dict(orient="records")
except FileNotFoundError:
    data = pandas.read_csv("french_words.csv")
# french_words = [value.French for key, value in data.iterrows()]
    to_learn = data.to_dict(orient="records")

# ----------------------------- REMOVING KNOWN CARD --------------------- #


def known_card():
    to_learn.remove(current_word)
    print(len(to_learn))
    unknown_card()


def unknown_card():
    global current_word, window_timer
    window.after_cancel(window_timer)
    canvas.itemconfig(card_img, image=card_front_img)
    current_word = choice(to_learn)
    canvas.itemconfig(card_word, text=current_word["French"], fill="black")
    canvas.itemconfig(card_title, text="French", fill="black")
    window_timer = window.after(3000, flip_card)
    words_to_learn = pandas.DataFrame(to_learn)
    words_to_learn.to_csv("words_to_learn.csv", index=False)
# ---------------------------------- UI SETUP ---------------------------#


window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flash card app")


# ------------------------- FLIPPING CARD -------------------------- #

def flip_card():
    canvas.itemconfig(card_img,  image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_word["English"], fill="white")


# canvas
window_timer = window.after(3000, flip_card)
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="card_front.png")
card_back_img = PhotoImage(file="card_back.png")
card_img = canvas.create_image(400, 265, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# buttons
cross_img = PhotoImage(file="wrong.png")
wrong_button = Button(image=cross_img, highlightthickness=0, command=unknown_card)
check_img = PhotoImage(file="right.png")
check_button = Button(image=check_img, highlightthickness=0, command=known_card)
wrong_button.grid(row=1, column=0)
check_button.grid(row=1, column=1)


unknown_card()

window.mainloop()
