from Tkinter import *
from items import items
from people import people

class adminWindowBase(Toplevel):
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
		self.elements["searchEntry"]=Entry(self.rootFrame)
		self.elements['searchEntry'].grid(row=0,column=0)
		self.elements['searchEntry'].bind("<Key>",self.searchItems_call)

		#ITEMS ADMIN AREA
		self.elements['itemsList']=Listbox(self.rootFrame)
		self.elements['itemsList'].grid(row=1,column=0,rowspan=900,sticky=N+S+W)

		#PERSON ADMIN AREA
		self.elements["peopleList"]=Listbox(self.rootFrame)
		self.elements['peopleList'].grid(row=1000,column=0,sticky=N+S+W) #yes i mean 1000

		self.items=items()
		self.searchedItems=[]
		for x in self.items:
			self.searchedItems.append(x)

		self.people=people()
		self.searchedPeople=[]
		for x in self.people:
			self.searchedPeople.append(x)

		self.redrawLists()

	def searchItems_call(self,ignore=""):self.root.after(1,self.searchItems)
	def searchItems(self,ignore=""):
		terms=self.elements['searchEntry'].get().split(' ')
		self.searchedItems=[]
		for x in self.items:
			Matches=True
			for term in terms:
				if not(term in x['tags'] or term in x['name']):
					Matches=False
					break
			if Matches:
				self.searchedItems.append(x)

		self.searchedPeople=[]
		for x in self.people:
			Matches=True
			for term in terms:
				if not(term in x['name'] or term in x["IDNumber"]):
					Matches=False
					break
			if Matches:
				self.searchedPeople.append(x)

		self.redrawLists()

	def redrawLists(self,ignore=""):
		self.elements['itemsList'].delete(0,END)
		self.elements['peopleList'].delete(0,END)
		for x in self.searchedItems:
			self.elements['itemsList'].insert(END,x['name'])
		for x in self.searchedPeople:
			self.elements["peopleList"].insert(END,x['name']+' - '+x['IDNumber'])
			if len(self.people.overdueItems(x))>0: #bad if they have overdue items
				self.elements['peopleList'].itemconfig(END,bg='red')
			elif len(self.people.dueItems(x))>0: #ok if they have items but not overdue
				self.elements['peopleList'].itemconfig(END,bg='green')
			###else: white background because we have no need to worry about this person


	def delete(self):
		self.grab_release()
		self.destroy()