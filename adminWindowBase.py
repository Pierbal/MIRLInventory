from Tkinter import *
from items import items
from people import people
from adminItemModifyWindow import adminItemModify
from adminAddItemWindow import adminAddItem
from adminPersonModify import adminPersonModify
from adminAddPersonWindow import adminAddPerson
from PIL import Image,ImageTk

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
		self.elements['itemsList'].bind("<Button-1>",self.displayInfoItem_call)
		self.elements['itemInfoName']=Label(self.rootFrame,text="Item Name")
		self.elements["itemInfoName"].grid(row=1,column=2)
		self.elements["itemInfoQuantityLeft"]=Label(self.rootFrame,text="Number Left: 0")
		self.elements["itemInfoQuantityLeft"].grid(row=2,column=2)
		self.elements["itemInfoQuantityTotal"]=Label(self.rootFrame,text="Total: OVER 9000!!!")
		self.elements["itemInfoQuantityTotal"].grid(row=3,column=2)
		self.elements["itemInfoTags"]=Label(self.rootFrame,text="Tags:\nTag1 Tag2 Tag3")
		self.elements["itemInfoTags"].grid(row=4,column=2)
		self.elements["itemInfoDaysAllowed"]=Label(self.rootFrame,text="Days Allowed: 555")
		self.elements["itemInfoDaysAllowed"].grid(row=5,column=2)
		self.elements["itemInfoPicture"]=Label(self.rootFrame,text="PICTURE WILL GO HERE")
		self.elements["itemInfoPicture"].grid(row=6,column=2,columnspan=2)

		self.elements['modifyItemButton']=Button(self.rootFrame,text="Modify Item",command=self.modifyItem_call)
		self.elements['modifyItemButton'].grid(row=1,column=3,rowspan=2,sticky=E)
		self.elements['removeItemButton']=Button(self.rootFrame,text="Remove Item",command=self.removeItem_call)
		self.elements['removeItemButton'].grid(row=3,column=3,rowspan=2,sticky=E)
		self.elements["addItemButton"]=Button(self.rootFrame,text="Add Items",command=self.addItem_call)
		self.elements['addItemButton'].grid(row=5,column=3,sticky=E)

		self.itemImage=ImageTk.PhotoImage(file="Image-not-found.gif")
		self.elements["itemInfoPicture"].config(image=self.itemImage)

		#PERSON ADMIN AREA
		self.elements["peopleList"]=Listbox(self.rootFrame)
		self.elements['peopleList'].grid(row=1000,column=0,rowspan=999,sticky=N+S+W) #yes i mean row=1000
		self.elements['peopleList'].bind("<Button-1>",self.displayPersonInfo_call)
		self.elements['personInfoName']=Label(self.rootFrame,text="Name Goes Here")
		self.elements['personInfoName'].grid(row=1000,column=2)
		self.elements['personInfoRoom']=Label(self.rootFrame,text="Room: Here")
		self.elements['personInfoRoom'].grid(row=1001,column=2)
		self.elements['personInfoIdNumber']=Label(self.rootFrame,text="IDNumber: Here")
		self.elements['personInfoIdNumber'].grid(row=1002,column=2)
		self.elements['personInfoPhone']=Label(self.rootFrame,text="PHONE NUMBER HERE")
		self.elements['personInfoPhone'].grid(row=1003,column=2)
		self.elements['personInfoEmail']=Label(self.rootFrame,text="Email Here")
		self.elements['personInfoEmail'].grid(row=1004,column=2)

		self.elements['modifyPersonButton']=Button(self.rootFrame,text="Modify Person",command=self.modifyPerson_call)
		self.elements['modifyPersonButton'].grid(row=1000,column=3,sticky=E,rowspan=2)
		self.elements['removePersonButton']=Button(self.rootFrame,text="Remove Person",command=self.removePerson_call)
		self.elements['removePersonButton'].grid(row=1002,column=3,sticky=E,rowspan=2)
		self.elements['addPersonButton']=Button(self.rootFrame,text="Add Person",command=self.addPerson_call)
		self.elements['addPersonButton'].grid(row=1004,column=3,rowspan=2,sticky=E)

		#initialize the lists
		self.items=items()
		self.searchedItems=[]
		for x in self.items:
			self.searchedItems.append(x)

		self.people=people()
		self.searchedPeople=[]
		for x in self.people:
			self.searchedPeople.append(x)

		self.redrawLists()

		#scrollbars
		self.elements['peopleListScroll']=Scrollbar(self.rootFrame,command=self.elements['peopleList'].yview)
		self.elements['peopleListScroll'].grid(row=1000,column=1,rowspan=999,sticky=N+S+W)
		self.elements['peopleList'].config(yscrollcommand=self.elements['peopleListScroll'].set)

		self.elements['itemsListScroll']=Scrollbar(self.rootFrame,command=self.elements['itemsList'].yview)
		self.elements['itemsListScroll'].grid(row=1,column=1,rowspan=900,sticky=N+S+W)
		self.elements['itemsList'].config(yscrollcommand=self.elements['itemsListScroll'].set)

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

