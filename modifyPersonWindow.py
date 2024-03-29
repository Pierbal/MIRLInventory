from Tkinter import *
from people import people
from items import items
from PIL import Image,ImageTk
from datetime import datetime,timedelta
from errorWindow import PopupErrorBox

#for a single person it will checkin or out items
#it will send a new email to the person after changing any status

class personWindow(Toplevel):
	def __init__(self,ROOT,people,personIndex):
		self.people=people
		self.person=self.people[personIndex]
		self.modifiedItems=False

		self.root=ROOT
		Toplevel.__init__(self, self.root)
		self.transient(self.root)
		self.protocol("WM_DELETE_WINDOW",self.delete)
		self.title("Person Items Checkout Window")
		self.result=None

		self.rootFrame=Frame(self)
		self.rootFrame.grid(row=0,column=0)
		self.body()
		self.grab_set()

		self.geometry("+%d+%d" % (self.root.winfo_rootx(),self.root.winfo_rooty()))

		self.wait_window(self)

	def body(self,ignore=""):
		self.elements={}
		self.elements["checkinButton"]=Button(self.rootFrame,text="Check-in Item",command=self.checkinItem_call)
		self.elements["checkinButton"].grid(row=0,column=0)
		self.elements["dateLabel"]=Label(self.rootFrame,text="Date:")
		self.elements["dateLabel"].grid(row=1,column=0)
		self.elements["itemsHave"]=Listbox(self.rootFrame)
		self.elements["itemsHave"].grid(row=2,column=0,sticky=N+S+W,rowspan=999)
		self.elements["itemsHave"].bind("<Button-1>",self.displayItemHaveInfo_call)

		self.elements["checkoutButton"]=Button(self.rootFrame,text="Check-out Item",command=self.checkoutItem_call)
		self.elements["checkoutButton"].grid(row=0,column=2)
		self.elements["searchEntry"]=Entry(self.rootFrame)
		self.elements["searchEntry"].grid(row=1,column=2,sticky=E+W)
		self.elements["searchEntry"].bind("<Key>",self.searchItems_call)
		self.elements["itemsAvailable"]=Listbox(self.rootFrame)
		self.elements["itemsAvailable"].grid(row=2,column=2,sticky=N+S,rowspan=999)
		self.elements["itemsAvailable"].bind("<Button-1>",self.displayItemInfo_call)

		self.elements['customMessageLabel']=Label(self.rootFrame,text="Custom Email Message: ")
		self.elements['customMessageLabel'].grid(row=0,column=4,sticky=W)
		self.elements['customMessageEntry']=Entry(self.rootFrame)
		self.elements['customMessageEntry'].grid(row=0,column=5,sticky=W+E)
		self.elements["itemInfoName"]=Label(self.rootFrame,text="NAME GOES HERE")
		self.elements["itemInfoName"].grid(row=2,column=4,columnspan=2)
		self.elements["itemInfoQuantityLeft"]=Label(self.rootFrame,text="Number Left: 0")
		self.elements["itemInfoQuantityLeft"].grid(row=3,column=4,columnspan=2)
		self.elements["itemInfoQuantityTotal"]=Label(self.rootFrame,text="Total: OVER 9000!!!")
		self.elements["itemInfoQuantityTotal"].grid(row=4,column=4,columnspan=2)
		self.elements["itemInfoTags"]=Label(self.rootFrame,text="Tags:\nTag1\nTag2\nTag3")
		self.elements["itemInfoTags"].grid(row=5,column=4,columnspan=2)
		self.elements["itemInfoDaysAllowed"]=Label(self.rootFrame,text="Days Allowed: 555")
		self.elements["itemInfoDaysAllowed"].grid(row=6,column=4,columnspan=2)
		self.elements["itemInfoPicture"]=Label(self.rootFrame,text="PICTURE WILL GO HERE")
		self.elements["itemInfoPicture"].grid(row=7,column=4,columnspan=2)

		self.itemImage=ImageTk.PhotoImage(file="Image-not-found.gif")
		self.elements["itemInfoPicture"].config(image=self.itemImage)

		#populates the items lis tthat the person currently has checked out
		for item in self.people.dueItems(self.person):
			self.elements["itemsHave"].insert(END,item[0])
			if(self.people.isOverdue(item)):
				self.elements["itemsHave"].itemconfig(END,bg='red')
			else:
				self.elements["itemsHave"].itemconfig(END,bg='green')

		#populates the item list of available things to checkout
		self.items=items()
		self.searchedItems=[]
		for item in self.items:
			if item['premiumStatus']=='1' and self.person['premiumStatus']=='0':continue #if it is a premium and you are not a premium member, then skip it
			self.elements['itemsAvailable'].insert(END,item['name'])
			self.searchedItems.append(item)
			if item["used"]==item["quantity"]:self.elements['itemsAvailable'].itemconfig(END,bg='red')

		self.elements["itemsAvailable"].select_set(0)
		self.displayItemInfo()

		#scrollbars
		self.elements['itemsHaveScroll']=Scrollbar(self.rootFrame,command=self.elements['itemsHave'].yview)
		self.elements['itemsHaveScroll'].grid(row=2,column=1,rowspan=999,sticky=N+S+W)
		self.elements['itemsHave'].config(yscrollcommand=self.elements['itemsHaveScroll'].set)

		self.elements['itemsAvailableScroll']=Scrollbar(self.rootFrame,command=self.elements['itemsAvailable'].yview)
		self.elements['itemsAvailableScroll'].grid(row=2,column=3,rowspan=999,sticky=N+S+W)
		self.elements['itemsAvailable'].config(yscrollcommand=self.elements['itemsAvailableScroll'].set)

	def displayItemHaveInfo_call(self,ignore=""):self.root.after(1,self.displayItemHaveInfo)
	def displayItemHaveInfo(self,ignore=""):
		index=int(self.elements["itemsHave"].curselection()[0])
		self.elements["dateLabel"].config(text="Date: "+self.people.dueItems(self.person)[index][1])

	def displayItemInfo_call(self,ignore=""):self.root.after(1,self.displayItemInfo)
	def displayItemInfo(self,ignore=""):
		index=int(self.elements["itemsAvailable"].curselection()[0])
		self.elements["itemInfoName"].config(text=self.searchedItems[index]['name'])
		self.elements["itemInfoQuantityLeft"].config(text="Number Used: "+self.searchedItems[index]['used'])
		self.elements["itemInfoQuantityTotal"].config(text="Number Total: "+self.searchedItems[index]['quantity'])
		self.elements["itemInfoTags"].config(text="Tags:\n"+self.searchedItems[index]['tags'])
		self.elements["itemInfoDaysAllowed"].config(text="Days Allowed: "+self.searchedItems[index]['daysAllowed'])


		try:
			temp=Image.open("images/"+self.searchedItems[index]['name']+".jpg")
			self.itemImage=ImageTk.PhotoImage(temp.resize((int(temp.size[0]*(300.0/temp.size[1])),300),Image.ANTIALIAS))
		except:self.itemImage=ImageTk.PhotoImage(Image.open("Image-not-found.gif").resize((300,300),Image.ANTIALIAS))
		self.elements["itemInfoPicture"].config(image=self.itemImage)

	def searchItems_call(self,ignore=""):self.root.after(1,self.searchItems)
	def searchItems(self,ignore=""):
		terms=self.elements['searchEntry'].get().split(' ')
		self.elements["itemsAvailable"].delete(0,END)
		self.searchedItems=[]
		for item in self.items:
			if item['premiumStatus']=='1' and self.person['premiumStatus']=='0':continue #if it is a premium and you are not a premium member, then skip it
			hasAllTerms=True
			for term in terms:
				if not (term in item['tags'] or term in item['name']):
					hasAllTerms=False
					break
			if hasAllTerms:
				self.elements["itemsAvailable"].insert(END,item['name'])
				self.searchedItems.append(item)
				if item["used"]==item["quantity"]:self.elements['itemsAvailable'].itemconfig(END,bg='red')
		self.elements["itemsAvailable"].select_set(0)
		self.displayItemInfo()

	def checkinItem_call(self,ignore=""):self.root.after(1,self.checkinItem)
	def checkinItem(self,ignore=""):
		self.modifiedItems=True
		index=int(self.elements["itemsHave"].curselection()[0])
		item=self.people.dueItems(self.person)[index]
		for x in xrange(len(self.person['items'])):
			if self.person['items'][x][0]==item[0] and self.person['items'][x][1]==item[1] and self.person['items'][x][2]==item[2]:
				self.person['items'][x][2]='in'
				break
		self.people.modify_person(self.person)

		otherVersionOfTheItem=self.items.getitem(item[0]) #temp storage of the item we are modifing
		otherVersionOfTheItem['used']=str(int(otherVersionOfTheItem['used'])-1)
		self.items.modify_item(otherVersionOfTheItem)

		self.redrawnLists()

	def checkoutItem_call(self,ignore=""):self.root.after(1,self.checkoutItem)
	def checkoutItem(self,ignore=""):
		self.modifiedItems=True
		index=int(self.elements["itemsAvailable"].curselection()[0])
		if int(self.searchedItems[index]['quantity'])<=int(self.searchedItems[index]['used']):
			PopupErrorBox(self,"Sorry but you cannot check out\n"+self.searchedItems[index]['name']+"\nbecause the max number allowed to be\nchecked out has been reached")
			return
		item=[self.searchedItems[index]['name'],"place-holderDate","out"]
		dueDate=(datetime.today()+timedelta(int(self.searchedItems[index]["daysAllowed"]))).strftime("%m-%d-%Y-%H-%M")
		item[1]=dueDate
		self.person['items'].append(item)
		self.people.modify_person(self.person)

		item=self.searchedItems[index]
		item['used']=str(int(item['used'])+1)
		self.items.modify_item(item)

		self.redrawnLists()
		self.displayItemInfo()

	def redrawnLists(self,ignore=""):
		self.elements["itemsHave"].delete(0,END)
		for item in self.people.dueItems(self.person):
			self.elements["itemsHave"].insert(END,item[0])
			if(self.people.isOverdue(item)):
				self.elements["itemsHave"].itemconfig(END,bg='red')
			else:
				self.elements["itemsHave"].itemconfig(END,bg='green')
		self.searchedItems=[]
		self.elements['itemsAvailable'].delete(0,END)
		for item in self.items:
			if item['premiumStatus']=='1' and self.person['premiumStatus']=='0':continue
			self.elements['itemsAvailable'].insert(END,item['name'])
			self.searchedItems.append(item)
			if item["used"]==item["quantity"]:self.elements['itemsAvailable'].itemconfig(END,bg='red')

	def delete(self,ignore=""):
		if self.modifiedItems:self.people.emailPerson(self.person,self.elements["customMessageEntry"].get()) #email the person
		self.grab_release()
		self.destroy()