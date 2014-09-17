import os

#magic in here
#see people to see the concept of use

class items:
	def __init__(self):
		self.neededAttributes={'used':"0",
							'premiumStatus':'0',
							'name':'None',
							'tags':'',
							'price':'5.0',
							"daysAllowed":'4',
							'quantity':'1'
							}
		self.update_items()

	def __iter__(self):
		for item in self.items:
			yield item
	def __getitem__(self,index):
		if type(index)==type(0):
			return self.items[index]
		elif type(index)==type(""):
			for item in self.items:
				if item['name']==index:
					return item
			return None
		raise TypeError("cannont handle "+str(type(index))+ "  :  "+str(index))

	def validateItem(self,item):
		if not type(item)==type({}):item=self[item]
		for x in self.neededAttributes:
			if not x in item: return False
		return True

	def fixInvalidPerson(self,item):
		if not type(item)==type({}):item=self[item]
		for x in self.neededAttributes:
			if not x in item: item[x]=self.neededAttributes[x]
		self.modify_item(item)
		return item

	def update_items(self):
		files=[]
		self.items=[]
		for x in os.walk('items'):
			files=x[2]

		for x in files:
			if not x.split('.')[1]=='info': continue
			self.items.append({})
			self.items[-1]['name']=x.split('.')[0]
			x=open('items/'+x,'r')
			for line in x:
				key=line.split('=')[0]
				value=line.split('=')[1][:-1]
				self.items[-1][key]=value
			if not self.validateItem(self.items[-1]):
				print "invalid item "+self.items[-1]['name']
				self.items[-1]=self.fixInvalidPerson(self.items[-1])

		self.items.sort(key=lambda a: a['name'])

	def getitem(self,name):
		if type(name)==type(""):
			for item in self.items:
				if item['name']==name: return item
			return None
		elif type(name)==type(0):
			return self.items[name]
		else:
			raise TypeError("cannont handle "+str(type(name))+ "  :  "+str(name))

	def search_items(self,term):
		#searches the items for a match in either name OR tags
		if term=='':return self.items
		found=[]
		for item in self.items:
			if term in item['name']: #does it match the name of an item? even partially?
				found.append(item)
				continue #don't check to add a second time

			#look for it to match the tags exclusivly
			exclusive=True
			for x in term.split():
				if not x in item['tags']:
					exclusive=False
					break #found to not match, continue on
			if exclusive==True:
				found.append(item)

		return found #return a list of items found to match

	def modify_item(self,name,quantity=None,used=None,tags=None,daysAllowed=None):
		#update the file
		if type(name)==type("") and quantity:
			temp=open('items/'+name+'.info','w')
			temp.write('quantity='+quantity+'\n')
			temp.write('used='+used+'\n')
			if type(tags)==list:
				temp.write('tags=')
				for tag in tags:
					temp.write(tag+' ')
				temp.write('\n')
			if type(tags)==type('') or type(tags)==type(""):
				temp.write('tags='+tags+'\n')
			temp.write('daysAllowed='+str(daysAllowed)+'\n')
			temp.close()
		elif type(name)==type({}):
			temp=open('items/'+name['name']+'.info','w')
			for x in name:
				if type(name[x])==type(""):temp.write(x+'='+name[x]+'\n')
				else:raise TypeError("connot write to file anything but strings : "+str(x)+'   '+type(x))
			temp.close()
		else:
			raise TypeError("connot deal with "+str(type(name))+"  :  "+ str(name))

		
		self.update_items()
				
	def add_item(self,name,quantity='',used='',tags=''):
		self.modify_item(name,quantity,used,tags) #got lazy, but hey, it does the job

	def delete_item(self,name):
		if type(name)==type({}):
			name=name['name']
		if not type(name)==type(""):
			raise TypeError("Cannot handle type "+str(type(name))+"  --  "+str(name))
		os.remove("items/"+name+'.info')
		for x in xrange(len(self.items)): #remove it from our list so that we dont 
			if self.items[x]['name']==name: 
				del self.items[x]
				break