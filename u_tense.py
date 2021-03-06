from bllipparser import RerankingParser
import csv
import pandas as pd

rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)
#tid = []
#tweet = []
def tweet_tense(text):
	#rrp = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)
	x = rrp.simple_parse(text)
	#print(x)
	st = str(x)
	#print(st)
	root = Tree()
	root.pos = "root"
	root.data = "root"
	root.parent = None
	root.children = []
	head = root
	breakpt = ["(", ")"]
	beg = 0
	end = 1
	token = ""
	while end!=len(st):
		while st[end] not in breakpt:
			end += 1
		if st[beg] == "(":
			token = st[beg:end+1]
			words = token.split(" ")
			if len(words)==1:
				node = Tree()
				node.pos = words[0][1:]
				node.data = None
				node.parent = root
				node.children = []
			elif len(words[1])==0:
				node = Tree()
				node.pos = words[0][1:]
				node.data = words[1]
				node.parent = root
				node.children = []
			else:
				node = Tree()
				node.pos = words[0][1:]
				node.data = words[1][:-1]
				node.parent = root
				node.children = []
			root.children.append(node)
			root = node
		if st[beg] == ")":
			root = root.parent
		beg = end
		end = end+1
	#print(head)
	# BFS
	child = head.children
	que = []
	for i in child:
		que.append(i)
	tags = []
	verb_part_words = []
	while(len(que)!=0):
		# print(que[i].pos)
		if que[0].pos == "VP":
			arr = []
			for j in que[0].children:
				arr.append(j)
			for j in arr:
				tags.append(j.pos)
				verb_part_words.append(j.data)
			break
		else:
			child = que[0].children
			que = que[1:]
			for j in child:
				que.append(j)
	print(tags)
	print(words)
	tense_str=-1
	if "will" in verb_part_words or "shall" in words or "would" in verb_part_words or "should" in verb_part_words:
		tense_str = 2 #FUTURE TENSE
	elif "VBD" in tags or "VBN" in tags:
		tense_str = 0 #PAST TENSE
	else:
		tense_str = 1 #PRESENT TENSE
	
	return tense_str

# st = "(S1 (S (SBAR (IN Although) (S (NP (PRP he)) (VP (VBD was) (ADJP (JJ tired))))) (, ,) (NP (PRP he)) (VP (VBD continued) (S (VP (TO to) (VP (VB play)))))))"
class Tree:
	def __init__(self):
		self.pos = None
		self.data = None
		self.parent = None
		self.children = []
	def __str__(self, level=0):
		ret = "\t"*level+repr(self.pos)+"\n"
		for child in self.children:
			ret += child.__str__(level+1)
		return ret

	def __repr__(self):
		return '<tree node representation>'


data2 = pd.read_csv('final_model/Event 1.csv')
tweet = data2['tweet'].tolist()

#with open('Event1.csv','rt')as f:
#    data = csv.reader(f)
#    for row in data:
#        tweet.append(row[1])
#        tid.append(row[0])
#tweet = tweet[603:]
# print(tweet[0])


#tid = tid[1:]
# print(tweet[0])
#result = []
#ip = []
for i in range(len(tweet)):
	# # print(tweet[i])
	# temp = tweet[i].split('.')
	# print(temp)
	temp = tweet[i]
	temp = temp.split('http')
	temp1 = temp[0].replace('#',"").replace('@', "")
	sen = temp1
	print(i)
	ans = tweet_tense(sen)
	data2['tense'][i] = ans
	print(ans)

    #ip.append(sen)
    # print(sen)

data2.to_csv('final_model/Event 1.csv', index=False)
#with open('tense_event1.csv', mode='a') as file:
#    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    for i in range(len(result)):
#        writer.writerow([tid[i], ip[i], result[i]])

#print(result)
