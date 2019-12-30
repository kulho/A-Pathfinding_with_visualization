from tkinter import *
import time
import sys
import os
import math

class Cube():
    def __init__(self, master, row, col):
        self.row = row
        self.col = col
        self.start = False
        self.end = False
        self.obstacle = False
        self.frame = Frame(master, bg="black", width=15, height=15, highlightcolor="white", highlightthickness=1)
        self.frame.grid(row=row, column=col)
        self.f = 0
        self.h = 0
        self.g = 0
        self.distance = []
        self.parent = None

    def start_point(self):
        self.start = True
        self.frame.config(bg="dark violet", highlightthickness=0)

    def end_point(self):
        self.end = True
        self.frame.config(bg="dark violet", highlightthickness=0)

    def get_g(self, parent):
        self.distance = abs(parent.row - self.row) + abs(parent.col - self.col)
        if self.distance > 1:
            self.g = parent.g + math.sqrt(2)
        else:
            self.g = parent.g + 1

    def get_h(self, end):
        drow = abs(self.row - end[0])
        dcol = abs(self.col - end[1])
        # Manhattan heuristic - always finds the optimal path, but it takes more time
        self.h = drow + dcol
        # Diagonal heuristic - faster, but the path is suboptimal
        # self.h = drow + dcol + (math.sqrt(2) - 1)*min(drow, dcol)

    def get_f(self):
        self.f = self.h + self.g


class MainWindow():

    def __init__(self, master):
        self.master = master
        self.master.title("Pathfinding Visualization")
        self.frame = Frame(self.master)
        self.frame.pack()

        self.start = []
        self.end = []
        self.mousePressed = False
        self.count = 0
        self.visual = BooleanVar()
        self.visual.set(False)
        self.n = 50
        self.openList = []
        self.closedList = []
        self.cubes = [[0 for i in range(self.n)] for j in range(self.n)]
        self.pathLenght = 0

        for i in range(self.n):
            for j in range(self.n):
                self.cubes[i][j] = Cube(self.frame, i, j)

    def setup(self):
        self.cubes[self.start[0]][self.start[1]].start_point()
        self.cubes[self.end[0]][self.end[1]].end_point()

    def selection(self, event):
        row = (root.winfo_pointery() - root.winfo_rooty()) // 15
        col = (root.winfo_pointerx() - root.winfo_rootx()) // 15
        if not self.cubes[row][col].start and not self.cubes[row][col].end:
            self.cubes[row][col].obstacle = True
            self.cubes[row][col].frame.config(bg="white")

    def key_press(self, event):
        if event.char == " ":
            if self.pathfind():
                DoneWindow(True)
            else:
                DoneWindow(False)

    def pathfind(self):
        self.openList.append(self.cubes[self.start[0]][self.start[1]])

        while len(self.openList) > 0:
            # get the square with the lowest value
            currentCube = self.openList[0]
            currentPosition = 0
            for position, cube in enumerate(self.openList):
                if currentCube.f > cube.f:
                    currentCube = cube
                    currentPosition = position
            # remove the square from the open list
            self.openList.pop(currentPosition)
            # add the square to the closed list
            self.closedList.append(currentCube)
            if not currentCube.start and not currentCube.end:
                currentCube.frame.config(bg="red", highlightthickness=0)
                if self.visual.get():
                    root.update()
                    time.sleep(0.001)

            # if the currentSquare is the end, done and backtrack to get the shortest path
            if currentCube.end:
                currentCube = currentCube.parent
                while currentCube is not None:
                    if not currentCube.start:
                        currentCube.frame.config(bg="blue2", highlightthickness=0)
                    currentCube = currentCube.parent
                    if self.visual.get():
                        root.update()
                        time.sleep(0.001)
                return True

            # generate children
            children = []

            for coor in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                # make sure it is inside the main window
                childrow = currentCube.row + coor[0]
                childcol = currentCube.col +coor[1]
                if childrow in range(self.n) and childcol in range(self.n):
                    # make sure it is not obstacle
                    if not self.cubes[childrow][childcol].obstacle:
                        # append the square to children list
                        children.append(self.cubes[childrow][childcol])

            # loop through the children
            for child in children:
                # if the child is on the closed list, ignore it
                if child not in self.closedList:
                    # if the child is not in the open list, add it and compute it's score
                    if child not in self.openList:
                        # calculate scores
                        child.get_g(currentCube)
                        child.get_h(self.end)
                        child.get_f()
                        # add it to open list, update its parent
                        self.openList.append(child)
                        if not child.end:
                            child.frame.config(bg="green2", highlightthickness=0)
                        child.parent = currentCube
                        if self.visual.get():
                            root.update()
                            time.sleep(0.001)
                    else:
                        # if already on the open list, recalculate score
                        last_g = child.g
                        last_h = child.h
                        last_f = child.f
                        child.get_g(currentCube)
                        child.get_h(self.end)
                        child.get_f()
                        # if new score is lower, update its parent, else revert
                        if child.g > last_g:
                            child.f = last_f
                            child.g = last_g
                            child.h = last_h
                        else:
                            child.parent = currentCube
        return False

    # def finalize(self, solution):
    #     DoneWindow(solution)


