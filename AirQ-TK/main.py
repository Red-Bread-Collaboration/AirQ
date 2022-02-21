# pylint:disable=W0401
from tkinter import *

import AirQ
import shutil

token = "d3c8a559-095a-43d9-a9d1-084fb1486703"
r = AirQ.AirQ(token)

stations = r.get_stations()

lat, lon = 46.938595, 142.758441  # Ours
# lat, lon = 46.944210, 142.725974 # Ленина
# lat, lon = 53.445432, 142.798966 # Оха


stations_distantion = {
    AirQ.haversine(lat, lon, i["DotItem"]["Latitude"], i["DotItem"]["Longitude"]): i
    for i in stations
}

near_station = stations_distantion[min(stations_distantion)]

near_station_id, near_station_name = near_station["MoId"], near_station["PublishNameRu"]

metrics, aqi = r.get_station_data(near_station_id)

warn = False

if aqi <= 3:
    image = "images/green.png"
elif aqi < 7:
    image = "images/yellow.png"
else:
    warn = True
    image = "images/red.png"

shutil.copyfile(image, "images/leaf.png")

root = Tk()
root.geometry("1080x2220")
root.resizable(0, 0)

logo_f = PhotoImage(file="images/logo.png")
leaf_img = PhotoImage(file="images/leaf.png")
info_img = PhotoImage(file="images/info.png")
BG = PhotoImage(file="images/BG.png")
BG2 = PhotoImage(file="images/BG2.png")
BG3 = PhotoImage(file="images/BG3.png")
BG4 = PhotoImage(file="images/BG4.png")


def info():
    newW = Toplevel(root, bg="white", bd=0)

    newW.geometry("1080x2220")
    newW.resizable(0, 0)

    newW.transient(root)
    newW.grab_set()
    newW.overrideredirect(1)

    BG = Label(newW, image=BG4)
    BG.place(x=0, y=0, relwidth=1, relheight=1)

    # Label(
    #     newW,
    #     foreground="#444444",
    #     text="PM2.5 – взвешенные твердые микрочастицы\nи мельчайшие капельки жидкости\n(10 нм - 2,5 мкм в диаметре).",
    #     bg="white",
    # ).place(x=0, y=50)

    # Label(
    #     newW,
    #     foreground="#444444",
    #     text="PM10 - взвешенные крупные твердые\nили жидкие частицы,\nдиаметром 10 мкм или меньше.",
    #     bg="white",
    # ).place(x=0, y=250)

    # Label(
    #     newW,
    #     foreground="#444444",
    #     text="CO - угарный газ.",
    #     bg="white",
    # ).place(x=0, y=450)

    # Label(
    #     newW,
    #     foreground="#444444",
    #     text="NO2 - Оксид азота(IV).",
    #     bg="white",
    # ).place(x=0, y=550)

    # Label(
    #     newW,
    #     foreground="#444444",
    #     text="SO2 - Оксид серы(IV).",
    #     bg="white",
    # ).place(x=0, y=650)

    # Label(
    #     newW,
    #     foreground="#444444",
    #     text="O3 - Озон.",
    #     bg="white",
    # ).place(x=0, y=750)

    # Label(
    #     newW,
    #     foreground="#444444",
    #     text="H2S - Сероводород.",
    #     bg="white",
    # ).place(x=0, y=850)


