from Tkinter import *
from modifyPersonWindow import personWindow
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
		self.elements["personList"].grid(row=0,column=0,rowspan=999)
		self.elements["personList"].focus_set()
		self.elements["personList"].bind("<Button-1>",self.displayPerson)
		self.elements["nameLabel"]=Label(self.rootFrame,text="Student Name")
		self.elements["nameLabel"].grid(row=0,column=1)
		self.elements["muidLabel"]=Label(self.rootFrame,text="Student Number")
		self.elements["muidLabel"].grid(row=1,column=1)
		self.elements["roomLabel"]=Label(self.rootFrame,text="Room")
		self.elements["roomLabel"].grid(row=2,column=1)
		self.elements["itemsLabel"]=Label(self.rootFrame,text="Items:\nLine 1\nLine2")
		self.elements["itemsLabel"].grid(row=3,column=1)
		
		self.elements["buttonAddItems"]=Button(self.rootFrame,text="Add Items")
		self.elements["buttonAddItems"].grid(row=10,column=1)

		self.people=people()
		for x in self.people.people:
			print x
			self.elements["personList"].insert(END,x['name'])

	def displayPerson(self,ignore=""):
		self.elements["personList"]

	def delete(self,ignore=""):
		self.grab_release()
		self.destroy()
