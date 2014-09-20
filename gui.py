from Tkinter import *
from selectPersonWindow import personSelectWindow
from adminWindowBase import adminWindowBase
from people import people
from datetime import datetime,timedelta
from multiprocessing import Process

#Really simple window that simply starts the cascade of more windows.
#this is the only non-opject window

global root
root=Tk()

def exitProgram(ignore=""):root.quit()
def ignoringAnything(ignore='yes'):pass
root.bind("<Control-q>",exitProgram)
root.protocol("WM_DELETE_WINDOW",ignoringAnything)
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)

#body
buttonPerson=Button(root,text="Person Selection")
buttonPerson.grid(row=0,column=0,sticky=N+S+E+W,padx=3,pady=3)
entryAdmin=Entry(root,show="*")
entryAdmin.grid(row=1,column=0)
buttonAdmin=Button(root,text="Admin Window")
buttonAdmin.grid(row=2,column=0)

#no password
def selectPerson(ignore=""):
	personWindow=personSelectWindow(root)
buttonPerson.config(command=selectPerson)

#Admin Takes a Password - will be changed to use a password from a file
def administration(ignore=""):
	if entryAdmin.get()=="37and34":
		entryAdmin.delete(0,END)
		adminWindow=adminWindowBase(root)
buttonAdmin.config(command=administration)

def dynamicResizing(ignore=''):
	factor=buttonPerson.winfo_height()/2
	if factor>buttonPerson.winfo_width()/10:factor=buttonPerson.winfo_width()/10
	buttonPerson.config(font=("Ariel",factor))
root.bind("<Configure>",dynamicResizing)

def checkForOverdue(ignore=""):
	now=datetime.today() #gives back the time now equivilent
	print now
	ppp=people()
	for person in ppp:
		if len(ppp.overdueItems(person))==0:continue #is first so that we dont waste cycles making the datetime if not needed
		last=datetime.strptime(person['emailedLast'],"%m-%d-%Y-%H-%M") #the time the person was emailed last
		print person['name'],'has overdue items'
		if (now-last)>timedelta(hours=4): #if it has been more than 4 hours
			print '\tEmailing',person["name"]
			ppp.emailPersonOverdue(person) #send the overdue email
			person['emailedLast']=datetime.strftime(now,"%m-%d-%Y-%H-%M") #update the last time emailed to now
			ppp.modify_person_noUpdate(person)#dont waste cycles updating the list from the HDD since this is a temporary list

	#repeat the timed check
	root.after(1000*60*5,checkForOverdue) #1000ms*60s*5mins  so basicly every 5 mins check for overdue items
#root.after(1000,checkForOverdue)
p=Process(target=checkForOverdue)
p.start()

root.mainloop()
