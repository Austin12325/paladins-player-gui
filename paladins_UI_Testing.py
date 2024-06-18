import requests
import mss
import pyMeow as pm
from bs4 import BeautifulSoup
from pytesseract import pytesseract
from time import sleep
import cv2
path_to_exe = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
run_path = r"C:\Users\Austin\Documents\Python\Projects\Web_stuff"
# image = r"C:\Users\Austin\Documents\Python\Projects\Web_stuff\in.png"
name_fail= []
players = []




heronames = []
classnames = []
kda = []
kda_stats = []
win_rate = []
champ_playtime = []
acc_stats = [] 
all_stats = {}


def playerloc(index):
    c1w = 450-290
    c1h = 385-360

    c2w = 1625-1435
    c2h = c1h
    player1_loc = {"top": 365, "left": 295, "width": c1w, "height": c1h}
    player2_loc = {"top": 435, "left": 295, "width": c1w, "height": c1h}
    player3_loc = {"top": 506, "left": 295, "width": c1w, "height": c1h}
    player4_loc = {"top": 575, "left": 295, "width": c1w, "height": c1h}
    player5_loc = {"top": 644, "left": 295, "width": c1w, "height": c1h}

    player6_loc = {"top": 362, "left": 1435, "width": c2w, "height": c2h}
    player7_loc = {"top": 433, "left": 1435, "width": c2w, "height": c2h}
    player8_loc = {"top": 502, "left": 1435, "width": c2w, "height": c2h}
    player9_loc = {"top": 574, "left": 1435, "width": c2w, "height": c2h}
    player10_loc = {"top": 643, "left": 1435, "width": c2w, "height": c2h}
    if index == 1:
        return player1_loc
    if index == 2:
        return player2_loc
    if index == 3:
        return player3_loc
    if index == 4:
        return player4_loc
    if index == 5:
        return player5_loc
    if index == 6:
        return player6_loc
    if index == 7:
        return player7_loc
    if index == 8:
        return player8_loc
    if index == 9:
        return player9_loc
    if index == 10:
        return player10_loc
    
def screenshot(index):
    with mss.mss() as sct:

        output = run_path+'\player'+str(index)+'.png'.format(**playerloc(index))
        sct.cls_image
        sct_img = sct.grab(playerloc(index))
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        return output

def getname(psm):
    for x in range(10):

        img = cv2.imread((screenshot(x+1)))
        convertimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        pytesseract.tesseract_cmd = path_to_exe
        text = pytesseract.image_to_string(convertimg,config='--psm '+str(psm)+' --oem 3')
        print(text)
        # for x in text:
        #     if x.isspace() and x[0] != 'W':
        #         print(text,'with space no W')
        players.append(text[:-1])


    c = 0
    # remove battlepass W that gets detected
    for x in players:
        print(x[0])
        if x[0] == 'W' or 'Y':
            if x[1] == ' ':
                print("FOUND SPACE 1",x)
                players[c]=x[2:]
            if x[2] == ' ':
                print("FOUND SPACE 2",x)
                players[c]=x[3:]                        
        c += 1
    # Remove space from names
    c = 0
    for x in players:
        for y in x:
            if y.isspace():
                players[c] = x.replace(' ','_')
                print(x.replace(' ','_'))
        c += 1
    
    print(players)

def getlink(player):
    searchterm = player
    r = requests.get('https://paladins.guru/search?term='+searchterm+'&type=Player')
    page = BeautifulSoup(r.content, 'html.parser')
    count = 0
    for x in page.find_all('a'):
        if str(x.get("href")).startswith("/profile"):
            while count < 1:
                count += 1
                return str("https://paladins.guru"+x.get("href"))
    sleep(1)
                
def getchampstats(player):
    c = 0
    sleep(1)
    print('Starting storage on player',player)
    heronames.clear()
    classnames.clear()
    champ_playtime.clear()
    kda.clear()
    kda_stats.clear()
    win_rate.clear()
    link = getlink(player)
    page = BeautifulSoup(requests.get(link).content,'html.parser')
    
    
        

    #Find misc stats, if I remember correctly this was the profile wide KD/W-l

    for x in page.find_all('div', attrs={"class":"ptw__val"}):
        
        string = str(x).split("</div>")[0]
        string1 = str(string).split('<div>'[-1])[-1]
        acc_stats.append(string1)

    # Find champion stats
    for x in page.find_all('div', attrs={"class":"mpc__body"}):

        for y in x:

            string = str(y).split("</div>")[0]
            string1 = str(string).split('<div>'[-1])[-1]
            heronames.append(string1)

            string = str(y).split("</div>")[1]
            string1 = str(string).split('<div>'[-1])[-1]   
            classnames.append(string1)
            
            string = str(y).split("</div>")[4]
            string1 = str(string).split('<div>'[-1])[-1]
            kda.append(string1) 
        

            string = str(y).split("</div>")[5]
            string1 = str(string).split('<div>'[-1])[-1] 
            string2 = str(string1).strip()           
            kda_stats.append(string2)

            string = str(y).split("</div>")[7]
            string1 = str(string).split('<div>'[-1])[-1]             
            win_rate.append(string1)

            string = str(y).split("</div>")[8]
            string1 = str(string).split('<div>'[-1])[-1]            
            champ_playtime.append(string1)

            # print(str(y).split("</div>")[0],'name')
            # print(str(y).split("</div>")[1],'Class')
            # print(str(y).split("</div>")[2])
            # print(str(y).split("</div>")[3])
            # print(str(y).split("</div>")[4],'KDA')
            # print(str(y).split("</div>")[5],"stats")
            # print(str(y).split("</div>")[6])
            # print(str(y).split("</div>")[7],"Win rate")
            # print(str(y).split("</div>")[8],"playtime")
            # print(str(y).split("</div>")[9])
            # print(str(y).split("</div>")[10])
            # print(str(y).split("</div>")[11])

    # Find account stats
    for x in page.find_all('h3'):
        region = str(x).split()
        time = str(x).split(">")
        time1 = str(time[-3]).split("<")
        acc_stats.append(region[2])
        acc_stats.append(time1[0])


