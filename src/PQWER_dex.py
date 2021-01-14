"""
changes made:
    make widgets parent explicitly declared
    Use either with root window or Toplevel
    Bind Return key to selection method
"""

#from tkinter import *
import tkinter as tk
import re
from PIL import ImageTk, Image
import json
from tkinter import ttk



# Helper function extracting ability descriptions from champion json files
def get_PQWER(champion):
    """
    Consumes a champion name in string form and returns a dictionary containing
    the champion's passive, Q, W, E, and R ability names and descriptions 
    
    Parameters:
    -----------
    champion    string
    
    Example:
    -----------
    get_PQWER("Malphite") -> dictionary
    
    """
    
    # Read champ-specific json
    with open(f"data/dragontail-11.1.1/11.1.1/data/en_US/champion/{champion}.json") as f:
      data = json.load(f)
    
    global champ_info
    champ_info =dict()
    
    # Add passive
    passive_name = data['data'][champion]['passive']['name']
    passive_description = data['data'][champion]['passive']['description']
    combined_passive = passive_name + '\n\n' + passive_description
    champ_info['passive'] = combined_passive
    
    # Add Q
    Q_name = data['data'][champion]['spells'][0]['name']
    Q_description = data['data'][champion]['spells'][0]['description']
    combined_Q = Q_name + '\n\n' + Q_description
    champ_info['Q'] = combined_Q
    
    # Add W
    W_name = data['data'][champion]['spells'][1]['name']
    W_description = data['data'][champion]['spells'][1]['description']
    combined_W = W_name + '\n\n' + W_description
    champ_info['W'] = combined_W
    
    # Add E
    E_name = data['data'][champion]['spells'][2]['name']
    E_description = data['data'][champion]['spells'][2]['description']
    combined_E = E_name + '\n\n' + E_description
    champ_info['E'] = combined_E
    
    # Add R
    R_name = data['data'][champion]['spells'][3]['name']
    R_description = data['data'][champion]['spells'][3]['description']
    combined_R = R_name + '\n\n' + R_description
    champ_info['R'] = combined_R

    return champ_info
    
def update_descriptions(champion):
    champ_info = get_PQWER(champion)   

    Passive_text.config(text=champ_info['passive'])
    Q_text.config(text=champ_info['Q'])
    W_text.config(text=champ_info['W'])
    E_text.config(text=champ_info['E'])
    R_text.config(text=champ_info['R'])



