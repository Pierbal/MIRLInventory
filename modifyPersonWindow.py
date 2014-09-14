from Tkinter import *
from people import people
from PIL import Image,ImageTk

class personWindow(Toplevel):
	def __init__(self,ROOT,people,personIndex):
		self.people=people
		self.person=self.people[personIndex]
		print self.person

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

	def body(self,ignore=""):
		self.elements={}
		self.elements["checkinButton"]=Button(self.rootFrame,text="Check-in Item")
		self.elements["checkinButton"].grid(row=0,column=0)
		self.elements["dateLabel"]=Label(self.rootFrame,text="Date:")
		self.elements["dateLabel"].grid(row=1,column=0)
		self.elements["itemsHave"]=Listbox(self.rootFrame)
		self.elements["itemsHave"].grid(row=2,column=0,sticky=N+S+W,rowspan=999)

		self.elements["checkoutButton"]=Button(self.rootFrame,text="Check-out Item")
		self.elements["checkoutButton"].grid(row=0,column=1)
		self.elements["searchEntry"]=Entry(self.rootFrame)
		self.elements["searchEntry"].grid(row=1,column=1,sticky=E+W)
		self.elements["itemsAvailable"]=Listbox(self.rootFrame)
		self.elements["itemsAvailable"].grid(row=2,column=1,sticky=N+S,rowspan=999)

		self.elements["itemInfoName"]=Label(self.rootFrame,text="NAME GOES HERE")
		self.elements["itemInfoName"].grid(row=2,column=2)
		self.elements["itemInfoQuantityLeft"]=Label(self.rootFrame,text="Number Left: 0")
		self.elements["itemInfoQuantityLeft"].grid(row=3,column=2)
		self.elements["itemInfoQuantityTotal"]=Label(self.rootFrame,text="Total: OVER 9000!!!")
		self.elements["itemInfoQuantityTotal"].grid(row=4,column=2)
		self.elements["itemInfoTags"]=Label(self.rootFrame,text="Tags:\nTag1\nTag2\nTag3")
		self.elements["itemInfoTags"].grid(row=5,column=2)
		self.elements["itemInfoPicture"]=Label(self.rootFrame,text="PICTURE WILL GO HERE")
		self.elements["itemInfoPicture"].grid(row=6,column=2)

		self.temp=ImageTk.PhotoImage(file="Image-not-found.gif")
		self.elements["itemInfoPicture"].config(image=self.temp)

	def delete(self,ignore=""):
		self.grab_release()
		self.destroy()