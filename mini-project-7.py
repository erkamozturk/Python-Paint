#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:23:58 2019

@author: erkamozturk
"""

# HINT : FOR 2-D SHAPES PLEASE CHOOSE BOTH FILL AND BORDER COLOR FOR EXAMPLE: OVAL RECTANGLE
# HINT : FOR 1-D SHAPES CHOOSE JUST FILL COLOR ENOUGH

from Tkinter import *
from PIL import Image, ImageTk
from tkColorChooser import askcolor
import time

class MyPaint(Frame):

    def __init__(self, root):

        Frame.__init__(self, root)
        self.root = root
        self.widgets()
        self.geometricDesign()



    def widgets(self):

        self.frame1 = Frame(self.root)
        self.frame2 = Frame(self.root)
        self.frame3 = Frame(self.root)
        self.title = Label(self.frame1, text="My Paint", font="times 15 bold ",
                           bg="orange", fg="white", width=80,height=2)

        image = Image.open("rectangle.png")
        photo = ImageTk.PhotoImage(image)
        self.rectangle = Button(self.frame1, image=photo, command=self.drawRec)
        self.rectangle.image = photo

        image = Image.open("oval.png")
        photo = ImageTk.PhotoImage(image)
        self.oval= Button(self.frame1, image=photo, command=self.drawOval)
        self.oval.image = photo # keep a reference

        image = Image.open("line.png")
        photo = ImageTk.PhotoImage(image)
        self.line= Button(self.frame1, image=photo, command=self.drawLine)
        self.line.image = photo

        image = Image.open("drag.png")
        photo = ImageTk.PhotoImage(image)
        self.move= Button(self.frame1, image=photo, command=self.mover)
        self.move.image = photo

        image = Image.open("eraser.png")
        photo = ImageTk.PhotoImage(image)
        self.eraser= Button(self.frame1, image=photo, command=self.cleaner)
        self.eraser.image = photo

        self.fillColor= Label(self.frame1, bg='green', text='Fill Color:')
        self.fillColor_b= Button(self.frame1, command=self.getfillColor, bg='green')

        self.borderColor= Label(self.frame1, bg='#187023', text='Border Color')
        self.borderColor_b= Button(self.frame1, command=self.getborderColor, bg='red')

        self.weight= Spinbox(self.frame1, width=2, from_=1, to=20)
        self.canvas=Canvas(self.frame2,width=690,height=500, bg='gray',cursor="tcross",)

        # self.drawingCircle = False
        # self.dragging = False

        self.buttonList = [self.rectangle, self.oval, self.line, self.move, self.eraser]
        self.cordinates = {}
        self.i = 1

        self.find = Button(self.frame3, text='Overlapping', command=self.overlapping)

        for i in self.buttonList:
            i.config(relief=RAISED)




    def getfillColor(self):
        color = askcolor()
        self.f_color = color[1]
        self.fillColor_b.config(bg=color[1])

    def getborderColor(self):
        color = askcolor()
        self.b_color = color[1]
        self.borderColor_b.config(bg=color[1])

    def canvasDrag(self, event):
        """Move this item using the pixel coordinates in the event object."""
        # see how far we have moved
        # if self.drawingCircle:
        item = self.canvas.find_closest(event.x, event.y)
        self.canvas.coords(self.circle, self.startx, self.starty, event.x, event.y)

    def canvasDrop(self, event):
        """Drops this item."""
        # if self.drawingCircle:
        #self.drawingCircle = False
        self.canvas.itemconfig(self.circle, fill= self.f_color)  # change color
        if self.i not in self.cordinates:
            self.cordinates[self.i] = self.canvas.coords(self.circle)
        else:
            self.i += 1
            self.cordinates[self.i] = self.canvas.coords(self.circle)


    def drawOval(self):
        for i in self.buttonList:
            i.config(relief=RAISED)
        self.oval.config(relief=SUNKEN)
        self.canvas.bind('<ButtonPress-1>', self.createOval)
        self.canvas.bind('<B1-Motion>', self.canvasDrag)
        self.canvas.bind('<ButtonRelease-1>', self.canvasDrop)

    def createOval(self, event):
        # if self.dragging:
        #     return
        # self.drawingCircle = True
        self.startx, self.starty = event.x, event.y
        item = self.canvas.create_oval(self.startx, self.starty, event.x, event.y, outline=self.b_color, width=self.weight.get())
        self.circle = item

    def drawRec(self):
        for i in self.buttonList:
            i.config(relief=RAISED)
        self.rectangle.config(relief=SUNKEN)
        self.canvas.bind('<ButtonPress-1>', self.createRec)
        self.canvas.bind('<B1-Motion>', self.canvasDrag)
        self.canvas.bind('<ButtonRelease-1>', self.canvasDrop)

    def createRec(self, event):
        # if self.dragging:
        #     return
        # self.drawingCircle = True
        self.startx, self.starty = event.x, event.y
        item = self.canvas.create_rectangle(self.startx, self.starty, event.x, event.y, outline=self.b_color, width=self.weight.get())
        self.circle = item

    def drawLine(self):
        for i in self.buttonList:
            i.config(relief=RAISED)
        self.line.config(relief=SUNKEN)

        self.canvas.bind('<ButtonPress-1>', self.createLine)
        self.canvas.bind('<B1-Motion>', self.canvasDrag)
        self.canvas.bind('<ButtonRelease-1>', self.canvasDrop)

    def createLine(self, event):
        # if self.dragging:
        #     return
        # self.drawingCircle = True
        self.startx, self.starty = event.x, event.y
        item = self.canvas.create_line(self.startx, self.starty, event.x, event.y, width=self.weight.get())
        self.circle = item

    def cleaner(self):
        for i in self.buttonList:
            i.config(relief=RAISED)
        self.eraser.config(relief=SUNKEN)
        self.canvas.bind("<ButtonPress-1>", self.clean)

    def clean(self, event):

        item = self.canvas.find_closest(event.x, event.y)[0]
        self.canvas.delete(item)
    # ==================================================================================================================
    # self.move buttonu na bak
    def mover(self):
        for i in self.buttonList:
            i.config(relief=RAISED)
        self.move.config(relief=SUNKEN)

        self.canvas.bind('<ButtonPress-1>', self.dragStart)
        self.canvas.bind('<B1-Motion>', self.itemDrag)
    def dragStart(self, event):

        """Selects this item for dragging."""
        print 'select'
        # self.dragging = True
        self.dragx, self.dragy = event.x, event.y
        self.dragitem = self.canvas.find_closest(event.x, event.y)
        self.canvas.itemconfig(self.dragitem)  # change color

    def itemDrag(self, event):
        """Move this item using the pixel coordinates in the event object."""
        # see how far we have moved
        # if not self.dragging:
        #     return
        dx = event.x - self.dragx
        dy = event.y - self.dragy
        self.canvas.move(self.dragitem, dx, dy)
        self.dragx, self.dragy = event.x, event.y

    def overlapping(self):
        overlap = 0
        self.list = []

        for i in self.cordinates:
            x1 = self.cordinates[i][0]
            y1 = self.cordinates[i][1]
            x2 = self.cordinates[i][2]
            y2 = self.cordinates[i][3]

            overs = self.canvas.find_overlapping(x1,y1,x2,y2)
            print overs
            if overs not in self.list:
                self.list.append(overs)
                overlap += 1
        print overlap
        print self.list
        if overlap > 0:
            for a in self.list:
                if len(a)>1:
                    y = x = 30
                    time.sleep(0.025)
                    self.canvas.move(a[0], -x, -y)
                    self.canvas.move(a[1], x, y)
                    self.canvas.update()




    def geometricDesign(self):

        self.title.grid(row=0,column=0,columnspan=10)
        self.rectangle.grid(row=1,column=1)
        self.oval.grid(row=1,column=2)
        self.line.grid(row=1,column=3)
        self.move.grid(row=1,column=4)
        self.eraser.grid(row=1,column=5)
        self.fillColor.grid(row=1,column=6)
        self.fillColor_b.grid(row=1,column=7)
        self.borderColor.grid(row=1,column=8)
        self.borderColor_b.grid(row=1,column=9)
        self.weight.grid(row=1,column=10)
        self.canvas.grid(row=0,column=0)
        self.find.grid(row=0,column=0)

        self.frame1.grid(sticky=W)
        self.frame2.grid(sticky=W)
        self.frame3.grid(sticky=W)

def main():

    root = Tk()
    root.title("My Paint")
    root.geometry("690x610+150+100")
    app = MyPaint(root)
    root.mainloop()

if __name__ == '__main__':

    main()




