import os
from datetime import datetime,timedelta
from items import items
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from multiprocessing import Process

#this is a complete pain
#save an instance like ppp=people()
#you can then use in for loops like    for person in ppp: print person['name']
#also, you can get people like   self.person[27]    or more straight forward    self.person['Alex Harper']

class people:
	people=[]
	overdueEmailThread=[]
	def __init__(self):
		self.neededAttributes={'name':'JohnDoe',
							"IDNumber":'0000',
							'phoneNumber':'0000',
							'premiumStatus':"0",
							'room':"None",
							'email':"None",
							'emailedLast':'1-1-1999-00-00'
							}
		self.update_people()

	def search_people(self, terms):
		if len(terms)==0:return people.people
		found=[]
		for person in people.people:
			for term in terms.split():
				if term in person['name']:
					found.append(person)
					break
				if term in person['IDNumber']:
					found.append(person)
					break
		return found

	def searchItem(self,item):
		if type(item)==type({}):
			item=item['name']
		if not type(item)==type(""):
			raise TypeError("cannot handle "+str(type(item))+"  :  "+str(item))
		tempPeople=[]
		for person in people.people:
			for x in person['items']:
				if x[0]==item:
					tempPeople.append(person)
		return tempPeople

	def get_person(self,name):
		for person in people.people:
			if person['name']==name:return person
			if person['IDNumber']==name:return person
		return None

	def validatePerson(self,person):
		if not type(person)==type({}):person=self[person]
		for x in self.neededAttributes:
			if not x in person: return False
		for x in xrange(len(person['items'])):
			if len(person['items'][x][1].split('-'))==3: #using the old format
				return False
		return True

	def fixInvalidPerson(self,person):
		if not type(person)==type({}):person=self[person]
		for x in self.neededAttributes:
			if not x in person: person[x]=self.neededAttributes[x]
		for x in xrange(len(person['items'])):
			if len(person['items'][x][1].split('-'))==3: #using the old format
				person['items'][x][1]+=("-00-00")#default the TIME to 0hours and 0mins
		self.modify_person_noUpdate(person) #write changes to file
		return person

	def __getitem__(self,entry):
		if type(entry)==type(0): #if an integer
			return people.people[entry]
		else:
			return self.get_person(entry)

	def __iter__(self):
		for person in people.people:
			yield person

	def __len__(self):
		return len(people.people)

	def isOverdue(self,item):
		if not type(item)==type([]):
			raise TypeError("please pass in an item from a person. i need the date from it")
		today=datetime.today()
		itemTime=datetime.strptime(item[1],"%m-%d-%Y-%H-%M")
		if (item[2]=='out' or item[2]=='damaged') and itemTime<today:
			return True
		return False

	def overdueItems(self,person=None):
		#returns only overdue items
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
			itemTime=datetime.strptime(x[1],"%m-%d-%Y-%H-%M")
			if self.isOverdue(x):
				overdueItems.append(x)
		return overdueItems

	def dueItems(self,person=None):
		#returns the items that are currently checked out, weither or not they are overdue
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
		return dueItems

	def pastItems(self,person=None):
		if person==None:
			print "Will on day return a list of lists that have all people and the assosiated DUE items, and not past items"
			return
		elif type(person)==type("") or type(person)==type(0): #we already have figured out how to get people by index terms like this so we are using these
			person=self[person]
		if person==None: #it got here which means the person was searched for and not found.
			return None #no person means bad search
		pastItems=[]
		for item in person["items"]:
			if not (item[2]=='out' or item[2]=='damaged'):
				pastItems.append(item)
		return pastItems

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
				temp.write(item[0]+'='+item[1]+'='+item[2]+'\n')
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

	def modify_person_noUpdate(self,IDNumber,keys={}):
		#note that this is the exact same as the simular named method above. This IS NECISSARY STILL
		#This is here to fix the problem of there being person duplication when fixing invalid people
		#the method above calls the self.update_people() method and so it parses files twice and adds 
		#more people to the people.people list. This here is functionally identical except that it will
		#NOT call the update method
		if type(IDNumber)==type({}): #if you pass in a dict then it will do the work still
			temp=open('people/'+IDNumber["IDNumber"]+'.info','w') #NOTE!: IDNumber is really the person dict
			for x in IDNumber:
				if x=='items':
					continue
				temp.write(x+'='+IDNumber[x]+'\n')
			temp.write("items:\n")
			for item in IDNumber["items"]:
				temp.write(item[0]+'='+item[1]+'='+item[2]+'\n')
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

	def update_people(self):
		ppp=[]
		for x in os.walk('people'):
			ppp=x[2]
			break
		people.people=[]
		for person in ppp:
			people.people.append({'items':[]})
			people.people[-1]['IDNumber']=person.split('.')[0]
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
					people.people[-1][key]=value
				if itemsSection==True: #format has changed!!!!!! the format is for the items which are always at the end of the file
					item=line.split('=')[0]
					date=line.split('=')[1]
					state=line.split('=')[2][:-1]
					line=line[1:] #remove the line since we got the info already
					people.people[-1]['items'].append([item,date,state])
			if not self.validatePerson(people.people[-1]):
				print "invalid person "+people.people[-1]['name']
				people.people[-1]=self.fixInvalidPerson(people.people[-1])

		#sort people by their name
		people.people.sort(key=lambda a:a['name'])

	def deletePerson(self,person):
		if type(person)==type({}):
			person=person['IDNumber']
		if not type(person)==type(""):
			raise TypeError("Did not send in a usable type "+str(type(person)))
		#can assume we have the idnumber now
		os.remove('people/'+person+'.info')
		for p in xrange(len(people.people)):
			if person==people.people[p]['IDNumber']:
				del people.people[p]
				break

				

	def emailPerson(self,person,message=""):
		#send an email with all information of due items, account info, and overdue items
		self.items=items()
		if not type(person)==type({}): raise TypeError("You MUST send in a person dict")
		message="MIRL CHECKOUT SYSTEM UPDATE EMAIL\nPlease read over the information for correctness\n\n"+person['name']+' - '+person["room"]+'\n'+message+'\n'
		message+="Due Items:\n"
		cost=0
		for x in self.dueItems(person):
			date=x[1][:10] #get a sensible date from the item
			message+="    due "+date+"  --  cost: "+self.items.getitem(x[0])['price']+"  --  "+x[0]+'\n'
			cost+=float(self.items.getitem(x[0])['price'])
		message+='\nCharges Due If Not Returned: '+str(cost)
		message+="\n\nPlease contact mirllabmanager@gmail.com for any questions or concerns\n\n"

		fullMessage=MIMEMultipart()
		fullMessage['From']="mirlcheckoutsystem@gmail.com"
		fullMessage["To"]=person['email']
		fullMessage["Subject"]="MIRL TOOLS UPDATE"
		fullMessage.attach(MIMEText(message,'plain'))

		try:
			server=smtplib.SMTP()
			server.connect('smtp.gmail.com',587)
			server.starttls()
			server.login("mirlcheckoutsystem@gmail.com","labmanager232")
			server.sendmail("mirlcheckoutsystem@gmail.com",person['email'],fullMessage.as_string()) #from,to,message
		except Exception,r:
			print "UNABLE TO SEND EMAIL!!!!"
			print r

	def emailPeopleOverdue(self):
		#emails all people with overdue things
		#special in that it will not freeze the program while emailing the people
		people.overdueEmailThread.append(Process(target=self.__emailPeopleOverdue))
		people.overdueEmailThread[-1].start()
	def __emailPeopleOverdue(self):
		#emails all people with overdue things
		now=datetime.today() #gives back the time now equivilent
		print now
		for person in self:
			if len(self.overdueItems(person))==0:continue #is first so that we dont waste cycles making the datetime if not needed
			last=datetime.strptime(person['emailedLast'],"%m-%d-%Y-%H-%M") #the time the person was emailed last
			print person['name'],'has overdue items'
			if (now-last)>timedelta(hours=4): #if it has been more than 4 hours
				print '\tEmailing',person["name"]
				self.emailPersonOverdue(person) #send the overdue email
				person['emailedLast']=datetime.strftime(now,"%m-%d-%Y-%H-%M") #update the last time emailed to now
				self.modify_person_noUpdate(person)#dont waste cycles updating the list from the HDD since this is a temporary list
		#clean the list of threads so that we can free some memory
		while(len(people.overdueEmailThread)>2):
			for x in xrange(len(people.overdueEmailThread),0,-1):
				if not people.overdueEmailThread[x].is_alive():
					del people.overdueEmailThread[x]

	def emailPersonOverdue(self,person,message=""):
		#send an email with all information of overdue items, account info
		#this is special in that it will not freeze up the program while running the stuff
		people.overdueEmailThread.append(Process(target=self.__emailPersonOverdue,args=(person,message)))
		people.overdueEmailThread[-1].start()#start what we just added
	def __emailPersonOverdue(self,person,message=""):
		#send an email with all information of overdue items, account info
		self.items=items()
		if not type(person)==type({}): raise TypeError("You MUST send in a person dict")
		message="MIRL CHECKOUT SYSTEM UPDATE EMAIL\nPlease read over the information for correctness\n\n"+person['name']+' - '+person["room"]+'\n'+message+'\n'

		message+="Overdue Items :\n"
		for x in self.overdueItems(person):
			date=x[1][:10] #get a sensible date from the item
			message+="    OVERDUE "+date+"  --  cost: "+self.items.getitem(x[0])['price']+"  --  "+x[0]+'\n'
		message+="\nThe items listed above should be returned as soon as possible\nIf the items are not returned soon, you may be liable for charges\n\n\n"

		message+="Due Items:\n"
		cost=0
		overdueCost=0
		for x in self.dueItems(person):
			date=x[1][:10] #get a sensible date from the item
			if self.isOverdue(x):
				message+="    OVERDUE  --  "+date+" - cost: "+self.items.getitem(x[0])['price']+"  --  "+x[0]+'  --  OVERDUE\n'
				overdueCost+=float(self.items.getitem(x[0])['price'])
			else:
				message+="    due "+date+"  --  cost: "+self.items.getitem(x[0])['price']+"  --  "+x[0]+'\n'
			cost+=float(self.items.getitem(x[0])['price'])
		message+='\nCharges Due If Not Returned: '+str(cost)
		message+='\nCharges Due For Overdue Items: '+str(overdueCost)
		message+="\n\nPlease contact mirllabmanager@gmail.com for any questions or concerns\n\n"

		fullMessage=MIMEMultipart()
		fullMessage['From']="mirlcheckoutsystem@gmail.com"
		fullMessage["To"]=person['email']
		fullMessage["Subject"]="MIRL TOOLS UPDATE"
		fullMessage.attach(MIMEText(message,'plain'))

		try:
			server=smtplib.SMTP()
			server.connect('smtp.gmail.com',587)
			server.starttls()
			server.login("mirlcheckoutsystem@gmail.com","labmanager232")
			server.sendmail("mirlcheckoutsystem@gmail.com",person['email'],fullMessage.as_string()) #from,to,message
		except Exception,r:
			print "UNABLE TO SEND EMAIL!!!!"
			print r