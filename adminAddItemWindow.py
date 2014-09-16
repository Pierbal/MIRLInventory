from Tkinter import *
from items import items
from people import people
from PIL import Image,ImageTk
from tkFileDialog import askopenfilename
import shutil

class adminAddItem(Toplevel):
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
		self.item={'used':'0'}
		self.elements['nameLabel']=Label(self.rootFrame,text="Name: ")
		self.elements['nameLabel'].grid(row=0,column=0,sticky=W)
		self.elements['nameEntry']=Entry(self.rootFrame)
		self.elements['nameEntry'].grid(row=0,column=1,sticky=W+E)
		self.elements['quantityLabel']=Label(self.rootFrame,text="Total Avail: ")
		self.elements['quantityLabel'].grid(row=2,column=0,sticky=W)
		self.elements['quantityEntry']=Entry(self.rootFrame)
		self.elements['quantityEntry'].grid(row=2,column=1,sticky=W+E)
		self.elements['quantityEntry'].insert(0,'0')
		self.elements['daysAllowedLabel']=Label(self.rootFrame,text="Days: ")
		self.elements['daysAllowedLabel'].grid(row=3,column=0,sticky=W)
		self.elements['daysAllowedEntry']=Entry(self.rootFrame)
		self.elements['daysAllowedEntry'].grid(row=3,column=1,sticky=W+E)
		self.elements['daysAllowedEntry'].insert(0,"2")
		self.elements['priceLabel']=Label(self.rootFrame,text="Price: ")
		self.elements['priceLabel'].grid(row=4,column=0,sticky=W)
		self.elements['priceEntry']=Entry(self.rootFrame)
		self.elements['priceEntry'].grid(row=4,column=1,sticky=W+E)
		self.elements['priceEntry'].insert(0,"2.0")
		self.elements['tagsLabel']=Label(self.rootFrame,text="Tags: ")
		self.elements['tagsLabel'].grid(row=5,column=0,sticky=W)
		self.elements['tagsEntry']=Entry(self.rootFrame)
		self.elements['tagsEntry'].grid(row=5,column=1,sticky=E+W)

		self.elements['premiumLabel']=Label(self.rootFrame,text="Premium Item")
		self.elements['premiumLabel'].grid(row=6,column=0,sticky=W)
		temp=StringVar()
		self.elements['premiumEntry']=Checkbutton(self.rootFrame,text="",variable=temp,onvalue='1',offvalue='0')
		self.elements['premiumEntry'].grid(row=6,column=1)
		self.elements['premiumEntry'].state=temp
		self.elements['premiumEntry'].deselect()

		self.elements['imageLabel']=Label(self.rootFrame)
		self.elements['imageLabel'].grid(row=1,column=3,rowspan=7,columnspan=2)
		self.updateImage()
		self.elements['imageImportButton']=Button(self.rootFrame,text="Import Image",command=self.importImage)
		self.elements['imageImportButton'].grid(row=9,column=4)

		self.elements['applyButton']=Button(self.rootFrame,text="  APPLY  ",command=self.applyChanges)
		self.elements['applyButton'].grid(row=10,column=0,columnspan=2,sticky=E+W+N+S)

	def importImage(self):
		self.filename=askopenfilename(parent=self,defaultextension='.jpg',initialdir='/home',title='Select a JPEG Image')
		self.updateImage()
		

	def pinchInUpdates_call(self,ignore=''):self.root.after(1,self.pinchInUpdates)
	def pinchInUpdates(self,ignore=''):
		self.update_idletasks()
		self.item['premiumStatus']=self.elements['premiumEntry'].state.get()
		self.item['quantity']=self.elements['quantityEntry'].get()
		self.item['daysAllowed']=self.elements['daysAllowedEntry'].get()
		self.item['price']=self.elements['priceEntry'].get()
		self.item["tags"]=self.elements['tagsEntry'].get()
		self.item['name']=self.elements['nameEntry'].get()
		print self.item['name']


	def applyChanges(self):
		self.pinchInUpdates()
		self.items=items()
		self.items.modify_item(self.item)
		try: shutil.copy(self.filename,'images/'+self.item['name']+'.jpg')
		except: print "WARNING: NO IMAGE IMPRTED FOR ITEM"
		self.destroy()

	def updateImage(self,ignore=''):
		self.pinchInUpdates()
		try:
			temp=Image.open(self.filename)
			self.image=ImageTk.PhotoImage(temp.resize((int(temp.size[0]*(300.0/temp.size[1])),300),Image.ANTIALIAS))
		except: self.image=ImageTk.PhotoImage(Image.open("Image-not-found.gif").resize((300,300),Image.ANTIALIAS))
		self.elements['imageLabel'].config(image=self.image)

	def delete(self):
		self.grab_release()
		self.destroy()