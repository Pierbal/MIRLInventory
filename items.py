import os

class items:
	def __init__(self):
		self.items=[]
		self.update_items()
	def update_items(self):
		files=[]
		self.items=[]
		for x in os.walk('items'):
			files=x[2]

		for x in files:
			self.items.append({})
			self.items[-1]['name']=x[:-5]
			x=open('items/'+x,'r')
			for line in x:
				key=''
				value=''
				while(True): #get the key from the front of the line
					if line[0]=='=':break
					key+=line[0] #add to the key
					line=line[1:] #already got this letter, delete it
				line=line[1:] #delete the =
				while(True):
					if line[0]=='\n':break
					value+=line[0]
					line=line[1:]
				self.items[-1][key]=value

	def get_item(self,name):
		for item in self.items:
			if item['name']==name: return item

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

	def modify_item(self,name,quantity,used,tags):
		#update the file
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
		
		foundTheItem=False
		for x in self.items: #see if we are updating an item
			if x['name']==name:
				foundTheItem=True
				x['quantity']=quantity
				x['used']=used
				if type(tags)==list:
					x['tags']=''
					for tag in tags:
						x['tags']+=tag+' '
				if type(tags)==type('') or type(tags)==type(""):
					x['tags']=tags
				break #don't look for other items, we already found it
		if foundTheItem==False: #nope, new item, so lets add it to the list
			self.items.append({})
			self.items[-1]['name']=name
				
	def add_item(self,name,quantity,used,tags):
		self.modify_item(name,quantity,used,tags) #got lazy, but hey, it does the job
