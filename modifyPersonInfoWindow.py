from Tkinter import *
from people import people

class modifyPersonInfoWindow(Toplevel):
	def __init__(self,ROOT,people,personIndex):
		self.people=people
		self.person=self.people[personIndex]

		self.root=ROOT
		Toplevel.__init__(self, self.root)
		self.transient(self.root)
		self.protocol("WM_DELETE_WINDOW",self.delete)
		self.title("Person Info Modification Window")
		self.result=None

		self.rootFrame=Frame(self)
		self.rootFrame.grid(row=0,column=0)
		self.body()
		self.grab_set()

		self.geometry("+%d+%d" % (self.root.winfo_rootx(),self.root.winfo_rooty()))

		self.wait_window(self)

	def body(self):
		self.people=people()
		self.elements={}
		self.elements["idLabel"]=Label(self.rootFrame,text="MUID: "+self.person["IDNumber"])
		self.elements["idLabel"].grid(row=0,column=0,columnspan=2)

		self.elements["nameLabel"]=Label(self.rootFrame,text="Name:  ")
		self.elements["nameLabel"].grid(row=1,column=0)
		self.elements["nameEntry"]=Entry(self.rootFrame)
		self.elements["nameEntry"].insert(0,self.person["name"])
		self.elements["nameEntry"].grid(row=1,column=1)

		self.elements["roomLabel"]=Label(self.rootFrame,text="Room:  ")
		self.elements["roomLabel"].grid(row=2,column=0)
		self.elements["roomEntry"]=Entry(self.rootFrame)
		self.elements["roomEntry"].insert(0,self.person["room"])
		self.elements["roomEntry"].grid(row=2,column=1)

		self.elements["phoneLabel"]=Label(self.rootFrame,text="Phone: ")
		self.elements["phoneLabel"].grid(row=3,column=0)
		self.elements["phoneEntry"]=Entry(self.rootFrame)
		self.elements["phoneEntry"].insert(0,self.person["phoneNumber"])
		self.elements["phoneEntry"].grid(row=3,column=1)

		self.elements["emailLabel"]=Label(self.rootFrame,text="Email: ")
		self.elements["emailLabel"].grid(row=4,column=0)
		self.elements["emailEntry"]=Entry(self.rootFrame)
		self.elements["emailEntry"].grid(row=4,column=1)
		self.elements["emailEntry"].insert(0,self.person['email'])

		self.elements["buttonChange"]=Button(self.rootFrame,text='Apply Changes',command=self.applyChanges_call)
		self.elements["buttonChange"].grid(row=10,column=0,columnspan=2)

	def applyChanges_call(self,ignore=""):self.root.after(1,self.applyChanges)
	def applyChanges(self,ignore=""):
		self.person["name"]=self.elements["nameEntry"].get()
		self.person["room"]=self.elements["roomEntry"].get()
		self.person["phoneNumber"]=self.elements["phoneEntry"].get()
		self.person['email']=self.elements["emailEntry"].get()

		self.people.modify_person(self.person)
		self.delete()

	def delete(self,ignore=""):
		self.grab_release()
		self.destroy()
