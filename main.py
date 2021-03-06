# ALL THE IMPORTS

import requests
import bs4

# IMPORT FOR GUI
import tkinter as tk

# IPORT FOR DISPLAYING NOTIFICATION
import plyer

# IMPORT FOR DISPLAYING DATE AND TIME
import time
import datetime as dt

import threading

# IMPORT FOR DISPLAYING IMAGE ON TKINTER
from PIL import ImageTk,Image

#IMPORT FOR CONNECTION DATABASE
import sqlite3

# MAKING THE CONNECTION TO DATABASE
conn=sqlite3.connect('covid.sqlite')
cur=conn.cursor()
try:
    cur.execute('CREATE TABLE tracker(date TEXT, active INTEGER, cured INTEGER, deaths INTEGER, migrated INTEGER)')
except:
    cur.execute('SELECT * FROM tracker')


# PYTHON PROGRAM

# GLOBAL VARIABLES
stuff=list()
date = dt.datetime.now()
format_date = f"{date:%a, %b %d %Y}"

# FUNCTION TO GET URL
def get_html_data(url):
    data = requests.get(url)
    return data

# FUNCTION TO GET THE CORONA DETAILS
def get_corona_detail_of_india():
    url= "https://www.mohfw.gov.in/"
    html_data = get_html_data(url)

    bs = bs4.BeautifulSoup(html_data.text, 'html.parser') # making of object
    info_div = bs.find("div",class_="site-stats-count").find_all("li")
    all_details = ""
    for block in info_div:
        try:
            count = block.find("strong").get_text()
            stuff.append(count)
            text = block.find("span").get_text()
            all_details = all_details + text +" : " + count + "\n"
        except:
            break
    active=stuff[0]
    cured=stuff[1]
    deaths=stuff[2]
    migrated=stuff[3]
    # print(format_date, active, cured, deaths, migrated)

    cur.execute('SELECT active FROM tracker WHERE cured= ?',(cured, ) )
    row=cur.fetchone()
    if row is None:
        cur.execute('''INSERT OR IGNORE INTO tracker (date, active,cured,deaths,migrated)
            VALUES ( ?, ?, ?, ?, ? )''', ( format_date, active, cured, deaths, migrated, ) )
        conn.commit()
    else:
        yo=row[0]
        if(yo!=int(active)):
            cur.execute('''INSERT OR IGNORE INTO tracker (date, active,cured,deaths,migrated)
                VALUES ( ?, ?, ?, ?, ? )''', ( format_date, active, cured, deaths, migrated, ) )
            conn.commit()

    return all_details

# FUNCTION TO PRODUCE NOTIFICATION
def get_corona_detail_of_india_noti():
    url= "https://www.mohfw.gov.in/"
    html_data = get_html_data(url)

    bs = bs4.BeautifulSoup(html_data.text, 'html.parser') # MAKING OF OBJECT
    info_div = bs.find("div",class_="site-stats-count").find_all("li")
    all_details = ""
    for block in info_div:
        try:
            count = block.find("strong").get_text()
            text = block.find("span").get_text()
            all_details = all_details + text +" : " + count + "\n"
        except:
            break
    return all_details

# FUNCTION TO REFRESH DATA
def refresh():
    newdata=get_corona_detail_of_india()
    print("Refreshing..")
    mainlabel['text'] = newdata

# FUNCTION TO DISPLAY NOTIFICATION
def notify_me():
    while True:
        plyer.notification.notify(
            title="COVID-19 CASES OF INDIA",
            message=get_corona_detail_of_india_noti(),
            timeout=10 # IT WILL SHOW UP FOR 10 SECONDS
        )
        time.sleep(1800) # IT WILL DISPLAY AFTER EVERY 1800 SECOND


# CREATING GUI USING TKINTER
root = tk.Tk()
root.geometry("700x750")
root.title("CORONA TRACKER - INDIA")
f = ("poppins", 25, "bold")
root.configure(bg="white")

# DISPLAYING IMAGE ON WINDOW
canvas = tk.Canvas(root, width = 300, height = 300)
canvas.pack()
img = ImageTk.PhotoImage(Image.open("banner.png"))
canvas.create_image(150, 150, image=img)
canvas.configure(bg="white")

# DISPLAYING TEXT ON WINDOW
mainlabel = tk.Label(root, text=get_corona_detail_of_india(), font=f, bg="white")
mainlabel.pack()

# DISPLAYING REFRESH BUTTON ON WINDOW
rebtn = tk.Button(root, text="Refresh", font=f, command=refresh)
rebtn.pack()

# DISPLAYING DATE
date = dt.datetime.now()
format_date = f"{date:%a, %b %d %Y}"
w = tk.Button(root, text=format_date, fg="black", bg="white", font=f)
w.pack()

# DISPLAYING DYNAMIC TIME
time1 = ''
clock = tk.Label(root, font=f, bg='white')
clock.pack(expand=1)

def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)

tick()

# DISPLAYING NAME BADGE
name= tk.Label(root,text='@RASHANDEEP SINGH', font=("poppins", 7), bg='white')
name.pack()

# CREATE A NEW THREAD
th1 = threading.Thread(target=notify_me)
th1.setDaemon(True)
th1.start()

root.mainloop()
