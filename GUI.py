from tkinter import *

def startGUI(canvasTitle, canvasWidth, canvasHeight):
    master = Tk()
    master.title(canvasTitle)
    window = Canvas(master, width = canvasWidth, height = canvasHeight)
    window.pack()

if __name__ == '__main__':
    startGUI('Window Title',640, 480)
    mainloop()