from tkinter import *
import random
from PIL import ImageTk, Image
import os

puzzleOptionList = ["Select puzzle size", "8puzzle", "15puzzle"]
algorithmOptionList = ["Select solving Algoritm","BFS", "DFS", "AStar"]

algorithmChoice = ""

def startGUI(master, canvasTitle, canvasWidth, canvasHeight):
    master.title(canvasTitle)
    Label(text = "choose size of the puzzle and the algorithm to solve it.", font = ("", 25)).pack()
    window = Canvas(master) #, width = canvasWidth, height = canvasHeight)
    window.pack()

def algorithmCallback(selection):
    algorithmChoice = selection

def choosePuzzle(master):
    options = StringVar(master)
    options.set(puzzleOptionList[0])
    opt = OptionMenu(master, options, *puzzleOptionList, command=displayImage)
    opt.config(font=('Helvetica', 15))
    opt.pack(side = BOTTOM)

def displayImage(selection):
    puzzleChoice = selection + ".png"
    img = ImageTk.PhotoImage(Image.open(puzzleChoice))
    panel = Label(master, image = img)
    panel.pack()

def chooseAlgorithm(master):
    variable = StringVar(master)
    variable.set(algorithmOptionList[0])
    opt = OptionMenu(master, variable, *algorithmOptionList, command=algorithmCallback)
    opt.config(font=('Helvetica', 15))
    opt.pack(side = BOTTOM)

def randomize(master):
    Button(master, text = "Randomize", command=NONE).pack(side = BOTTOM)

if __name__ == '__main__':
    master = Tk()
    startGUI(master, 'Sliding Puzzle', 680, 480)
    choosePuzzle(master)
    chooseAlgorithm(master)
    randomize(master)
    mainloop()
