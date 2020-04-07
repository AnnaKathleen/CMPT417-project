from tkinter import *
import random

puzzleOptionList = ["Select puzzle size", "8 - puzzle", "15 - puzzle"]
algorithmOptionList = ["Select solving Algoritm","BFS", "DFS", "AStar"]

def startGUI(master, canvasTitle, canvasWidth, canvasHeight):
    master.title(canvasTitle)
    Label(text = "Sliding puzzle", font = ("", 50)).pack()
    Label(text = "choose size of the puzzle and the algorithm to solve it.", font = ("", 25)).pack()
    window = Canvas(master, width = canvasWidth, height = canvasHeight)
    window.pack()

def choosePuzzle(master):
    variable = StringVar(master)
    variable.set(puzzleOptionList[0])
    opt = OptionMenu(master, variable, *puzzleOptionList)
    opt.config(font=('Helvetica', 15))
    opt.pack(side = RIGHT)

def chooseAlgorithm(master):
    variable = StringVar(master)
    variable.set(algorithmOptionList[0])
    opt = OptionMenu(master, variable, *algorithmOptionList)
    opt.config(font=('Helvetica', 15))
    opt.pack(side = RIGHT)

def randomize(master):
    Button(master, text = "Randomize", command=NONE).pack(side = RIGHT)

if __name__ == '__main__':
    master = Tk()
    startGUI(master, 'Sliding Puzzle', 680, 480)
    choosePuzzle(master)
    chooseAlgorithm(master)
    randomize(master)
    mainloop()
