import items
import people
import time
from Tkinter import *

items=items.items() #automaticly makes the full list of items in the recorded inventory
people=people.people() #automaticlly fills the list of people

#add items window
def addItems_windwosMake(ignore=''):
	global addItemsWindow
	addItemsWindow=Toplevel(itemWindow)
	addItemsWindow.protocol("WM_DELETE_WINDOW",addItems_windowDelete)
def addItems_windowDelete(ignore=''):	
	addItemsWindow.destroy()

#Items window
def itemWindow_removeItem_call(ignore=''):root.after(1,itemWindow_removeItem)
def itemWindow_removeItem(ignore=''):
	itemIndex=int(itemWindow_list.curselection()[0])
	item=items.get_item(itemWindow_list.get(ACTIVE))
	items.modify_item(item['name'],item['quantity'],str(int(item['used'])-1),item['tags'])
	global person
	del person['items'][itemIndex]
	people.modify_person(person['name'],person['IDNumber'],person['room'],person['items'])
	itemWindow_list.delete(itemIndex)

def itemWindow_addItem_call(ignore=''):root.after(1,itemWindow_addItem)
def itemWindow_addItem(ignore=''):
	itemIndex=int(itemWindow_addList.curselection()[0])
	item=items.get_item(itemWindow_addList.get(ACTIVE))
	items.modify_item(item['name'],item['quantity'],str(int(item['used'])+1),item['tags'])
	global person
	person['items'].append([item['name'],time.strftime('%m-%d-%Y')])
	people.modify_person(person['name'],person['IDNumber'],person['room'],person['items'])
	itemWindow_list.insert(END,person['items'][-1][0])

def itemWindow_searchItems_call(ignore=''):root.after(1,itemWindow_searchItems)
def itemWindow_searchItems(ignore=''):
	itemWindow_addList.delete(0,END)
	itemList=items.search_items(itemWindow_addSearch.get())
	for item in itemList:
		itemWindow_addList.insert(END,item['name'])

def itemWindow_info_call(ignore=''):root.after(1,itemWindow_info)
def itemWindow_info(ignore=''):
	index=int(itemWindow_list.curselection()[0])
	itemWindow_date.config(text='Date: '+person['items'][index][1])

def item_windowMake(ignore=''):
	global itemWindow,person,itemWindow_list,itemWindow_addButton,itemWindow_date,itemWindow_removeButton
	global itemWindow_addList,itemWindow_addSearch
	itemWindow=Toplevel(personWindow)
	itemWindow.protocol("WM_DELETE_WINDOW",item_windowDelete)
	personWindow_search_list.config(state='disable')
	personWindow_search_entry.config(state='disable')
	personWindow_addPersonButton.config(state='disable')
	personWindow_modifyPersonButton.config(state='disable')
	personWindow_info_button.config(state='disable')

	person=personWindow_search_list.get(ACTIVE)
	person=people.get_person(person)

	itemWindow_addButton=Button(itemWindow,text='Add Item',command=itemWindow_addItem_call)
	itemWindow_addButton.grid(row=0,column=1)
	itemWindow_addSearch=Entry(itemWindow)
	itemWindow_addSearch.grid(row=1,column=1)
	itemWindow_addSearch.bind("<Key>",itemWindow_searchItems_call)
	itemWindow_addList=Listbox(itemWindow)
	itemWindow_addList.grid(row=2,column=1,rowspan=1000)
	itemWindow_list=Listbox(itemWindow)
	itemWindow_list.grid(row=2,column=0,rowspan=1000)
	itemWindow_list.bind("<Button-1>",itemWindow_info_call)
	itemWindow_date=Label(itemWindow,text='Date: ')
	itemWindow_date.grid(row=1,column=0)
	itemWindow_removeButton=Button(itemWindow,text='Remove Item',command=itemWindow_removeItem_call)
	itemWindow_removeButton.grid(row=0,column=0)

	for item in person['items']:
		itemWindow_list.insert(END,item[0])
	itemWindow_searchItems()
def item_windowDelete(ignore=''):
	itemWindow.destroy()
	personWindow_search_list.config(state='normal')
	personWindow_search_entry.config(state='normal')
	personWindow_addPersonButton.config(state='normal')
	personWindow_modifyPersonButton.config(state='normal')
	personWindow_info_button.config(state='normal')


#Person window
def personWindow_modifyPerson_call(ignore=''):root.after(1,personWindow_modifyPerson)
def personWindow_modifyPerson(ignore=''):
	global person
	personWindow_makePerson()
	person=people.get_person(personWindow_search_list.get(ACTIVE))
	makePersonWindow_name_entry.insert(END,person['name'])
	makePersonWindow_idnumber_entry.insert(END,person['IDNumber'])
	makePersonWindow_room_entry.insert(END,person['room'])

