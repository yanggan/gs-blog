#coding:utf-8
#this file  class use about posts 
from mgdb import Mgdb
import time
import config
import markdown2
from bson.objectid import ObjectId


class Post:
	def __init__(self):
		self.db = Mgdb()

	def std_post(self,post):
		start = post 
		"""
		std = {
			'title':"",
			'author':"",
			'post':'',
			'tags':"",
			'time':"",
			'username':''
			'permalink':''
			'id':1
		}
		"""
		if not start.has_key('time') or start['time'] == None:
			start['time'] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
		else:
			start['last_mod_time'] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
		if not start.has_key('author') or start['author'] == None:
			start['author'] = config.AUTHOR
		if not start.has_key('title') or start['title'] == None:
			start['title'] = "New Post"
		if not start.has_key('posts') or start['posts'] == None:
			start['post'] = "Hello flask"
		if not start.has_key('username') or start['username'] == None:
			start['username'] = "admin"
		if not start.has_key('id') or start['id'] == None:
			start['id'] = self.db.count_document()['count'] + 1 
		if not start.has_key('permalink') or start['permalink'] == None:
			start['permalink'] = ""+ time.strftime("%Y-%m-%d-", time.localtime())+ start['title'].replace(' ',"-")
		return start


	def add_markdown(self,post_list):
		#add markdown key
		if post_list == None:
			return post_list 
		start = []
		for post in post_list:
			post['mk_posts'] = markdown2.markdown(post.get('posts'))
			start.append(post)
		return start

	#查
	def get_all_Post(self):
		all_post = [
			{'title':"This is my First Post",'contents':"im am super man"},
			{'title':"This is my sec Post",'contents':"just a test"},
		]
		post = self.db.get_document({})
		post_list = [{"title":"hello",'posts':'test'}]
		result_posts = []
		if post['result']:
			post_list = post['documents']
			for post in post_list:
				post['mk_posts'] = markdown2.markdown(post.get('posts','no'))
				result_posts.append(post)
			return result_posts
		else:
			print "no data"
			return [{"title":"hello",'posts':'<h1>xxxxxxxxxxxxx</h1>'}]
	#查id
	def get_Post_byID(self,id=None):
		pass
	#search by permalink
	def get_Post_byPermalink(self,permalink):
		post = self.db.get_document({'permalink':permalink})['documents']
		posts = self.add_markdown(post)
		if posts != None:
			return posts
		else:
			return [{'title':'no this post'}]
	#增
	def new_Post(self,post_contents_dict={}):
		result = {'result':False,'reason':"sucess put in db"}
		start = post_contents_dict
		if start['posts'] != u'' and start['title'] != u'':
			print self.std_post(post_contents_dict)
			self.db.insert_document(self.std_post(post_contents_dict))
		else:
			print "wuxiao data"
			return result

	#删
	def del_Post(self,_id=None):
		print _id
		try:
			# use db del
			result = self.db.del_document({'_id':ObjectId(_id)})
			if result['result']:
				print result['reason']
				return True
			else:
				return False
		except Exception:
			print "objectid error"
			return False
	#
	def get_Post_by_Pagenumber(self,current_page,limit=config.PAGE_NUMBERS,dict={}):
		#pass documents with get documents
		if current_page == 1:
			skip = 0
		elif current_page > 1: 
			skip = (current_page -1) * limit 
			print skip
		else:
			print "error"

		print "current_page:",current_page
		print "limit:",limit
		print "skip:",skip
		post = self.db.get_document(dict,limit=limit,skip=skip)['documents']
		posts = self.add_markdown(post)
		print posts
		print "list length:",len(posts)
		if posts != None:
			return posts
		else:
			return [{'title':'no this post'}]
	#get by _id
	#search by permalink
	def get_by_id(self,id):
		try:
			post = self.db.get_document({'_id':ObjectId(id)})['documents']
			posts = self.add_markdown(post)
			if posts != None:
				return posts
			else:
				return [{'title':'no this post'}]
		except Exception:
			print "error"
			return [{'title':'no this post'}]
	def update_by_id(self,id,new={}):
		try:
			new = self.std_post(new)
			result = self.db.update_document({'_id':ObjectId(id)},new)
			result = True
			if True:
				return True
			else:
				return False
		except Exception:
			print "objectid error"
			return [{'title':'no this post'}]
