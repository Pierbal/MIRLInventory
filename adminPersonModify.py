from Tkinter import *
from items import items
from people import people

class adminPersonModify(Toplevel):
	def __init__(self,ROOT,person):
		self.root=ROOT
		self.person=person
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
		self.elements['idNumberLabel']=Label(self.rootFrame,text="ID Number: "+self.person['IDNumber'])
		self.elements['idNumberLabel'].grid(row=0,column=0,columnspan=2)
		self.elements['nameLabel']=Label(self.rootFrame,text="Name: ")
		self.elements['nameLabel'].grid(row=1,column=0,sticky=W)
		self.elements['nameEntry']=Entry(self.rootFrame)
		self.elements['nameEntry'].grid(row=1,column=1,sticky=E+W)
		self.elements['nameEntry'].insert(0,self.person['name'])
		self.elements['roomLabel']=Label(self.rootFrame,text="Room: ")
		self.elements['roomLabel'].grid(row=2,column=0,sticky=W)
		self.elements['roomEntry']=Entry(self.rootFrame)
		self.elements['roomEntry'].grid(row=2,column=1,sticky=E+W)
		self.elements['roomEntry'].insert(0,self.person['room'])
		self.elements['phoneLabel']=Label(self.rootFrame,text="Phone: ")
		self.elements['phoneLabel'].grid(row=3,column=0,sticky=W)
		self.elements['phoneEntry']=Entry(self.rootFrame)
		self.elements['phoneEntry'].grid(row=3,column=1,sticky=E+W)
		self.elements['phoneEntry'].insert(0,self.person['phoneNumber'])
		self.elements['emailLabel']=Label(self.rootFrame,text="E-Mail: ")
		self.elements['emailLabel'].grid(row=4,column=0,sticky=W)
		self.elements['emailEntry']=Entry(self.rootFrame)
		self.elements['emailEntry'].grid(row=4,column=1,sticky=E+W)
		self.elements['emailEntry'].insert(0,self.person['email'])

		self.elements['premiumLabel']=Label(self.rootFrame,text="Premium Status: ")
		self.elements['premiumLabel'].grid(row=5,column=0,sticky=W)
		temp=StringVar()
		self.elements['premiumEntry']=Checkbutton(self.rootFrame,text="",variable=temp,onvalue='1',offvalue='0')
		self.elements['premiumEntry'].grid(row=5,column=1,sticky=W)
		self.elements['premiumEntry'].state=temp
		if self.person['premiumStatus']=='1':self.elements['premiumEntry'].select()
		else:self.elements['premiumEntry'].deselect()

		self.elements['currentItemsLabel']=Label(self.rootFrame,text="Checked Out")
		self.elements['currentItemsLabel'].grid(row=0,column=2)
		self.elements['currentItems']=Listbox(self.rootFrame)
		self.elements["currentItems"].grid(row=1,column=2,rowspan=8,sticky=N+S)
		self.elements['pastItemsLabel']=Label(self.rootFrame,text="Past Items")
		self.elements['pastItemsLabel'].grid(row=0,column=4)
		self.elements['pastItems']=Listbox(self.rootFrame)
		self.elements['pastItems'].grid(row=1,column=4,rowspan=8,sticky=N+S)

		self.elements['applyButton']=Button(self.rootFrame,text="  APPLY  ",command=self.applyChanges)
		self.elements['applyButton'].grid(row=10,column=0,columnspan=2)

		self.people=people()
		for x in self.people.dueItems(self.person):
			self.elements['currentItems'].insert(END,x[0])
			if self.people.isOverdue(x):
				self.elements['currentItems'].itemconfig(END,bg='red')
		for x in self.people.pastItems(self.person):
			self.elements['pastItems'].insert(END,x[0])

		self.elements['itemInfoDate']=Label(self.rootFrame,text="Date: HERE!")
		self.elements['itemInfoDate'].grid(row=10,column=2)
		self.elements['itemInfoPrice']=Label(self.rootFrame,text="Price: HERE!")
		self.elements['itemInfoPrice'].grid(row=10,column=4)

		#scrollbars
		self.elements['currentItemsScroll']=Scrollbar(self.rootFrame,command=self.elements['currentItems'].yview)
		self.elements['currentItemsScroll'].grid(row=1,column=3,rowspan=8,sticky=N+S+W)
		self.elements['currentItems'].config(yscrollcommand=self.elements['currentItemsScroll'].set)

		self.elements['pastItemsScroll']=Scrollbar(self.rootFrame,command=self.elements['pastItems'].yview)
		self.elements['pastItemsScroll'].grid(row=1,column=5,rowspan=8,sticky=N+S+W)
		self.elements['pastItems'].config(yscrollcommand=self.elements['pastItemsScroll'].set)

	def applyChanges(self,ignore=""):
		self.person['name']=self.elements['nameEntry'].get()
		self.person['room']=self.elements['roomEntry'].get()
		self.person['phoneNumber']=self.elements['phoneEntry'].get()
		self.person['email']=self.elements['emailEntry'].get()
		self.person['premiumStatus']=self.elements['premiumEntry'].state.get()
		self.people.modify_person(self.person)
		self.destroy()

	def delete(self):
		self.grab_release()
		self.destroy()