"""
Jarome Leslie
January 12, 2021
League of Legends Champion Dex 
"""
from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("League Champions Dex")
# root.geometry("600x1800")

# # Add an icon
# img = Image("photo", file="data/dragontail-11.1.1/img/champion/tiles/Malphite_0.jpg")
# root.iconphoto(True, img) 
# # root.tk.call('wm','iconphoto', root._w, img)

# Select champion
e = Entry(root, width=35, borderwidth=5)
e.grid(row=0, column=0, columnspan=2)


search_button = Button(root,text="Search", padx=40, pady =10)
search_button.grid(row=0,column=3)

# Load images
passive_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/Passive.png"))
Q_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/Q.png"))
W_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/W.png"))
E_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/E.png"))
R_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/R.png"))

# Place them inside labels
passive_label = Label(image=passive_icon)
Q_label = Label(image=Q_icon)
W_label = Label(image=W_icon)
E_label = Label(image=E_icon)
R_label = Label(image=R_icon)

# Assign locations to image labels
passive_label.grid(row=1,column=0, pady=20)
Q_label.grid(row=2,column=0, pady=20)
W_label.grid(row=3, column=0, pady=20)
E_label.grid(row=4, column=0, pady=20)
R_label.grid(row=5, column=0,pady=20)

# Add text boxes
Passive_text = Label(root, text="Placeholder")
Q_text = Label(root, text="Placeholder")
W_text = Label(root, text="Placeholder")
E_text = Label(root, text="Placeholder")
R_text = Label(root, text="Placeholder")

# Assign locations to text boxes
Passive_text.grid(row=1, column=1, pady=20)
Q_text.grid(row=2, column=1, pady=20)
W_text.grid(row=3, column=1, pady=20)
E_text.grid(row=4, column=1, pady=20)
R_text.grid(row=5, column=1, pady=20)

# Add exit button
button_quit = Button(root, text="Exit Program", command=root.quit)
button_quit.grid(row=10, column=1)

root.mainloop()