# Class adopted from samuelkazeem/tkinter-autocomplete-listbox.py
class AutocompleteEntry(tk.Entry):
    def __init__(self, autocompleteList, *args, **kwargs):

        self.listboxLength = 0
        self.parent = args[0]

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile(
                    '.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)

            self.matchesFunction = matches

        # Custom return function
        if 'returnFunction' in kwargs:
            self.returnFunction = kwargs['returnFunction']
            del kwargs['returnFunction']
        else:
            def selectedValue(value):
                print(value)
            self.returnFunction = selectedValue

        tk.Entry.__init__(self, *args, **kwargs)
        #super().__init__(*args, **kwargs)
        self.focus()

        self.autocompleteList = autocompleteList

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        self.bind("<Return>", self.selection)
        self.bind("<Escape>", self.deleteListbox)

        self.listboxUp = False

    def deleteListbox(self, event=None):
        if self.listboxUp:
            self.listbox.destroy()
            self.listboxUp = False

    def select(self, event=None):
        if self.listboxUp:
            index = self.listbox.curselection()[0]
            value = self.listbox.get(tk.ACTIVE)
            self.listbox.destroy()
            self.listboxUp = False
            self.delete(0, tk.END)
            self.insert(tk.END, value)
            self.returnFunction(value)

    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.deleteListbox()
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listboxLength = len(words)
                    self.listbox = tk.Listbox(self.parent,
                        width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(
                        x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True
                else:
                    self.listboxLength = len(words)
                    self.listbox.config(height=self.listboxLength)

                self.listbox.delete(0, tk.END)
                for w in words:
                    self.listbox.insert(tk.END, w)
            else:
                self.deleteListbox()

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(tk.ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(tk.END)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            self.listbox.selection_clear(first=index)
            index = str(int(index) - 1)
            if int(index) == -1:
                index = str(self.listboxLength-1)

            self.listbox.see(index)  # Scroll!
            self.listbox.selection_set(first=index)
            self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '-1'
            else:
                index = self.listbox.curselection()[0]

            if index != tk.END:
                self.listbox.selection_clear(first=index)
                if int(index) == self.listboxLength-1:
                    index = "0"
                else:
                    index = str(int(index)+1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        return [w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w)]


if __name__ == '__main__':
    # Taken from https://www.reddit.com/r/leagueoflegends/comments/cumsa6/list_of_league_of_legends_champion_separated_by/
    autocompleteList = ["Aatrox","Ahri","Akali","Alistar","Amumu","Anivia","Annie","Aphelios","Ashe","Aurelion Sol","Azir",\
        "Bard","Blitzcrank","Brand","Braum","Caitlyn","Camille","Cassiopeia","Cho'Gath","Corki","Darius","Diana","Dr. Mundo","Draven",\
        "Ekko","Elise","Evelynn","Ezreal","Fiddlesticks","Fiora","Fizz","Galio","Gangplank","Garen","Gnar","Gragas","Graves","Hecarim",\
        "Heimerdinger","Illaoi","Irelia","Ivern","Janna","Jarvan IV","Jax","Jayce","Jhin","Jinx","Kai'Sa","Kalista","Karma","Karthus",\
        "Kassadin","Katarina","Kayle","Kayn","Kennen","Kha'Zix","Kindred","Kled","Kog'Maw","LeBlanc","Lee Sin","Leona","Lillia","Lissandra",\
        "Lucian","Lulu","Lux","Malphite","Malzahar","Maokai","Master Yi","Miss Fortune","Mordekaiser","Morgana","Nami","Nasus","Nautilus",\
        "Neeko","Nidalee","Nocturne","Nunu and Willump","Olaf","Orianna","Ornn","Pantheon","Poppy","Pyke","Qiyana","Quinn","Rakan",\
        "Rammus","Rek'Sai","Rell","Renekton","Rengar","Riven","Rumble","Ryze","Samira","Sejuani","Senna","Seraphine","Sett",\
        "Shaco","Shen","Shyvana","Singed","Sion","Sivir","Skarner","Sona","Soraka","Swain","Sylas","Syndra","Tahm Kench","Taliyah",\
        "Talon","Taric","Teemo","Thresh","Tristana","Trundle","Tryndamere","Twisted Fate","Twitch","Udyr","Urgot","Varus","Vayne","Veigar",\
        "Vel'Koz","Vi","Viktor","Vladimir","Volibear","Warwick","Wukong","Xayah","Xerath","Xin Zhao","Yasuo","Yone","Yorick","Yuumi","Zac","Zed","Ziggs","Zilean","Zoe","Zyra"]

    def matches(fieldValue, acListEntry):
        pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
        return re.match(pattern, acListEntry)

    root = tk.Tk()
    topLevel = tk.Toplevel()
    topLevel.title('League Champions Dex')
    
    #pass either root or toplevel as the second argument to use as entry's parent widget
    entry = AutocompleteEntry(
        autocompleteList, topLevel, width=32, matchesFunction=matches)
    entry.grid(row=0, column=0, columnspan=2)



    search_button = tk.Button(topLevel,text="Search", padx=10, command=lambda: update_descriptions(entry.get()))
    search_button.grid(row=0,column=3)

    # Save dynamic descriptions
    P = tk.StringVar()
    

    # tk.Button(topLevel, text='Python').grid(column=0)
    # tk.Button(topLevel, text='Tkinter').grid(column=0)
    # tk.Button(topLevel, text='Regular Expressions').grid(column=0)
    # tk.Button(topLevel, text='Fixed bugs').grid(column=0)
    # tk.Button(topLevel, text='New features').grid(column=0)
    # tk.Button(topLevel, text='Check code comments').grid(column=0)


    # Load images
    passive_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/Passive.png"))
    Q_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/Q.png"))
    W_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/W.png"))
    E_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/E.png"))
    R_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/R.png"))

    # Place them inside labels
    passive_label = tk.Label(topLevel, image=passive_icon)
    Q_label = tk.Label(topLevel, image=Q_icon)
    W_label = tk.Label(topLevel, image=W_icon)
    E_label = tk.Label(topLevel, image=E_icon)
    R_label = tk.Label(topLevel, image=R_icon)

    # Assign locations to image labels
    passive_label.grid(row=1,column=0, pady=20)
    Q_label.grid(row=2,column=0, pady=20)
    W_label.grid(row=3, column=0, pady=20)
    E_label.grid(row=4, column=0, pady=20)
    R_label.grid(row=5, column=0,pady=20)

    # Add text boxes
    # Passive_text = tk.Label(topLevel, textvariable= P)
    # P.set(champ_info['passive'])
    Passive_text = tk.Label(topLevel, text="Placeholder", wraplength=600, justify="left")
    Q_text = tk.Label(topLevel,text="Placeholder", wraplength=600, justify="left")
    W_text = tk.Label(topLevel,text="Placeholder", wraplength=600, justify="left")
    E_text = tk.Label(topLevel,text="Placeholder", wraplength=600, justify="left")
    R_text = tk.Label(topLevel,text="Placeholder", wraplength=600, justify="left")

    # Assign locations to text boxes
    Passive_text.grid(row=1, column=1, pady=20)
    Q_text.grid(row=2, column=1, pady=20)
    W_text.grid(row=3, column=1, pady=20)
    E_text.grid(row=4, column=1, pady=20)
    R_text.grid(row=5, column=1, pady=20)

    # Add exit button
    button_quit = tk.Button(topLevel, text="Exit Program", command=root.quit)
    button_quit.grid(row=10, column=3)

    root.mainloop()