def personWindow_addPerson_call(ignore=''):root.after(1,personWindow_addPerson)
def personWindow_addPerson(ignore=''):
	name=makePersonWindow_name_entry.get()
	idnumber=makePersonWindow_idnumber_entry.get()
	room=makePersonWindow_room_entry.get()
	try:people.modify_person(name,idnumber,room,person['items'])
	except:people.modify_person(name,idnumber,room,[])
	personWindow_makePerson_delete()
	people.update_people()
	personWindow_search_list.delete(0,END)
	for person in people.people:
		personWindow_search_list.insert(END,person['name'])
	del person

def personWindow_makePerson_call(ignore=''):root.after(1,personWindow_makePerson)
def personWindow_makePerson(ignore=''):
	global makePersonWindow,makePersonWindow_name_entry,makePersonWindow_idnumber_entry,makePersonWindow_room_entry
	makePersonWindow=Toplevel(personWindow)
	makePersonWindow.protocol("WM_DELETE_WINDOW",personWindow_makePerson_delete)
	personWindow_search_list.config(state='disable')
	personWindow_search_entry.config(state='disable')
	personWindow_addPersonButton.config(state='disable')
	personWindow_modifyPersonButton.config(state='disable')
	personWindow_info_button.config(state='disable')

	makePersonWindow_name_label=Label(makePersonWindow,text='Name: ')
	makePersonWindow_name_label.grid(row=0,column=0)
	makePersonWindow_name_entry=Entry(makePersonWindow)
	makePersonWindow_name_entry.grid(row=0,column=1)
	makePersonWindow_idnumber_label=Label(makePersonWindow,text='ID Number: ')
	makePersonWindow_idnumber_label.grid(row=1,column=0)
	makePersonWindow_idnumber_entry=Entry(makePersonWindow)
	makePersonWindow_idnumber_entry.grid(row=1,column=1)
	makePersonWindow_room_label=Label(makePersonWindow,text='Work Room Number: ')
	makePersonWindow_room_label.grid(row=2,column=0)
	makePersonWindow_room_entry=Entry(makePersonWindow)
	makePersonWindow_room_entry.grid(row=2,column=1)
	makePersonWindow_button=Button(makePersonWindow,text='Add Person',command=personWindow_addPerson_call)
	makePersonWindow_button.grid(row=3,column=0,columnspan=2)

def personWindow_makePerson_delete(ignore=''):
	makePersonWindow.destroy()
	personWindow_search_list.config(state='normal')
	personWindow_search_entry.config(state='normal')
	personWindow_addPersonButton.config(state='normal')
	personWindow_modifyPersonButton.config(state='normal')
	personWindow_info_button.config(state='normal')

def person_search_searchPeople_call(ignore=''):root.after(1,person_search_searchPeople)
def person_search_searchPeople(ignore=''):
	personWindow_search_list.delete(0,END)
	term=personWindow_search_entry.get()
	person_list=people.search_people(term)
	for person in person_list:
		personWindow_search_list.insert(END,person['name'])

def person_search_showPerson_call(ignore=''):root.after(10,person_search_showPerson)
def person_search_showPerson(ignore=''):
	person=personWindow_search_list.get(ACTIVE)
	person=people.get_person(person)
	personWindow_info_name.config(text='Name: '+person['name'])
	personWindow_info_idnumber.config(text='ID Number: '+person['IDNumber'])
	personWindow_info_room.config(text='Room: '+person['room'])
	temp='Tools: '+str(len(person['items']))+'\n'
	for tool in person['items']:
		temp+='\n'+tool[0]+' - '+tool[1]
	personWindow_info_tools.config(text=temp)
	personWindow_info_button.config(state='normal')
	personWindow_modifyPersonButton.config(state='normal')

def person_windowMake(ignore=''):
	global personWindow,personWindow_search_entry,personWindow_search_list,personWindow_addPersonButton,personWindow_modifyPersonButton
	global personWindow_info_name,personWindow_info_idnumber,personWindow_info_room,personWindow_info_tools,personWindow_info_button
	personWindow=Toplevel(root)
	personWindow.protocol("WM_DELETE_WINDOW",person_windowDelete)
	root_button_person.configure(state='disable')
	root_button_admin.configure(state='disable')

	personWindow_search_label=Label(personWindow,text='Search:')
	personWindow_search_label.grid(row=0,column=0)
	personWindow_search_entry=Entry(personWindow)
	personWindow_search_entry.grid(row=0,column=1)
	personWindow_search_entry.bind("<Key>",person_search_searchPeople_call)
	personWindow_search_list=Listbox(personWindow)
	personWindow_search_list.grid(row=1,column=0,columnspan=2,rowspan=1000,sticky=N+S+E+W)
	personWindow_search_list.bind("<Key>",person_search_showPerson_call)
	personWindow_search_list.bind("<Button-1>",person_search_showPerson_call)

	person_search_searchPeople()

	personWindow_info_name=Label(personWindow,text='Name: None Selected')
	personWindow_info_name.grid(row=1,column=2)
	personWindow_info_idnumber=Label(personWindow,text='ID Number: None Selected')
	personWindow_info_idnumber.grid(row=2,column=2)
	personWindow_info_room=Label(personWindow,text='Room: None Selected')
	personWindow_info_room.grid(row=3,column=2)
	personWindow_info_tools=Label(personWindow,text='Tools: 0')
	personWindow_info_tools.grid(row=4,column=2)
	personWindow_info_button=Button(personWindow,text='Alter',state='disable',command=item_windowMake)
	personWindow_info_button.grid(row=5,column=3)

	personWindow_modifyPersonButton=Button(personWindow,text='Modify Person',state='disable',command=personWindow_modifyPerson)
	personWindow_modifyPersonButton.grid(row=6,column=3)
	personWindow_addPersonButton=Button(personWindow,text='New Person',command=personWindow_makePerson_call)
	personWindow_addPersonButton.grid(row=7,column=3)
	
