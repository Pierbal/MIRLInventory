from Tkinter import *
from items import items
from people import people

class adminAddPerson(Toplevel):
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
		self.person={"items":[]}
		self.elements['nameLabel']=Label(self.rootFrame,text="Name: ")
		self.elements['nameLabel'].grid(row=0,column=0,sticky=W)
		self.elements['nameEntry']=Entry(self.rootFrame)
		self.elements['nameEntry'].grid(row=0,column=1,sticky=E+W)
		self.elements['idNumberLabel']=Label(self.rootFrame,text="ID Number: ")
		self.elements['idNumberLabel'].grid(row=1,column=0,sticky=W)
		self.elements['idNumberEntry']=Entry(self.rootFrame)
		self.elements['idNumberEntry'].grid(row=1,column=1,sticky=E+W)
		self.elements['roomLabel']=Label(self.rootFrame,text="Room: ")
		self.elements['roomLabel'].grid(row=2,column=0,sticky=W)
		self.elements['roomEntry']=Entry(self.rootFrame)
		self.elements['roomEntry'].grid(row=2,column=1,sticky=E+W)
		self.elements['phoneLabel']=Label(self.rootFrame,text="Phone: ")
		self.elements['phoneLabel'].grid(row=3,column=0,sticky=W)
		self.elements['phoneEntry']=Entry(self.rootFrame)
		self.elements['phoneEntry'].grid(row=3,column=1,sticky=E+W)
		self.elements['emailLabel']=Label(self.rootFrame,text="E-Mail: ")
		self.elements['emailLabel'].grid(row=4,column=0,sticky=W)
		self.elements['emailEntry']=Entry(self.rootFrame)
		self.elements['emailEntry'].grid(row=4,column=1,sticky=E+W)

		self.elements['applyButton']=Button(self.rootFrame,text="  APPLY  ",command=self.applyChanges)
		self.elements['applyButton'].grid(row=10,column=0,columnspan=2)

	def applyChanges(self,ignore=""):
		self.person['name']=self.elements['nameEntry'].get()
		self.person['IDNumber']=self.elements['idNumberEntry'].get()
		self.person['room']=self.elements['roomEntry'].get()
		self.person['phoneNumber']=self.elements['phoneEntry'].get()
		self.person['email']=self.elements['emailEntry'].get()
		self.people=people()
		self.people.modify_person(self.person)
		self.destroy()

	def delete(self):
		self.grab_release()
		self.destroy()