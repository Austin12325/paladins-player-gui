import PIL.ImageGrab
import pyMeow as pm
import requests
import pyautogui as pag
import os
import sys
from time import sleep,time
from pytesseract import pytesseract
from bs4 import BeautifulSoup

# install, pil, pymeow, requests, pyautogui, pyperclip, pytesseract, bs4

players = []
name_fail= []

heronames = []
classnames = []
kda = []
kda_stats = []
win_rate = []
champ_playtime = []
acc_stats = [] 
all_stats = {}

def resource_path():
    font_file = 'Lato-Black.ttf'
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, f'fonts\{font_file}')

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
    
                
def getchampstats(player):
    sleep(1)
    print('Starting storage on player',player)
    heronames.clear()
    classnames.clear()
    champ_playtime.clear()
    kda.clear()
    kda_stats.clear()
    win_rate.clear()
    acc_stats.clear()
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
def acc_storage(player):
    players.clear()
    all_stats.clear()
    hnames = []
    cnames = []
    ctime = []
    ckda = []
    ckdastats = []
    cwinrate = []
    caacstats = []
 

    
    getchampstats(player)
       

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
    for x in acc_stats:
        caacstats.append(x)

        
    dict = {"champs":hnames,"classes":cnames,"champ_time":ctime,"kda":ckda,"kda_stats":ckdastats,"win%":cwinrate,"acc_info":caacstats}
    all_stats.update({player:dict})

    print("finished storing:",player)  
    players.append(player)
    return player





size = 0
player = 'default_name'
draw = False
tab = 0x09                                          
start_pos = []
end_pos = []
path_to_exe = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pm.overlay_init()

maxfont = 22

maxh = 550 # max height for buttons 
maxw = 320 # max width for buttons to match main window
starty = 340 
fetch = False
pm.load_font(fileName=f"{resource_path()}",fontId=0)
while pm.overlay_loop():
    
    pytesseract.tesseract_cmd = path_to_exe
    


    pm.begin_drawing()
    if pm.key_pressed(tab):
        mousex = str(pm.mouse_position()).split(' ')[1][:-3]
        mousey = str(pm.mouse_position()).split(' ')[3][:-3] 
        value = round((int(mousex) * -1.45)) + maxw
        zerovalue = 0 if value <= 0 else value

        alpha_value = 230 if zerovalue >= 230 else zerovalue
        
        try:
            
            pm.pm.pm.draw_rectangle_lines(int(start_pos[0]),int(start_pos[1]),int(mousex)-int(start_pos[0]),int(mousey)-int(start_pos[1]),color=(pm.get_color('red')),lineThick=2)
            
        except:
            pm.draw_circle_lines(centerX=int(mousex),centerY=int(mousey)+2,radius=5,color=(pm.get_color('red')))

        if len(start_pos) == 0:
            
            if pm.mouse_pressed('left') and pm.mouse_pressed("right"):
                start_pos.append(mousex)
                start_pos.append(mousey)
                print(start_pos)      

        if len(start_pos) >= 1 and len(end_pos) == 0:
            pm.end_drawing()

            if pm.mouse_pressed('left'):
                pass
            else:
                end_pos.append(mousex)                                                                  
                end_pos.append(mousey)
                orig_img = PIL.ImageGrab.grab(bbox=(int(start_pos[0]),int(start_pos[1]),int(mousex),int(mousey)))
                
                # img = PIL.ImageGrab.grab(bbox=(0,0,500,800))

                player = pytesseract.image_to_string(orig_img,config='--psm 10 --oem 3')
                
                try:
                    acc_storage(player[:-1])
                    players.append(player[:-1])
                    fetch = True
                except:
                    try:
                        acc_storage(pag.prompt('Corrected Name','paladins UI',player))
                        fetch = True
                    except:                                                                                                                                                                                                                                                                         
                        print("NAME FAILED")
                                                                                                                                                                                                                                                                                                                                                                                         
                print(all_stats)
                
                
                
                start_pos.clear()
                end_pos.clear() 
        
        if fetch == True:
            
            pm.draw_rectangle(posX=15,
                            posY=300,
                            width=maxw,
                            height=maxh,
                            color={'r': 173, 'g': 204, 'b': 199, 'a': alpha_value})
            
            pm.draw_font(fontId=0,
                    text=f"Name: {players[0]}",
                    posX=20,
                    posY=starty-40,
                    fontSize=maxfont,
                    spacing=0,
                    tint={'r': 0, 'g': 0, 'b': 0, 'a': alpha_value})  
                    
            pm.draw_font(fontId=0,
                        text=f"Region: {all_stats[players[0]]['acc_info'][2]}",
                        posX=20,
                        posY=starty-20,
                        fontSize=maxfont,
                        spacing=0,
                        tint={'r': 0, 'g': 0, 'b': 0, 'a': alpha_value})

            pm.draw_font(fontId=0,
                        text=f"Global Stats: {all_stats[players[0]]['acc_info'][0]}   {all_stats[players[0]]['acc_info'][1]}",
                        posX=20,
                        posY=starty,
                        fontSize=maxfont,
                        spacing=0,
                        tint={'r': 0, 'g': 0, 'b': 0, 'a': alpha_value})

            pm.draw_font(fontId=0,
                         text=f"Last Seen: {all_stats[players[0]]['acc_info'][3]}",
                        posX=20,
                        posY=starty+20,
                        fontSize=maxfont,
                        spacing=0,
                        tint={'r': 0, 'g': 0, 'b': 0, 'a': alpha_value})
                                                    
            c = 0
            space_y = 0                  
            for x in all_stats[players[0]]['champs']:

                    pm.draw_font(fontId=0,
                                text=f"Champion: {all_stats[players[0]]['champs'][c]} {all_stats[players[0]]['classes'][c]} {all_stats[players[0]]['champ_time'][c]}",
                                posX=20,
                                posY=starty+60+(space_y*6),
                                fontSize=maxfont,
                                spacing=0,
                                tint={'r': 0, 'g': 0, 'b': 0, 'a': alpha_value})

                    pm.draw_font(fontId=0,
                                text=f"KDA stats: {all_stats[players[0]]['kda'][c]} {all_stats[players[0]]['win%'][c]}",
                                posX=20,
                                posY=starty+75+(space_y*6),
                                fontSize=maxfont,
                                spacing=0,
                                tint={'r': 0, 'g': 0, 'b': 0, 'a': alpha_value})
                    
                    pm.draw_font(fontId=0,
                                text=f"Stats: {all_stats[players[0]]['kda_stats'][c]}",
                                posX=20,
                                posY=starty+90+(space_y*6),
                                fontSize=maxfont,
                                spacing=0,
                                tint={'r': 0, 'g': 0, 'b': 0, 'a': alpha_value})         
                                                            
                    # draw_text(text='Stats : '+all_stats[player]['kda'][c]+' '+all_stats[player]['win%'][c])
                    # draw_text(text='KDA stats : '+all_stats[player]['kda_stats'][c])
                    space_y += 15
                    c += 1
                                                                                    
    pm.end_drawing()
