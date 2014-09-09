import os
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

	def modify_person(self,name,IDNumber,room,items):
		if type(name)==type({}):
			print "Will be added so can pass a modified dict"
			return
		temp=open('people/'+str(IDNumber)+'.info','w')
		temp.write('name='+name+'\n')
		temp.write('room='+room+'\n')
		temp.write('items:\n')
		for item in items:
			temp.write(item[0]+'='+item[1]+'\n')

	def update_people(self):
		people=[]
		for x in os.walk('people'):
			people=x[2]
		self.people=[]
		for person in people:
			self.people.append({'items':[]})
			self.people[-1]['IDNumber']=person[:-5]
			temp=open('people/'+person,'r')
			itemsSection=False #flips to true when we find the list of items checked out by the person
			for line in temp:
				if line=='items:\n':
					itemsSection=True
					continue
				if itemsSection==False:	
					key=''
					value=''
					while(True):
						if line[0]=='=':
							break
						key+=line[0]
						line=line[1:]
					line=line[1:]
					while(True):
						if line[0]=='\n':
							break
						value+=line[0]
						line=line[1:]
					self.people[-1][key]=value
				if itemsSection==True:
					item=''
					date=''
					while(True):
						if line[0]=='=':
							break
						item+=line[0]
						line=line[1:]
					line=line[1:]
					while(True):
						if line[0]=='\n':
							break
						date+=line[0]
						line=line[1:]
					self.people[-1]['items'].append([item,date])
				