#ITEM SPECIFIC THINGS
	def displayInfoItem_call(self,ignore=""):self.root.after(1,self.displayInfoItem)
	def displayInfoItem(self,ignore=""):
		index=int(self.elements['itemsList'].curselection()[0])
		self.elements["itemInfoName"].config(text=self.searchedItems[index]['name'])
		self.elements['itemInfoQuantityLeft'].config(text="Number Left: "+self.searchedItems[index]['used'])
		self.elements['itemInfoQuantityTotal'].config(text="Total: "+self.searchedItems[index]['quantity'])
		self.elements['itemInfoDaysAllowed'].config(text="Days Allowed: "+self.searchedItems[index]['daysAllowed'])
		self.elements['itemInfoTags'].config(text="Tags:\n"+self.searchedItems[index]['tags'])
		
		try:
			temp=Image.open("images/"+self.searchedItems[index]['name']+".jpg")
			self.itemImage=ImageTk.PhotoImage(temp.resize((int(temp.size[0]*(300.0/temp.size[1])),300),Image.ANTIALIAS))
		except: self.itemImage=ImageTk.PhotoImage(Image.open("Image-not-found.gif").resize((300,300),Image.ANTIALIAS))
		self.elements["itemInfoPicture"].config(image=self.itemImage)

	def removeItem_call(self,ignore=''):self.root.after(1,self.removeItem)
	def removeItem(self,ignore=''):
		#ONLY DO THIS IF THERE ARE NONE CHECKED OUT
		index=int(self.elements['itemsList'].curselection()[0])
		for person in self.people:
			for item in person['items']:
				if item[0]==self.searchedItems[index]['name']:
					print "UNABLE TO DELETE "+item[0]+" BECAUSE SOMEONE HAS ONE CHECKED OUT"
					return #so that it never touches the bottom
		self.items.delete_item(self.searchedItems[index])
		self.redrawLists()

	def modifyItem_call(self,ignore=""):self.root.after(1,self.modifyItem)
	def modifyItem(self,ignore=""):
		index=int(self.elements['itemsList'].curselection()[0])
		adminItemModify(self,self.items[index])
		self.searchItems()
		self.elements['itemsList'].select_set(index)
		self.displayInfoItem()

	def addItem_call(self,ignore=""):self.root.after(1,self.addItem)
	def addItem(self,ignore=""):
		adminAddItem(self)
		self.items.update_items()
		self.searchItems()

#PEOPLE SPECIFIC THINGS
	def displayPersonInfo_call(self,ignore=""):self.root.after(1,self.displayPersonInfo)
	def displayPersonInfo(self,ignore=""):
		index=int(self.elements['peopleList'].curselection()[0])
		self.elements['personInfoName'].config(text=self.searchedPeople[index]['name'])
		self.elements['personInfoEmail'].config(text=self.searchedPeople[index]['email'])
		self.elements['personInfoPhone'].config(text=self.searchedPeople[index]['phoneNumber'])
		self.elements['personInfoRoom'].config(text="Room: "+self.searchedPeople[index]['room'])
		self.elements['personInfoIdNumber'].config(text=self.searchedPeople[index]['IDNumber'])

	def addPerson_call(self,ignore=''):self.root.after(1,self.addPerson)
	def addPerson(self,ignore=''):
		adminAddPerson(self)
		self.people.update_people()
		self.searchItems()

	def removePerson_call(self,ignore=""):self.root.after(1,self.removePerson)
	def removePerson(self,ignore=""):
		index=int(self.elements['peopleList'].curselection()[0])
		if len(self.people.dueItems(self.people[index]))>0:
			print "UNABLE TO DELETE "+self.people[index]['name']+" BECAUSE THEY HAVE ITEMS CHECKED OUT"
			return
		self.people.deletePerson(self.people[index])
		self.searchItems()

	def modifyPerson_call(self,ignore=""):self.root.after(1,self.modifyPerson)
	def modifyPerson(self,ignore=""):
		index=int(self.elements['peopleList'].curselection()[0])
		adminPersonModify(self,self.searchedPeople[index])
		self.people.update_people()
		self.searchItems()
		self.elements['peopleList'].select_set(index)
		self.displayPersonInfo()

	def delete(self):
		self.grab_release()
		self.destroy()