def openNew():
    newW = Toplevel(root, bg="white", bd=0)

    newW.geometry("1080x2220")
    newW.resizable(0, 0)

    newW.transient(root)
    newW.grab_set()
    newW.overrideredirect(1)

    if not warn:

        BG_label = Label(newW, image=BG2)
        BG_label.place(x=0, y=0, relwidth=1, relheight=1)

        info_btn = Button(
            newW, image=info_img, bg="white", highlightthickness=0, bd=0, command=info
        )

        info_btn.place(x=50, y=1050)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{near_station_id} - {near_station_name}",
            bg="white",
        ).place(x=357, y=968)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{aqi}\nAQI",
            bg="#acf99d",
            font=("Oswald", 8),
        ).place(x=570, y=691)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{metrics['Temperature']}",
            bg="white",
            font=("Oswald", 5),
        ).place(x=355, y=843)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{metrics['Pressure']}",
            bg="white",
            font=("Oswald", 5),
        ).place(x=516, y=843)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{metrics['Humidity']}",
            bg="white",
            font=("Oswald", 5),
        ).place(x=785, y=843)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{metrics['PM2.5']}",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=385, y=1108)

        Label(
            newW,
            foreground="#536250",
            text="< 25 мкг/м³",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=671, y=1108)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{metrics['PM10']}",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=375, y=1245)

        Label(
            newW,
            foreground="#536250",
            text="< 50 мкг/м³",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=671, y=1245)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{metrics['CO']}",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=335, y=1382)

        Label(
            newW,
            foreground="#536250",
            text="< 20000 мкг/м³",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=600, y=1382)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{metrics['NO2']}",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=345, y=1518)

        Label(
            newW,
            foreground="#536250",
            text="< 400 мкг/м³",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=648, y=1518)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{metrics['SO2']}",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=355, y=1658)

        Label(
            newW,
            foreground="#536250",
            text="< 10000 мкг/м³",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=600, y=1658)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{metrics['O3']}",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=345, y=1793)

        Label(
            newW,
            foreground="#536250",
            text="< 160 мкг/м³",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=648, y=1793)

        Label(
            newW,
            foreground="#6aa95e",
            text=f"{metrics['H2S']}",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=355, y=1929)

        Label(
            newW,
            foreground="#536250",
            text="< 8 мкг/м³",
            bg="#d0f4c4",
            font=("Oswald", 8),
        ).place(x=700, y=1929)

    else:
        BG_label = Label(newW, image=BG3)
        BG_label.place(x=0, y=0, relwidth=1, relheight=1)

        info_btn = Button(
            newW, image=info_img, bg="white", highlightthickness=0, bd=0, command=info
        )

        info_btn.place(x=50, y=1050)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{near_station_id} - {near_station_name}",
            bg="white",
        ).place(x=357, y=968)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{aqi}\nAQI",
            bg="#f59d9c",
            font=("Oswald", 8),
        ).place(x=570, y=678)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{metrics['Temperature']}",
            bg="white",
            font=("Oswald", 5),
        ).place(x=355, y=827)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{metrics['Pressure']}",
            bg="white",
            font=("Oswald", 5),
        ).place(x=516, y=827)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{metrics['Humidity']}",
            bg="white",
            font=("Oswald", 5),
        ).place(x=767, y=827)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{metrics['PM2.5']}",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=385, y=1098)

        Label(
            newW,
            foreground="#536250",
            text="< 25 мкг/м³",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=671, y=1098)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{metrics['PM10']}",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=375, y=1235)

        Label(
            newW,
            foreground="#536250",
            text="< 50 мкг/м³",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=671, y=1235)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{metrics['CO']}",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=330, y=1371)

        Label(
            newW,
            foreground="#536250",
            text="< 20000 мкг/м³",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=600, y=1371)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{metrics['NO2']}",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=345, y=1508)

        Label(
            newW,
            foreground="#536250",
            text="< 400 мкг/м³",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=648, y=1508)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{metrics['SO2']}",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=345, y=1645)

        Label(
            newW,
            foreground="#536250",
            text="< 160 мкг/м³",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=648, y=1645)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{metrics['O3']}",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=340, y=1781)

        Label(
            newW,
            foreground="#536250",
            text="< 160 мкг/м³",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=648, y=1781)

        Label(
            newW,
            foreground="#9f282a",
            text=f"{metrics['H2S']}",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=345, y=1918)

        Label(
            newW,
            foreground="#536250",
            text="< 8 мкг/м³",
            bg="#f8c2c2",
            font=("Oswald", 8),
        ).place(x=700, y=1918)


BG_label = Label(root, image=BG)
BG_label.place(x=0, y=0, relwidth=1, relheight=1)

button_qwer = Button(
    root, image=leaf_img, bg="white", highlightthickness=0, bd=0, command=openNew
)
button_qwer.place(x=820, y=35)

root.mainloop()
