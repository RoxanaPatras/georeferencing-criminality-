
from tkinter import *
from tkinter import messagebox
import pandas as pd


BLUE = "#00ccff"
TEXT = "#003957"
FONT = ("Roboto", 24, "bold")

# ---------------------------- SALVEAZA COORDONATELE -------------------------------

def salveaza_datele():
    # preia datele introduse
    padure = padure_entry.get()
    localitate = localitate_entry.get()
    long = longitudine_entry.get()
    lat = latitudine_entry.get()

    # variabila stocheaza informatiile sub forma de dictionar
    noile_date = {"Name": [f"{padure}"],
                  "Adress": [f"{localitate}"],
                  "Longitude": [f"{long}"],
                  "Latitude": [f"{lat}"]
                  }
    # am transformat datele intr-un DataFrame (df) cu Pandas
    df = pd.DataFrame(noile_date)

    # am introdus alternativa atentionarii in caz ca user-ul nu completeaza campurile, am introdus datele in csv + am sters campurile
    if len(padure) == 0 or len(localitate) == 0 or len(long) == 0 or len(lat) == 0:
        messagebox.showinfo(title="Atenție", message="Completează toate câmpurile!!")
    else:
        este_ok = messagebox.askokcancel(title=localitate, message=f"Ai introdus datele:\n Padure: {padure}\n Localitate: {localitate}\n Longitudine: {long}\n Latitudine: {lat}\n "f"Salvăm?")
        if este_ok:
            df.to_csv("my_csv.csv", mode='a', header=False, index=False)
            padure_entry.delete(0, END)
            localitate_entry.delete(0, END)
            longitudine_entry.delete(0, END)
            latitudine_entry.delete(0, END)

# ---------------------------- INTERFATA PROGRAMULUI ------------------------------- #

window = Tk()
window.title("CoordinateYX")
window.config(padx=15, pady=15, bg=BLUE)
window.grid()

canvas = Canvas(width=410, height=410, bg=BLUE, highlightthickness=0)
imagine = PhotoImage(file = "my_img_logo.png")
canvas.create_image(205, 205, image = imagine)
canvas.grid(column=1, row=1)

# TITLUL
titlul = canvas.create_text(200, 50, text="CoordinateYX", fill=TEXT, font=FONT)


# ETICHETELE

nume_padure = Label(text="Padure:", bg=BLUE, font=("Roboto", 12, "bold"))
nume_padure.grid(column=0, row=2)


nume_localitate = Label(text="Localitate:", bg=BLUE, font=("Roboto", 12, "bold"))
nume_localitate.grid(column=0, row=3)

longitudine = Label(text="Longitudine:", bg=BLUE, font=("Roboto", 12, "bold"))
longitudine.grid(column=0, row=4)

latitudine = Label(text="Latitudine:", bg=BLUE, font=("Roboto", 12, "bold"))
latitudine.grid(column=0, row=5)

#INTRARILE

padure_entry = Entry(width=40)
padure_entry .grid(column=1, row= 2, columnspan=2)
padure_entry .focus()

localitate_entry = Entry(width=40)
localitate_entry .grid(column=1, row= 3, columnspan=2)


longitudine_entry = Entry(width=40)
longitudine_entry.grid(column=1, row=4, columnspan=2)

latitudine_entry = Entry(width=40)
latitudine_entry.grid(column=1, row=5, columnspan=2)

#NUMELE MEU

nume_realizator = Label(text= "© DHL \n Constantin Răchită", bg=BLUE, font=("Roboto", 10))
nume_realizator.grid(column=3, row=6)

# BUTONUL ADD
adauga_coordonate = Button(width=20, text= "Adaugă datele", command=salveaza_datele)
adauga_coordonate.grid(column=1, row=6, columnspan=2)



window.mainloop()