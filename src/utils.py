import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import json
from tkinter import ttk

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


def get_ability_icons(champion):
    """
    Grab the file paths corresponding to the abilities of the selected champion

    List of exceptions in file names (partial - resume check at Gangplank):
    Lee Sin
    Diana
    Elise
    Udyr
    Azir
    Teemo
    Caitlyn   
    Dr. Mundo
    Twisted Fate
    Corki
    Darius
    Anivia
    Ekko
    Rammus
    Cho'gath
    Alistar
    Gangplank

    """
    global ability_icon_paths
    ability_icon_paths = dict()

    # Read champ-specific json
    with open(f"data/dragontail-11.1.1/11.1.1/data/en_US/champion/{champion}.json") as f:
        data = json.load(f)

    P_png = data['data'][champion]['passive']['image']['full']
    Q_png = data['data'][champion]['spells'][0]['image']['full']
    W_png = data['data'][champion]['spells'][1]['image']['full']
    E_png = data['data'][champion]['spells'][2]['image']['full']
    R_png = data['data'][champion]['spells'][3]['image']['full']

    ability_icon_paths['Passive'] = f"data/dragontail-11.1.1/11.1.1/img/passive/{P_png}"
    ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{Q_png}"
    ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{W_png}"
    ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{E_png}"
    ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{R_png}"


    # Group_1 = ['Urgot','Jhin','Kled','Illaoi','Talon','Zac','Zoe','Irelia','Ekko',\
    #     'Quinn','Jinx','Pantheon','Morgana','Lissandra','Nami','Sejuani','Brand',\
    #     'Ziggs','Ornn','Sivir','Zed','Nasus','Yone','Zyra','Lucian','Aatrox','Rengar',\
    #     'Qiyana','Fizz','Cassiopeia','Warwick','Sona','Seraphine','Mordekaiser',\
    #     'Ivern','Neeko','Shen','Yorick','Xayah','Senna','Rakan','Sion','Fiora',\
    #     'Poppy','Kayle','Sett','Swain','Syndra','Camille','Maokai','Volibear',\
    #     'Akali','Malzahar','Tristana','Galio','Bard','Kayn','Lulu','Samira',\
    #     'Evelynn','Annie','Gnar','Heimerdinger','Ezreal','Lillia','Varus','Vi',\
    #     'Taric','Gragas','Soraka','Garen','Sylas','Pyke','Yuumi']

    

    # if champion in Group_1:
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{champion}Q.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{champion}W.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{champion}E.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{champion}R.png"

    # if champion == "Ahri":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{champion}OrbOfDeception.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{champion}FoxFire.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{champion}Seduce.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/{champion}Tumble.png"

    # if champion == "MasterYi":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/AlphaStrike.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/Meditate.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/WujuStyle.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/Highlander.png"

    # if champion == "Aphelios":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/ApheliosQ_ClientTooltipWrapper.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/ApheliosW.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/ApheliosE_ClientTooltipWrapper.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/ApheliosR.png"

    # if champion == "LeeSin":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkQOne.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkWOne.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkEOne.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkRKick.png"
    
    # if champion == "Amumu":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BandageToss.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkWOne.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/Tantrum.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/CurseoftheSadMummy.png"

    # if champion == "LeeSin":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkQOne.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkWOne.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkEOne.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkRKick.png"

    # if champion == "LeeSin":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkQOne.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkWOne.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkEOne.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkRKick.png"

    # if champion == "LeeSin":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkQOne.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkWOne.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkEOne.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkRKick.png"

    # if champion == "LeeSin":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkQOne.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkWOne.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkEOne.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkRKick.png"

    # if champion == "LeeSin":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkQOne.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkWOne.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkEOne.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkRKick.png"

    # if champion == "LeeSin":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkQOne.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkWOne.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkEOne.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkRKick.png"

    # if champion == "LeeSin":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkQOne.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkWOne.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkEOne.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkRKick.png"

    # if champion == "LeeSin":
    #     ability_icon_paths['Q'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkQOne.png"
    #     ability_icon_paths['W'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkWOne.png"
    #     ability_icon_paths['E'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkEOne.png"
    #     ability_icon_paths['R'] = f"data/dragontail-11.1.1/11.1.1/img/spell/BlindMonkRKick.png"




    return ability_icon_paths

def get_cooldowns(champion):
    """
    """
    # Read champ-specific json
    with open(f"data/dragontail-11.1.1/11.1.1/data/en_US/champion/{champion}.json") as f:
      data = json.load(f)
    
    # global cooldown_info
    cooldown_info =dict()

    # Add Q
    Q_name = data['data'][champion]['spells'][0]['name']
    Q_cooldown = str(data['data'][champion]['spells'][0]['cooldown'])
    combined_Q = Q_name + '\n\n' + Q_cooldown
    cooldown_info['Q'] = combined_Q
    
    # Add W
    W_name = data['data'][champion]['spells'][1]['name']
    W_cooldown = str(data['data'][champion]['spells'][1]['cooldown'])
    combined_W = W_name + '\n\n' + W_cooldown
    cooldown_info['W'] = combined_W
    
    # Add E
    E_name = data['data'][champion]['spells'][2]['name']
    E_cooldown = str(data['data'][champion]['spells'][2]['cooldown'])
    combined_E = E_name + '\n\n' + E_cooldown
    cooldown_info['E'] = combined_E
    
    # Add R
    R_name = data['data'][champion]['spells'][3]['name']
    R_cooldown = str(data['data'][champion]['spells'][3]['cooldown'])
    combined_R = R_name + '\n\n' + R_cooldown
    cooldown_info['R'] = combined_R

    return cooldown_info


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
    
    # global champ_info
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