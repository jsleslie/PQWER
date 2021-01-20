import tkinter as tk
from tkinter import *
from PIL import Image as PIL_image, ImageTk as PIL_imagetk
import json
from tkinter import ttk
from utils import *


#####################
# Helper Functions
#####################

def update_avatar_icon(champion):
    global avatar_icon
    avatar_icon_path = f"data/dragontail-11.1.1/11.1.1/img/champion/{champion}.png"
    # avatar_icon = ImageTk.PhotoImage(Image.open(avatar_icon_path))

    # avatar_icon = avatar_icon._PhotoImage__photo.zoom(1.3)

    image = Image.open(avatar_icon_path)
    image = image.resize((200, 200), Image.ANTIALIAS)
    avatar_icon  = ImageTk.PhotoImage(image=image)

    avatar_label = tk.Label(root, image=avatar_icon, padx=20, pady=20)
    avatar_label.grid(row=0,column=0)

def update_ability_icons(champion):
    """

    """
    champ_ability_icons = get_ability_icons(champion)

    global passive_icon, Q_icon, W_icon, E_icon, R_icon

    # Load images
    passive_icon = ImageTk.PhotoImage(Image.open(champ_ability_icons['Passive']))
    Q_icon = ImageTk.PhotoImage(Image.open(champ_ability_icons['Q']))
    W_icon = ImageTk.PhotoImage(Image.open(champ_ability_icons['W']))
    E_icon = ImageTk.PhotoImage(Image.open(champ_ability_icons['E']))
    R_icon = ImageTk.PhotoImage(Image.open(champ_ability_icons['R']))

    for tab in [tab1, tab2]:
        # Place them inside labels
        passive_label = tk.Label(tab, image=passive_icon)
        Q_label = tk.Label(tab, image=Q_icon)
        W_label = tk.Label(tab, image=W_icon)
        E_label = tk.Label(tab, image=E_icon)
        R_label = tk.Label(tab, image=R_icon)

        # Assign locations to image labels
        passive_label.grid(row=0,column=0)
        Q_label.grid(row=1,column=0)
        W_label.grid(row=2, column=0)
        E_label.grid(row=3, column=0)
        R_label.grid(row=4, column=0)
    
def update_descriptions(champion):
    champ_info = get_PQWER(champion)   

    Passive_text.config(text=champ_info['passive'])
    Q_text.config(text=champ_info['Q'])
    W_text.config(text=champ_info['W'])
    E_text.config(text=champ_info['E'])
    R_text.config(text=champ_info['R'])

def update_cooldowns(champion):
    cooldown_info = get_cooldowns(champion)   

    # Passive_text.config(text=champ_info['passive'])
    Q_cooldown.config(text=cooldown_info['Q'])
    W_cooldown.config(text=cooldown_info['W'])
    E_cooldown.config(text=cooldown_info['E'])
    R_cooldown.config(text=cooldown_info['R'])

# Make default text disappear on click
def delete_text(event):
    global default_text
    if default_text:
        entry1.delete(0, END)
        default_text = False


