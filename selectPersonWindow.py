from Tkinter import *
from modifyPersonWindow import personWindow

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

	def delete(self,ignore=""):
		self.grab_release()
		self.destroy()
