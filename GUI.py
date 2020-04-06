from tkinter import *

master = Tk()

def startGUI(canvasTitle, canvasWidth, canvasHeight):
    master.title(canvasTitle)
    window = Canvas(master, width = canvasWidth, height = canvasHeight)
    window.pack()

def closeButton():
    button = Button(master, text = "End", width = 10, command=master.destroy)
    button.pack()


if __name__ == '__main__':
    startGUI('Window Title',640, 480)
    closeButton()
    mainloop()