class DoneWindow():

    def __init__(self, solution):
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title("Finished!")
        self.top.lift()
        self.top.focus_force()

        self.visual = False
        self.frame = Frame(self.top)
        self.frame.pack()
        if solution:
            pathtxt = "Yay, the shortest path has been found! The minimum " \
                      + "distance form the starting point to the end point is " \
                      + str(round(app.cubes[app.end[0]][app.end[1]].g, 2)) + " tiles away."
            self.pathfound = Label(self.frame, wraplength=300, text=pathtxt)
            self.pathfound.grid(row=0, columnspan=2)
        else:
            self.nosolution = Label(self.frame, wraplength=300, text="Make sure you can reach the end point from the starting point.. There is no path between the two.")
            self.nosolution.grid(row=0, columnspan=2)
        self.restartTxt = Label(self.frame, text="Whould you like to restart the simulation?")
        self.restartTxt.grid(row=1, columnspan=2)
        self.yes = Button(self.frame, text="Yes", command=self.restart)
        self.yes.grid(row=2, column=0)
        self.no = Button(self.frame, text="No", command=self.finish)
        self.no.grid(row=2, column=1)

        width = self.top.winfo_reqwidth()
        height = self.top.winfo_reqheight()
        swidth = root.winfo_screenwidth()
        sheight = root.winfo_screenheight()
        x = swidth / 2 - width / 2
        y = sheight / 2 - height / 2
        self.top.geometry('+%d+%d' % (x, y))

    def restart(self):
        os.execv(sys.executable, ['python'] + sys.argv)

    def finish(self):
        sys.exit()


class SetupWindow():

    def __init__(self):
        self.top = Toplevel()
        self.top.grab_set()
        self.top.title("Setup")
        self.top.lift()
        self.top.focus_force()

        self.visual = False
        self.frame = Frame(self.top)
        self.frame.pack()
        self.startLabel = Label(self.frame, text="Starting point coordinates:")
        self.endLabel = Label(self.frame, text="End point coordinates:")
        self.startInput = Entry(self.frame, width=7)
        self.endInput = Entry(self.frame, width=7)
        self.startLabel.grid(row=0, column=0)
        self.startInput.grid(row=0, column=1)
        self.endLabel.grid(row=1, column=0)
        self.endInput.grid(row=1, column=1)
        self.checkbox = Checkbutton(self.frame, text="Process visualization", variable=app.visual)
        self.checkbox.grid(row=2, columnspan=2)
        self.confirm = Button(self.frame, text="Submit", command = self.initialization)
        self.confirm.grid(row=3, columnspan=2)

        width = self.top.winfo_reqwidth()
        height = self.top.winfo_reqheight()
        swidth = root.winfo_screenwidth()
        sheight = root.winfo_screenheight()
        x = swidth / 2 - width / 2
        y = sheight / 2 - height / 2
        self.top.geometry('+%d+%d' % (x, y))


    def initialization(self):
        start = self.startInput.get().split(",")
        app.start = [int(start[0])-1, int(start[1])-1]
        end = self.endInput.get().split(",")
        app.end = [int(end[0])-1, int(end[1])-1]
        app.setup()
        print(app.visual.get())
        self.top.grab_release()
        self.top.destroy()


if __name__ == "__main__":
    root = Tk()

    app = MainWindow(root)
    setup = SetupWindow()

    root.bind("<B1-Motion>", app.selection)
    root.bind("<Key>", app.key_press)

    root.mainloop()