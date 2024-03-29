from Tkinter import *
from modifyPersonWindow import personWindow
from modifyPersonInfoWindow import modifyPersonInfoWindow
from people import people

#window to select a single person to work with
#is not an admin thing

class personSelectWindow(Toplevel):
	def __init__(self,ROOT):
		#magic
		self.root=ROOT
		Toplevel.__init__(self, self.root)
		self.transient(self.root)
		self.protocol("WM_DELETE_WINDOW",self.delete)
		self.title("Person Selection Window")
		self.result=None

		self.body()
		self.grab_set()

		self.geometry("+%d+%d" % (self.root.winfo_rootx(),self.root.winfo_rooty()))

		#more magic
		self.wait_window(self)


	def body(self):
		#makes the elements of the body and binds them to things
		#tried to keep the columns togeather and goes from top to bottom
		self.elements={}
		self.elements["personList"]=Listbox(self)
		self.elements["personList"].grid(row=0,column=0,rowspan=12,sticky=N+S+W+E)
		self.elements["personList"].focus_set()
		self.elements["personList"].bind("<Button-1>",self.displayPerson_call)
		self.elements["nameLabel"]=Label(self,text="Student Name")
		self.elements["nameLabel"].grid(row=0,column=2)
		self.elements["muidLabel"]=Label(self,text="Student Number")
		self.elements["muidLabel"].grid(row=1,column=2)
		self.elements["roomLabel"]=Label(self,text="Room")
		self.elements["roomLabel"].grid(row=2,column=2)
		self.elements["itemsLabel"]=Label(self,text="Items:\nLine 1\nLine2")
		self.elements["itemsLabel"].grid(row=3,column=2)

		self.elements["buttonAddItems"]=Button(self,text="Add/Remove Items",command=self.modifyPersonItems_call)
		self.elements["buttonAddItems"].grid(row=10,column=2)
		self.elements["buttonChangePerson"]=Button(self,text="Change Information",command=self.modifyPersonInfo_call)
		self.elements["buttonChangePerson"].grid(row=11,column=2)

		self.people=people() #auto populates the person list
		for x in self.people:
			self.elements["personList"].insert(END,x['name'])

		self.elements["personList"].select_set(0)
		self.displayPerson()

		#scollbar
		self.elements['personListScroll']=Scrollbar(self,command=self.elements['personList'].yview)
		self.elements['personListScroll'].grid(row=0,column=1,rowspan=12,sticky=N+S+W)
		self.elements['personList'].config(yscrollcommand=self.elements['personListScroll'].set)

		#allows the dynamic resizing stuff to work
		self.rowconfigure(9,weight=1)
		self.columnconfigure(0,weight=1)
		self.columnconfigure(2,weight=1)
		self.bind("<Configure>",self.dynamicResizing)

	def dynamicResizing(self,ignore=''):
		print self.winfo_width(),self.winfo_height()

	def displayPerson_call(self,ignore=""):self.root.after(1,self.displayPerson)
	def displayPerson(self,ignore=""):
		#gives basic information about the person when clicked on
		index=int(self.elements["personList"].curselection()[0])
		person=self.people[index]
		self.elements["nameLabel"].config(text=person['name'])
		self.elements["muidLabel"].config(text="MUID: "+person["IDNumber"])
		self.elements["roomLabel"].config(text="Room: "+person["room"])

		temp="Items Due:"
		for x in self.people.dueItems(person):
			temp+='\n'+str(x[0])+": "+str(x[1])
		self.elements["itemsLabel"].config(text=temp)

	def modifyPersonInfo_call(self,ignore=""):self.root.after(1,self.modifyPersonInfo)
	def modifyPersonInfo(self,ignore=""):
		#opens a window that modifies some values of the person. Protects some values still such as premium status
		index=int(self.elements["personList"].curselection()[0])
		modifyPersonInfoWindow(self,self.people,index)
		self.elements['personList'].select_set(index)
		self.displayPerson()

	def modifyPersonItems_call(self,ignore=""):self.root.after(1,self.modifyPersonItems)
	def modifyPersonItems(self,ignore=""):
		#opens a window to add or remove items for a person
		index=int(self.elements["personList"].curselection()[0])
		personWindow(self,self.people,index)
		self.elements['personList'].select_set(index)
		self.displayPerson()

	def delete(self,ignore=""):
		self.grab_release()
		self.destroy()
