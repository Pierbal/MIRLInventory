from Tkinter import *
from items import items
from people import people
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

		self.elements['modifyItemButton']=Button(self.rootFrame,text="Modify Item")
		self.elements['modifyItemButton'].grid(row=1,column=3,rowspan=2,sticky=E)
		self.elements['removeItemButton']=Button(self.rootFrame,text="Remove Item",command=self.removeItem_call)
		self.elements['removeItemButton'].grid(row=3,column=3,rowspan=2,sticky=E)
		self.elements["addItemButton"]=Button(self.rootFrame,text="Add Items")
		self.elements['addItemButton'].grdi(row=5,column=3,sticky=E)

		self.itemImage=ImageTk.PhotoImage(file="Image-not-found.gif")
		self.elements["itemInfoPicture"].config(image=self.itemImage)

		#PERSON ADMIN AREA
		self.elements["peopleList"]=Listbox(self.rootFrame)
		self.elements['peopleList'].grid(row=1000,column=0,sticky=N+S+W) #yes i mean 1000
		self.elements['personInfoName']=Label(self.rootFrame,text="Name Goes Here")
		self.elements['personInfoName'].grid(row=1000,column=2)
		self.elements['personInfoRoom']=Label(self.rootFrame,text="Room: Here")
		self.elements['personInfoRoom'].grid(row=1002,column=2)

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

	def delete(self):
		self.grab_release()
		self.destroy()