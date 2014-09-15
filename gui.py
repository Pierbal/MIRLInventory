from Tkinter import *
from selectPersonWindow import personSelectWindow
from adminWindowBase import adminWindowBase

global root
root=Tk()

def exitProgram(ignore=""):root.quit()
root.protocol("WM_DELETE_WINDOW",exitProgram)

#body
buttonPerson=Button(root,text="Person Selection")
buttonPerson.grid(row=0,column=0)
entryAdmin=Entry(root)
entryAdmin.grid(row=1,column=0)
buttonAdmin=Button(root,text="Admin Window")
buttonAdmin.grid(row=2,column=0)

def selectPerson(ignore=""):
	personWindow=personSelectWindow(root)
buttonPerson.config(command=selectPerson)

def administration(ignore=""):
	if entryAdmin.get()=="37and34":adminWindow=adminWindowBase(root)
buttonAdmin.config(command=administration)

root.mainloop()