#####################
# Main Function
#####################

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
    root.title("PQWER Ability Dex")
    tabControl = ttk.Notebook(root)

    # # Try adding background image
    # canvas = Canvas(tabControl,width=900,height=600)
    # bg = ImageTk.PhotoImage(Image.open("data/inhouse/img/bg1.jpg"))

    # canvas.create_image(0,0, anchor=NW, image=bg)
    # canvas.grid(row=0,column=0, rowspan=8, columnspan=4)
    
    # Add an icon
    img = tk.Image("photo", file="data/inhouse/img/PQWER_icon.png")
    root.tk.call('wm','iconphoto', root._w, img)

    entry1 = AutocompleteEntry(
    autocompleteList, root, width=32, matchesFunction=matches)
    entry1.grid(row=0, column=1, padx=10,pady=10)
    entry1.insert(END, 'Enter Champion Name')

    default_text = True
    entry1.bind("<Button-1>", delete_text)

    # Define and embed update functions into the search button
    search_button = tk.Button(root,text="Search", padx=10, \
        command=lambda: [update_descriptions(entry1.get().replace(" ","").replace("'","")),\
                        update_cooldowns(entry1.get().replace(" ","").replace("'","")),\
                        update_ability_icons(entry1.get().replace(" ","").replace("'","")),\
                            update_avatar_icon(entry1.get().replace(" ","").replace("'",""))])
    search_button.grid(row=0,column=2)

    # Add champion avatar
    avatar_icon_path = "data/inhouse/img/PQWER_icon.png"
    # avatar_icon = ImageTk.PhotoImage(Image.open(avatar_icon_path))
    
    # avatar_icon = avatar_icon._PhotoImage__photo.zoom(1.3)

    image = Image.open(avatar_icon_path)
    image = image.resize((200, 200), Image.ANTIALIAS)
    avatar_icon  = ImageTk.PhotoImage(image=image)

    avatar_label = tk.Label(root, image=avatar_icon, padx=20, pady=20)
    avatar_label.grid(row=0,column=0)
   

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    tabControl.add(tab1, text='Descriptions')
    tabControl.add(tab2, text='Cooldowns')
    tabControl.grid(row=1,column=0, columnspan=3)

    # TAB 1
    #-----------
    # Load images
    passive_icon = ImageTk.PhotoImage(Image.open(f"data/inhouse/img/Passive.png"))
    Q_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/Q.png"))
    W_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/W.png"))
    E_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/E.png"))
    R_icon = ImageTk.PhotoImage(Image.open("data/inhouse/img/R.png"))

    # Place them inside labels
    passive_label = tk.Label(tab1, image=passive_icon)
    Q_label = tk.Label(tab1, image=Q_icon)
    W_label = tk.Label(tab1, image=W_icon)
    E_label = tk.Label(tab1, image=E_icon)
    R_label = tk.Label(tab1, image=R_icon)

    # Assign locations to image labels
    passive_label.grid(row=0,column=0)
    Q_label.grid(row=1,column=0)
    W_label.grid(row=2, column=0)
    E_label.grid(row=3, column=0)
    R_label.grid(row=4, column=0)

    # Add text boxes
    Passive_text = tk.Label(tab1, text="", wraplength=600, justify="left")
    Q_text = tk.Label(tab1,text="", wraplength=600, justify="left")
    W_text = tk.Label(tab1,text="", wraplength=600, justify="left")
    E_text = tk.Label(tab1,text="", wraplength=600, justify="left")
    R_text = tk.Label(tab1,text="", wraplength=600, justify="left")

    # Assign locations to text boxes
    Passive_text.grid(row=0, column=1)
    Q_text.grid(row=1, column=1)
    W_text.grid(row=2, column=1)
    E_text.grid(row=3, column=1)
    R_text.grid(row=4, column=1)


    # TAB 2
    #-----------
    # Place them inside labels
    passive_label = tk.Label(tab2, image=passive_icon)
    Q_label = tk.Label(tab2, image=Q_icon)
    W_label = tk.Label(tab2, image=W_icon)
    E_label = tk.Label(tab2, image=E_icon)
    R_label = tk.Label(tab2, image=R_icon)

    # Assign locations to image labels
    passive_label.grid(row=0,column=0)
    Q_label.grid(row=1,column=0)
    W_label.grid(row=2, column=0)
    E_label.grid(row=3, column=0)
    R_label.grid(row=4, column=0)

    # Add text boxes
    Passive_cooldown = tk.Label(tab2, text="", wraplength=600, justify="left")
    Q_cooldown = tk.Label(tab2,text="", wraplength=600, justify="left")
    W_cooldown = tk.Label(tab2,text="", wraplength=600, justify="left")
    E_cooldown = tk.Label(tab2,text="", wraplength=600, justify="left")
    R_cooldown = tk.Label(tab2,text="", wraplength=600, justify="left")
   
   # Assign locations to text boxes
    Passive_cooldown.grid(row=0, column=1)
    Q_cooldown.grid(row=1, column=1)
    W_cooldown.grid(row=2, column=1)
    E_cooldown.grid(row=3, column=1)
    R_cooldown.grid(row=4, column=1)

    # Add exit button
    button_quit = tk.Button(root, text="Exit Program", padx=10, command=root.quit)
    button_quit.grid(row=6,column=1)



    root.mainloop()