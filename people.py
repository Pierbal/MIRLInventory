import os
from datetime import datetime 

class people:
	def __init__(self):
		self.update_people()

	def search_people(self, terms):
		if len(terms)==0:return self.people
		found=[]
		for person in self.people:
			for term in terms.split():
				if term in person['name']:
					found.append(person)
					break
				if term in person['IDNumber']:
					found.append(person)
					break
		return found

	def get_person(self,name):
		for person in self.people:
			if person['name']==name:return person
			if person['IDNumber']==name:return person
		return None

	def __getitem__(self,entry):
		if type(entry)==type(0): #if an integer
			return self.people[entry]
		else:
			return self.get_person(entry)

	def __iter__(self):
		for person in self.people:
			yield person

	def __len__(self):
		return len(self.people)

	def isOverdue(self,item):
		if not type(item)==type([]):
			raise TypeError
		today=datetime.today()
		itemTime=datetime.strptime(item[1],"%m-%d-%Y")
		if (x[2]=='out' or item[2]=='damaged') and itemTime<today:
			return True
		return False

	def overdueItems(self,person=None):
		if person==None:
			print "Will on day return a list of lists that have all people and the assosiated OVERDUE items"
			return
		elif type(person)==type("") or type(person)==type(0): #we already have figured out how to get people by index terms like this so we are using these
			person=self[person]
		if person==None: #it got here which means the person was searched for and not found.
			return None #no person means bad search
		#we are guarenteed a valid person dict now
		overdueItems=[]
		today=datetime.today()
		for x in person["items"]:
			itemTime=datetime.strptime(x[1],"%m-%d-%Y")
			if self.isOverdue(x):
				overdueItems.append(x)
		return overdueItems

	def dueItems(self,person=None):
		if person==None:
			print "Will on day return a list of lists that have all people and the assosiated DUE items, and not past items"
			return
		elif type(person)==type("") or type(person)==type(0): #we already have figured out how to get people by index terms like this so we are using these
			person=self[person]
		if person==None: #it got here which means the person was searched for and not found.
			return None #no person means bad search
		#we are guarenteed a valid person dict now
		dueItems=[]
		for item in person["items"]:
			if item[2]=='out' or item[2]=='damaged':
				dueItems.append(item)
		return dueItems #testing, this will have past items also

	def addPerson(self,IDNumber,keys={}):
		self.modify_person(IDNumber,keys)

	def modify_person(self,IDNumber,keys={}):
		if type(IDNumber)==type({}): #if you pass in a dict then it will do the work still
			temp=open('people/'+IDNumber["IDNumber"]+'.info','w') #NOTE!: IDNumber is really the person dict
			for x in IDNumber:
				if x=='items':
					continue
				temp.write(x+'='+IDNumber[x]+'\n')
			temp.write("items:\n")
			for item in IDNumber["items"]:
				temp.write(item[0]+'='+item[1])+'\n'
			temp.close()
		else:
			temp=open('people/'+str(IDNumber)+'.info','w')
			for x in keys:
				if x=='items': continue
				temp.write(x+'='+keys[x])
			temp.write('items:\n')
			for item in items:
				temp.write(item[0]+'='+item[1]+'\n')
			temp.close()
		self.update_people()

	def update_people(self):
		people=[]
		for x in os.walk('people'):
			people=x[2]
			break
		self.people=[]
		for person in people:
			self.people.append({'items':[]})
			self.people[-1]['IDNumber']=person.split('.')[0]
			temp=open('people/'+person,'r')
			itemsSection=False #flips to true when we find the list of items checked out by the person
			for line in temp:
				if line=='items:\n':
					itemsSection=True
					continue
				if itemsSection==False:	#not the items lines yet
					key=''
					value=''
					key=line.split("=")[0]
					value=line.split("=")[1][:-1] #remember that this will have a newline at the end
					self.people[-1][key]=value
				if itemsSection==True: #format has changed!!!!!! the format is for the items which are always at the end of the file
					item=line.split('=')[0]
					date=line.split('=')[1]
					state=line.split('=')[2][:-1]
					line=line[1:]
					self.people[-1]['items'].append([item,date,state])
				
