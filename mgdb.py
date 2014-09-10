#coding:utf-8
from pymongo import MongoClient
import config

class Mgdb:
	#一些默认变量，类变量，db的ip,port,和默认db名字
	MG_HOST = config.MONGODB_HOST
	MG_PORT = config.MONGODB_PORT
	DEFAULT_DB_NAME = config.DEFAULT_DB_NAME
	DEFAULT_COLLECTION_NAME = config.DEFAULT_COLLECTION_NAME
	def __init__(self):
		#创建数据库链接
		self.client = MongoClient(Mgdb.MG_HOST,Mgdb.MG_PORT)

	#-------------db-----------
	#是否存在?
	def has_db(self,db_name=""):
		result = {'result':False,'reason':'','db':None}
		#所有db的列表
		all_db_list = self.client.database_names()
		if db_name in all_db_list:
			result['result'] = True
			result['reason'] = "yes we hava"
			return result
		else:
			result['reason'] = "no this db"
			return result
	#获取db对象		
	def get_db(self,db_name):
		result = {'result':False,'reason':'get db success','db':None}
		#先判断是否存在，存在就返回对象
		x = self.has_db(db_name)
		if x['result'] == True:
			result['db'] = self.client[db_name]
			result['result'] = True
			return result
		else:
			result['reason'] = x['reason']
			return result

	#所有db
	def all_db(self):
		result = {'result':False,'reason':'list all db seccess'}
		all_db_list = self.client.database_names()
		result['db'] = all_db_list
		result['result'] = True
		return result

	#创建db
	def create_db(self,db_name=DEFAULT_DB_NAME):
		result = {'result':False,'reason':'create db success','db':'db object'}
		db = self.client[db_name]
		#为什么要马上创建集合？不创建集合不能算真正创建db,但是调用自己写的方法前提是要存在数据库,死循环啊
		db.create_collection('init')
		result['result'] = True
		result['db'] = db
		return result
	#删除
	def del_db(self,db_name):
		result = {'result':False,'reason':'no this db'}
		if self.has_db(db_name)['result'] == True:
			#删除db
			self.client.drop_database(db_name)
			result['result'] = True
			result['reason'] = "del db success"
			return result
		else:
			return result
	#-------------collection-----------
	#是否有collection
	def has_collection(self,col_name,db_name=DEFAULT_DB_NAME):
		result = {'result':False,'reason':'no this collection'}
		all_col_list = None
		x = self.get_db(db_name)
		if x['result']:
			all_col_list = x['db'].collection_names()
			if col_name in all_col_list:
				result['result'] = True
				result['reason'] = "find it"
				return result
			else:
				result['reason'] = "no this collections"
				return result
		#没有这个db
		else:
			result['reason'] = x['reason']
			return result
	#获得coll对象
	def get_collection(self,col_name,db_name=DEFAULT_DB_NAME):
		result = {'result':False,'reason':'success return this collection','collections':None}
		#是否有这个集合?
		x = self.has_collection(col_name,db_name)
		if x['result']:
			db = self.get_db(db_name)
			col = db['db'][col_name]
			result['result'] = True
			result['collections'] = col 
			return result
		else:
			result['reason'] = x['reason']
			return result


	#所有collection
	def all_collection(self,db_name=DEFAULT_DB_NAME):
		result = {'result':False,'reason':'some reason','collections':None}
		x = self.get_db(db_name)
		if x['result']:
			result['result'] = True
			result['reason'] = "all here"
			result['collections'] = x['db'].collection_names()
			return result
		else:
			return result
	#创建collection
	def create_collection(self,col_name,db_name=DEFAULT_DB_NAME):
		result = {'result':False,'reason':'some reason'}
		x = self.get_db(db_name)
		db = None 
		if x['result']:
			#数据库对象
			db = x['db']
			#给数据库创建集合，并且返回对象
			result['collection'] = db.create_collection(col_name)
			result['result'] = True
			result['reason'] = "create success"
			return result
		else:
			#没有这个db的情况
			result['reason']=x['reason']
			return result
	#删除collection
	def del_collection(self,col_name,db_name=DEFAULT_DB_NAME):
		result = {'result':False,'reason':'some reason'}
		db = None
		#保证数据库存在和集合都存在才删除
		x = self.get_db(db_name)
		y = self.has_collection(col_name)
		if x['result']:
			if y['result']:
				db = x['db']
				db.drop_collection(col_name)
				result['result'] = True
				result['reason'] = "drop collection success"
				return result
			else:
				result['reason'] = y['reason']
				return result
		else:
			result['reason'] = x['reason']
			return result
	#改 collection
	def rename_collection(self,db_name=DEFAULT_DB_NAME,old_col_name=None,new_col_name=None):
		result = {'result':False,'reason':'some reason'}
		pass

	#-------------documents-----------
	#是否有document
	def has_document(self,doc_key,col_name=DEFAULT_COLLECTION_NAME,db_name=DEFAULT_DB_NAME):
		result = {'result':False,'reason':'some reason'}
		pass

	#统计document条目
	def count_document(self,doc_key={},col_name=DEFAULT_COLLECTION_NAME,db_name=DEFAULT_DB_NAME):
		result = {'result':False,'reason':'some reason','count':0}
		col = None
		x = self.get_collection(col_name,db_name)
		if x['result']:
			col = x['collections']
			#获取所有符合数据,不过返回是对象
			y = col.find(doc_key)
			result['result'] = True
			result['reason'] = "count done"
			#统计条目
			result['count'] = y.count() 
			return result
		else:
			result['reason'] = x['reason'] 
			return result
	#增　document
	def insert_document(self,doc_dict,col_name=DEFAULT_COLLECTION_NAME,db_name=DEFAULT_DB_NAME):
		result = {'result':False,'reason':'some reason'}
		demo = {'title':"new post",'author':"yg",'body':"xxxxxxxxxxx",'time':"2014-7-25"}
		col = None
		x = self.get_collection(col_name,db_name)
		if x['result']:
			col = x['collections'] 
			col.insert(doc_dict)
			result['result'] = True
			result['reason'] = "Ok insert success"
			print "insert db ok "
			return result
		else:
			result['reason'] = x['reason'] 
			return result

	#删　document
	def del_document(self,doc_key,col_name=DEFAULT_COLLECTION_NAME,db_name=DEFAULT_DB_NAME,lock=True,multi=False):
		result = {'result':False,'reason':'some reason'}
		col = None
		x = self.get_collection(col_name,db_name)
		if x['result']:
			col = x['collections']
			#如果lock=true　只允许用__id的方式删除
			if lock == True:
				#看看传过来的命令是否含有_id
				if doc_key.has_key("_id"):
					y = col.remove(doc_key)
					#查看返回删除条目判断是否成功
					if y['n'] != 0:
						result['reason'] = "del success and del %s " % y['n']
						result['result'] = True
						return result
					else:
						result['reason'] = "not math doc"
						return result
				else:
					result['reason'] = "lock is true can del by _id only "
					return result
			#安全lock关闭，自由删除
			else:
				#multi开始是否删除所有匹配？默认之删除第一条匹配
				y = col.remove(doc_key,multi=multi)
				if y['n'] != 0:
					result['reason'] = "del success and del %s " % y['n']
					result['result'] = True
					return result
				else:
					result['reason'] = "not math doc"
					return result
		else:
			result['reason'] = x['reason'] 
			return result

	#改 document
	def update_document(self,old_doc,new_doc,col_name=DEFAULT_COLLECTION_NAME,db_name=DEFAULT_DB_NAME, multi=False):
		result = {'result':False,'reason':'some reason'}
		#db.test.update({"x": "y"}, {"$set": {"a": "c"}})
		col = None
		#统计修改前后new_doc的数量变化，确定修改成功
		before_nunmber = self.count_document(new_doc,col_name,db_name)['count']
		x = self.get_collection(col_name,db_name)
		if x['result']:
			col = x['collections']
			#核心修改语句,multi为是否修改所有，默认之修改第一条
			col.update(old_doc,{"$set":new_doc},multi=multi)
			#修改后new_doc的数量
			ofter_number = self.count_document(new_doc,col_name,db_name)['count']
			#前后无变化修改不成功
			if ofter_number == before_nunmber:
				result['reason'] = "update not success"
				return result
			else:
				result['result'] = True
				result['reason'] = "update success"
				return result
		else:
			result['reason'] = x['reason'] 
			return self.get_document(new_doc)



		
	#查 document
	def get_one_document(self,doc_key={},col_name=DEFAULT_COLLECTION_NAME,db_name=DEFAULT_DB_NAME):
		result = {'result':False,'reason':'some reason','documents':{}}
		col = None
		x = self.get_collection(col_name,db_name)
		if x['result']:
			col = x['collections']
			#获取一条最匹配数据
			y = col.find_one(doc_key)
			if not y == None:
				result['result'] = True
				result['reason'] = "find it"
				print y 
				result['documents'] = y 
				return result
			else:
				result['reason'] = "no math document"
				result['documents'] = None
				return result
		else:
			result['reason'] = x['reason'] 
			return result

	#查 document
	def get_document(self,doc_key={},limit=0,skip=0,col_name=DEFAULT_COLLECTION_NAME,db_name=DEFAULT_DB_NAME):
		result = {'result':False,'reason':'some reason','documents':{}}
		col = None
		x = self.get_collection(col_name,db_name)
		if x['result']:
			col = x['collections']
			#获取所有符合数据,不过返回是对象
			if limit != 0:
				y = col.find(doc_key).limit(limit).skip(skip)
			else:
				y = col.find(doc_key)
			if y.count() != 0:
				result['result'] = True
				result['reason'] = "find it"
				#这一步很重要，list(y)才能得到所有符合的列表
				result['documents'] = list(y) 
				return result
			else:
				result['reason'] = "no math document"
				result['documents'] = None
				return result
		else:
			result['reason'] = x['reason'] 
			return result