# acc_storage is used to store the data I got from getchampstats (from their  paladins guru) in the all_stats dictionary
def acc_storage():
    name_fail.clear()

    for acc in players:
        print(players)
        hnames = []
        cnames = []
        ctime = []
        ckda = []
        ckdastats = []
        cwinrate = []
        try:
            getchampstats(acc)
            name_fail.append('-')
        except:
            print("account grab failed, correct with debug names")
            name_fail.append(acc)

        for x in heronames:
            hnames.append(x)
        for x in classnames:
            cnames.append(x)
        for x in champ_playtime:
            ctime.append(x)
        for x in kda:
            ckda.append(x)
        for x in kda_stats:
            ckdastats.append(x)
        for x in win_rate:
            cwinrate.append(x)

            
        dict = {"champs":hnames,"classes":cnames,"champ_time":ctime,"kda":ckda,"kda_stats":ckdastats,"win%":cwinrate}
        all_stats.update({acc:dict})

        print("finished storing:",acc)  


draw = False
menu_key = 0x2D # I want to make it tab to match paladins but that would block part of your teams talents 
maxh = 25 # max height for buttons 
maxw = 280 # max width for buttons to match main window

pm.overlay_init()

# pm.gui_load_style(r"C:\Users\Austin\Documents\Python\Projects\Web_stuff\styles\default\style_default.txt.rgs")
# I need to figure out how to reset that box's contents, also my font no worky 

index = 0 # index is used to get the proper player info for the champion info box
toggle = 1 # Toggle is used to open and close the debug player names box
while pm.overlay_loop():
    if pm.key_pressed(menu_key):
        draw = not draw
        pm.toggle_mouse()
        sleep(0.1)
    pm.begin_drawing()
    space = 0

    if draw:
        if pm.gui_window_box(5, 5, maxw, 1065,title="Paladins G-uWu-I"):
            draw = not draw
            pm.toggle_mouse()

        if pm.gui_button(5,100,maxw,maxh,text='print player names'):
            print(name_fail)

        if pm.gui_button(5,25,maxw,maxh,text='Scan names'):
            name_fail.clear()
            # if the getname has already been ran, don't run it again, if its ran again it'll overwrite our name_fail list.
            if len(players)<= 9:
                getname(10)

            acc_storage()
            players_str = [x+';' for x in players]
            print(players_str)

            # This block is going to check if we have any errors, if there are 0 errors then clear name_fail once name_fail is cleared allow drop down box to show.
            fail_check = 0
            for playerf in name_fail:
                print(name_fail)
                print('checking name fail')
                if len(playerf) <= 3:
                    print(playerf,'greater than 3')
                    print(len(players),len(name_fail))
                    fail_check += 1
                    print(fail_check)
                if fail_check == 10:
                    print('clearing name fail, no errors left')
                    name_fail.clear()
                    toggle = 0
                    break
                    
        if pm.gui_button(5,50,maxw,maxh,text='Clear'):
            players.clear()
            name_fail.clear()    
            index = 0
        c = 0
        s = 0

        for player in players:
            if toggle == 1:
                if pm.gui_text_box(10,500+s,maxw,maxh,text=player,id=c):
                    players[c] = pm.gui_text_box(10,500+s,maxw,maxh,text=player,id=c)
                if player in name_fail:
                    pm.draw_rectangle_lines(10,500+s,maxw,maxh,color=(pm.get_color('red')),lineThick=1.0)

                    # print(print(len(players)),len(name_fail))

            c+=1 
            s+=25
                
        pm.gui_group_box(10,150,maxw-10,200,text='Account Info')
        pm.gui_group_box(10,355,maxw-10,708,text='Champion Info')

        # make sure index exists
        if index >= 0:
            # make sure all_stats dict is populated
            if len(all_stats) >= 1:
                c = 0
                space_y = 0
                # if any failed names are present do not open the UI, otherwise it will probably crash if you select anything past an errored out name
                if len(name_fail) == 0:
                    try:
                        for x in all_stats[players[index]]['champs']:
                            if toggle == 0:
                                pm.gui_label(15,360+(space_y*6),maxw-10,maxh,text='Champion : '+all_stats[players[index]]['champs'][c]+' '+all_stats[players[index]]['classes'][c]+' '+all_stats[players[index]]['champ_time'][c])
                                pm.gui_label(15,380+(space_y*6),maxw-10,maxh,text='Stats : '+all_stats[players[index]]['kda'][c]+' '+all_stats[players[index]]['win%'][c])
                                pm.gui_label(15,400+(space_y*6),maxw-10,maxh,text='KDA stats : '+all_stats[players[index]]['kda_stats'][c])
                                space_y += 15
                                c += 1
                            
                        index = pm.gui_dropdown_box(5,100,maxw,maxh,text=''.join((str(x)) for x in players_str),id=1)
                    except:
                        pass
    pm.end_drawing()
