from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
from pygame import mixer

BACKGROUND = "#9BBEC8"
BUTTON_BG = "#427D9D"
HOVER_BUTTON = "#435585"

# insert sound effects using pygame mixer
mixer.init()
click_sound = mixer.Sound("mouse_click.mp3")
intro_sound = mixer.Sound("intro_sound.mp3")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_list = [choice(letters) for _ in range(nr_letters)]
    password_list += [choice(symbols) for _ in range(nr_symbols)]
    password_list += [choice(numbers) for _ in range(nr_numbers)]

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_new_credentials():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    # warning for empty fields
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oooops!", message="Please don't leave empty fields!")

    else:
        #  pop up a message to the user
        is_ok = messagebox.askokcancel(title=website, message="It's ok to save the data?")

        if is_ok:

            try:
                with open("pass_data.json", "r") as file:
                    data = json.load(file)  # read old data(if exist)

            except FileNotFoundError:
                with open("pass_data.json", "w") as file:
                    # save updated data
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open("pass_data.json", "w") as file:
                    # save updated data
                    json.dump(data, file, indent=4)

            finally:
                # clear the entries (not the email entry)
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                messagebox.showinfo(title="Save data", message="The new entries have been saved!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg=BACKGROUND, borderwidth=2, relief="groove")
# Canvas setup to display lock image
canvas = Canvas(window, width=200, height=200, bg=BACKGROUND, highlightthickness=0)
locker_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=locker_image)
pass_text = canvas.create_text(100, 80, text="Password Generator", font=("Courier", 7, "normal"))
canvas.grid(column=1, row=0)
# intro_sound.play()  # play the intro sound
# -------------------------------------Labels Configuration---------------------------------------- #
website_label = Label(text="Website:", bg=BACKGROUND)
website_label.grid(column=0, row=1, sticky=E)

username_label = Label(text="Email/Username:", bg=BACKGROUND)
username_label.grid(column=0, row=2)

password_label = Label(text="Password:", bg=BACKGROUND)
password_label.grid(column=0, row=3, sticky=E)

# -----------------------------------Entries Configuration---------------------------------------- #
website_entry = Entry(width=52)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2)

email_entry = Entry(width=52)
email_entry.insert(0, "dimjim34@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)


# -------------------------------------Buttons Configuration----------------------------------- #
def hovering(e):
    butt = str(e.widget).split(".")[-1]
    if butt == "!button":
        generate_button["bg"] = HOVER_BUTTON
    elif butt == "!button2":
        add_button["bg"] = HOVER_BUTTON


def not_hovering(e):
    butt = str(e.widget).split(".")[-1]
    if butt == "!button":
        generate_button["bg"] = BUTTON_BG
    elif butt == "!button2":
        add_button["bg"] = BUTTON_BG


generate_button = Button(text="Generate Password", activebackground=BACKGROUND, bg=BUTTON_BG, fg="white",
                         command=lambda: [generate_pass(), click_sound.play()])
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=44, activebackground=BACKGROUND, bg=BUTTON_BG, fg="white",
                    command=lambda: [click_sound.play(), save_new_credentials()])
add_button.grid(column=1, row=4, columnspan=2)

# ------------------behaviour of buttons when the cursor is hovering and out-------------------------- #
add_button.bind_all("<Enter>", hovering)
add_button.bind("<Leave>", not_hovering)
generate_button.bind("<Enter>", hovering)
generate_button.bind("<Leave>", not_hovering)

window.mainloop()
