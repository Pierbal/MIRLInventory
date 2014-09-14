from Tkinter import *
from modifyPersonWindow import personWindow
from modifyPersonInfoWindow import modifyPersonInfoWindow
from people import people

class personSelectWindow(Toplevel):
	def __init__(self,ROOT):
		self.root=ROOT
		Toplevel.__init__(self, self.root)
		self.transient(self.root)
		self.protocol("WM_DELETE_WINDOW",self.delete)
		self.title("Person Selection Window")
		self.result=None

		self.rootFrame=Frame(self)
		self.rootFrame.grid(row=0,column=0)
		self.body()
		self.grab_set()

		self.geometry("+%d+%d" % (self.root.winfo_rootx(),self.root.winfo_rooty()))

		self.wait_window(self)


	def body(self):
		self.elements={}
		self.elements["personList"]=Listbox(self.rootFrame)
		self.elements["personList"].grid(row=0,column=0,rowspan=999,sticky=N+S+W)
		self.elements["personList"].focus_set()
		self.elements["personList"].bind("<Button-1>",self.displayPerson_call)
		self.elements["nameLabel"]=Label(self.rootFrame,text="Student Name")
		self.elements["nameLabel"].grid(row=0,column=1)
		self.elements["muidLabel"]=Label(self.rootFrame,text="Student Number")
		self.elements["muidLabel"].grid(row=1,column=1)
		self.elements["roomLabel"]=Label(self.rootFrame,text="Room")
		self.elements["roomLabel"].grid(row=2,column=1)
		self.elements["itemsLabel"]=Label(self.rootFrame,text="Items:\nLine 1\nLine2")
		self.elements["itemsLabel"].grid(row=3,column=1)

		self.elements["buttonAddItems"]=Button(self.rootFrame,text="Add/Remove Items",command=self.modifyPersonItems_call)
		self.elements["buttonAddItems"].grid(row=10,column=1)
		self.elements["buttonChangePerson"]=Button(self.rootFrame,text="Change Information",command=self.modifyPersonInfo_call)
		self.elements["buttonChangePerson"].grid(row=11,column=1)

		self.people=people() #auto populates the person list
		for x in self.people:
			self.elements["personList"].insert(END,x['name'])

		self.elements["personList"].select_set(0)
		self.displayPerson()

	def displayPerson_call(self,ignore=""):self.root.after(1,self.displayPerson)
	def displayPerson(self,ignore=""):
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
		index=int(self.elements["personList"].curselection()[0])
		self.modifyPerson=modifyPersonInfoWindow(self,self.people,index)

	def modifyPersonItems_call(self,ignore=""):self.root.after(1,self.modifyPersonItems)
	def modifyPersonItems(self,ignore=""):
		index=int(self.elements["personList"].curselection()[0])
		self.modifyPerson=personWindow(self,self.people,index)

	def delete(self,ignore=""):
		self.grab_release()
		self.destroy()
