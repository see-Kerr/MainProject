import tkinter as tk
from tkinter import filedialog
import numpy as np
import coordsData
import getPixel
import RefAlpha





end,pv=[0,0],[0,0]
Y=15

def Main(content):
    root = tk.Tk()
    root.title("Handwriting Digitization")
    root.geometry("850x700")
    image_path = "C:\\Users\\Piyush\\Desktop\\MainMiniProject-main\\Python_MiniProject\\database\\alphabets_config\\Prateek.jpg"
    coordinates = coordsData.getData(image_path)
    #RefCoordinates = RefAlpha.getData(r"C:\Users\Piyush\Desktop\Code\Python_MiniProject\database\alphabets_config\table.jpg")
    pixels = {
        'a': coordinates[0],
        'b': coordinates[1],
        'c': coordinates[2],
        'd': coordinates[3],
        'e': coordinates[4],
        'f': coordinates[5],
        'g':coordinates[6],
        'h':coordinates[7],
        'i': coordinates[8],
        'j': coordinates[9],
        'k': coordinates[10],
        'l':coordinates[11],
        'm': coordinates[12],
        'n':coordinates[13],
        'o':coordinates[14],
        'p': coordinates[15],
        'q': coordinates[16],
        'r': coordinates[17],
        's': coordinates[18],
        't': coordinates[19],
        'u': coordinates[20],
        'v': coordinates[21],
        'w': coordinates[22],
        'x': coordinates[23],
        'y': coordinates[24],
        'z': coordinates[25],
    }
    #print(pixels['t'])
    refmin,refmax =min(coord[1] for coord in pixels["a"]), max(coord[1] for coord in pixels["a"] )
    ref=(refmin,refmax)
    print(ref)
    print(ref)
    for key in pixels:
        pixels[key]=getPixel.align(pixels[key],ref,key)
    #print(pixels["a"])
    #pixels = getPixel.scaling(pixels,RefCoordinates)
    def draw_coordinates(canvas, coordinates,sx=0.1, sy=0.1, end=[0,0],col='#000000'):
        global Y
        coordinate = coordinates*np.array([sx,sy])
        coordinate = coordinates.tolist()
        #print(coordinates[1])
        for (x, y) in coordinate:
            canvas.create_line(x+end[0]+20,y+40+Y, x+end[0]+21.5, y+41+Y, fill=col,width=0.1,splinesteps=100)
        return coordinate[len(coordinate)-1]
    

    def copy(content):
        global end,pv,Y
        #print(end[1])
        for char in content:
            #print(end[1])
            if(end[1]<-200):
                Y=Y+60
                end=[0,0]
            key = char.lower()
            if key==" ":
                end=[end[0]+20,end[1]]
            elif key=="\n":
                Y=Y+60
                end=[0,0]
            elif key in pixels:
                #print(key)
                pv=draw_coordinates(canvas, pixels[key],0.05,0.05,end)
                end=np.add(pv,end)


    print(content.split(" "))
    root.title("Notebook")
    canvas = tk.Canvas(root, bg='white', width=1100, height=830)
    canvas.pack()

    canvas.pack()
    copy(content)
    

    root.mainloop()