def person_windowDelete(ignore=''):
	personWindow.destroy()
	root_button_person.configure(state='normal')
	root_button_admin.configure(state='normal')

#admin panel - add and remove items
def adminWindow_update_itemList(ignore=''):
	items.update_items()
	adminWindow_search_list.delete(0,END)
	for item in items.items:
		adminWindow_search_list.insert(END,item['name'])

def adminWindow_addItem_call(ignore=''):root.after(1,adminWindow_addItem)
def adminWindow_addItem(ignore=''):
	global addItemWindow
	addItemWindow=Toplevel(adminWindow)
	addItemWindow.protocol("WM_DELETE_WINDOW",adminWindow_addItem_deleteWindow)
	#add entries for name,quantity,used,tags. it must be global so that modify item can hyjack the same window :P

def adminWindow_addItem_deleteWindow(ignore=''):
	addItemWindow.destroy()
	adminWindow_search_entry.config(state='normal')
	adminWindow_search_list.config(state='normal')

def admin_windowMake(ignore=''):
	global adminWindow,adminWindow_info_name,adminWindow_info_quantity,adminWindow_info_used,adminWindow_info_tags
	global adminWindow_search_list,adminWindow_search_entry
	adminWindow=Toplevel(root)
	adminWindow.protocol("WM_DELETE_WINDOW",admin_windowDelete)
	root_button_person.config(state='disable')
	root_button_admin.config(state='disable')

	adminWindow_search_entry=Entry(adminWindow)
	adminWindow_search_entry.grid(row=0,column=0)
	adminWindow_search_list=Listbox(adminWindow)
	adminWindow_search_list.grid(row=1,column=0,rowspan=1000)
	adminWindow_info_name=Label(adminWindow,text="Name: ")
	adminWindow_info_name.grid(row=1,column=1)
	adminWindow_info_quantity=Label(adminWindow,text="Quantity: ")
	adminWindow_info_quantity.grid(row=2,column=1)
	adminWindow_info_used=Label(adminWindow,text="Used: ")
	adminWindow_info_used.grid(row=3,column=1)
	adminWindow_info_tags=Label(adminWindow,text="Tags: ")
	adminWindow_info_tags.grid(row=4,column=1)

	adminWindow_update_itemList()

	adminWindow_button_addItem=Button(adminWindow,text="Add Item",command=None)
	adminWindow_button_addItem.grid(row=1002,column=0)
	adminWindow_button_modifyItem=Button(adminWindow,text='Modify Item',command=None)
	adminWindow_button_modifyItem.grid(row=5,column=2)
	adminWindow_button_removeItem=Button(adminWindow,text='Remove Item',command=None)
	adminWindow_button_removeItem.grid(row=6,column=2)

def admin_windowDelete(ignore=''):
	adminWindow.destroy()
	root_button_person.config(state='normal')
	root_button_admin.config(state='normal')



root=Tk()

global itemWindow,personWindow
itemWindow=None
personWindow=None

root_button_person=Button(root,text="User Checkout",command=person_windowMake)
root_button_person.grid(row=0,column=0)
root_button_admin=Button(root,text="Admin Panel",command=admin_windowMake)
root_button_admin.grid(row=1,column=0)

root.protocol("WM_DELETE_WINDOW",root.quit)
root.mainloop()



exit()
items.get_item('hammer') #must be the full name
items.search_items('wrench')
items.add_item('cresent wrench','1','0','wrench cresent')
items.modify_item('cresent wrench','1','0','wrench cresent')
items.update_items() #gets called at the beginning. should never need to be called as modify_item will keep everything updated

#example that decrements the used quantity unless it is 0
item=items.get_item('hammer') #get the item
print item
if int(item['used'])>0:
	#                  name         quantity          used-1                  tags
	items.modify_item(item['name'],item['quantity'],str(int(item['used'])-1),item['tags'])

#example that increments the used quantity unless it is the same as the available quantity
item=items.get_item('hammer') #get the item
print item
if int(item['quantity'])>=int(item['used']):
	#                  name         quantity          used+1                  tags
	items.modify_item(item['name'],item['quantity'],str(int(item['used'])+1),item['tags'])
