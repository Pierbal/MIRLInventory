from Tkinter import *
from items import items
from people import people
from PIL import Image,ImageTk
from tkFileDialog import askopenfilename
import shutil

class adminItemModify(Toplevel):
	def __init__(self,ROOT,item):
		self.root=ROOT
		self.item=item
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
		print self.item
		self.elements['nameLabel']=Label(self.rootFrame,text=self.item['name'])
		self.elements['nameLabel'].grid(row=0,column=0,columnspan=2)
		self.elements['usedLabel']=Label(self.rootFrame,text="Checked Out: "+self.item['used'])
		self.elements['usedLabel'].grid(row=1,column=0,columnspan=2)
		self.elements['quantityLabel']=Label(self.rootFrame,text="Total Avail: ")
		self.elements['quantityLabel'].grid(row=2,column=0,sticky=W)
		self.elements['quantityEntry']=Entry(self.rootFrame)
		self.elements['quantityEntry'].grid(row=2,column=1,sticky=W+E)
		self.elements['quantityEntry'].insert(0,self.item['quantity'])
		self.elements['daysAllowedLabel']=Label(self.rootFrame,text="Days: ")
		self.elements['daysAllowedLabel'].grid(row=3,column=0,sticky=W)
		self.elements['daysAllowedEntry']=Entry(self.rootFrame)
		self.elements['daysAllowedEntry'].grid(row=3,column=1,sticky=W+E)
		self.elements['daysAllowedEntry'].insert(0,self.item['daysAllowed'])
		self.elements['hoursAllowedLabel']=Label(self.rootFrame,text="Hours: ")
		self.elements['hoursAllowedLabel'].grid(row=4,column=0,sticky=W)
		self.elements['hoursAllowedEntry']=Entry(self.rootFrame)
		self.elements['hoursAllowedEntry'].grid(row=4,column=1,sticky=W+E)
		self.elements['hoursAllowedEntry'].insert(0,self.item['hoursAllowed'])
		self.elements['priceLabel']=Label(self.rootFrame,text="Price: ")
		self.elements['priceLabel'].grid(row=5,column=0,sticky=W)
		self.elements['priceEntry']=Entry(self.rootFrame)
		self.elements['priceEntry'].grid(row=5,column=1,sticky=W+E)
		self.elements['priceEntry'].insert(0,self.item['price'])

		self.elements['premiumLabel']=Label(self.rootFrame,text="Premium Item: ")
		self.elements['premiumLabel'].grid(row=6,column=0,sticky=W)
		temp=StringVar()
		self.elements['premiumEntry']=Checkbutton(self.rootFrame,text="",variable=temp,onvalue='1',offvalue='0')
		self.elements['premiumEntry'].grid(row=6,column=1,sticky=W)
		self.elements['premiumEntry'].state=temp
		if self.item['premiumStatus']=='1':self.elements['premiumEntry'].select()
		else:self.elements['premiumEntry'].deselect()

		self.elements['tagsLabel']=Label(self.rootFrame,text="Tags: ")
		self.elements['tagsLabel'].grid(row=7,column=0,sticky=W)
		self.elements['tagsEntry']=Entry(self.rootFrame)
		self.elements['tagsEntry'].grid(row=7,column=1,sticky=E+W)
		self.elements["tagsEntry"].insert(0,self.item['tags'])

		self.elements['imageLabel']=Label(self.rootFrame)
		self.elements['imageLabel'].grid(row=1,column=3,rowspan=7,columnspan=2)
		self.updateImage()
		self.elements['imageImportButton']=Button(self.rootFrame,text="Import Image",command=self.importImage)
		self.elements['imageImportButton'].grid(row=9,column=4)

		self.elements['peopleList']=Listbox(self.rootFrame)
		self.elements['peopleList'].grid(row=0,column=5,rowspan=10,sticky=N+S)

		self.elements['applyButton']=Button(self.rootFrame,text="  APPLY  ",command=self.applyChanges)
		self.elements['applyButton'].grid(row=10,column=0,columnspan=2,sticky=E+W+N+S)

		self.people=people()
		for person in self.people:
			for item in person['items']:
				if self.item['name']==item[0]:
					self.elements['peopleList'].insert(END,person['name']+' - '+person['IDNumber'])
					break

	def updateImage(self,ignore=''):
		try:
			temp=Image.open("images/"+self.item['name']+".jpg")
			self.image=ImageTk.PhotoImage(temp.resize((int(temp.size[0]*(300.0/temp.size[1])),300),Image.ANTIALIAS))
		except: self.image=ImageTk.PhotoImage(Image.open("Image-not-found.gif").resize((300,300),Image.ANTIALIAS))
		self.elements['imageLabel'].config(image=self.image)

	def importImage(self):
		filename=askopenfilename(parent=self,defaultextension='.jpg',initialdir='/home',title='Select a JPEG Image')
		shutil.copy(filename,'images/'+self.item['name']+'.jpg')
		self.updateImage()

	def applyChanges(self):
		self.item['premiumStatus']=self.elements['premiumEntry'].state.get()
		self.item['quantity']=self.elements['quantityEntry'].get()
		self.item['daysAllowed']=self.elements['daysAllowedEntry'].get()
		self.item['hoursAllowed']=self.elements['hoursAllowedEntry'].get()
		self.item['price']=self.elements['priceEntry'].get()
		self.item["tags"]=self.elements['tagsEntry'].get()
		self.items=items()
		self.items.modify_item(self.item)
		self.destroy()

	def delete(self):
		self.grab_release()
		self.destroy()