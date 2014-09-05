#coding:utf-8

class User:

	
	def __init__(self):
		#自己虚构的帐号，还没使用数据库，后期用数据库读取帐号密码
		self.user_and_passwd = [
			{'username':'yanggan','password':'bbs8886342'},
			{'username':"admin",'password':"admin"},
			{'usernmae':"1",'password':'1'},
			{'usernmae':"a",'password':'a'}
			]

	#严重登录的用户密码
	def login(self,username,password):
		#返回结果，根据result来判断是否成功，reason是原因，附带其他信息
		result = {'result':False,'reason':'not','username':username,'email':'user_email'}
		#帐号密码是否为空？
		if not username or not password:
			result['result'] = False
			result['reason'] = "User or Passwd exception"
			return result 
		else:
			#循环判断用户是否存在和密码是否正确
			for i in self.user_and_passwd:
				if i.has_key('username') and username == i['username']:
				#判断密码是否正确？
					if password == i['password']:
						result['result'] = True
						result['reason'] = "login success"
						return result
					else:
						result['result'] = False
						result['reason'] = "Passwd Error"
						return result
			else:
			#循环完了还不返回，那么帐号不存在
				result['result'] = False
				result['reason'] = "The User Not Exist"
				return result

		return result
	#判断是否开放注册
	def can_register(self):
		result = {'result':False,'reason':"暂时不开放注册"}
		return result
	#添加用户
	def add_User(self,username,email,password):
		result = {'result':False,'reason':"原因未知"}
		if self.is_exist(username):
			result['result'] = False
			result['reason'] = "抱歉,用户已经存在"
			return  result
		else:
			#添加帐号信息
			self.user_and_passwd.append({'username':username,'email':email,'password':password})
			print self.user_and_passwd
			result['result'] = True
			result['reason'] = "成功添加"
			return  result
		#默认返回失败信息
		return result

	def del_User(self,username):
		pass
	def rename_User(self,oldname,newname):
		pass
	def all_User(self):
		pass

	#判断用户是否已经存在
	def is_exist(self,username):
		#对值进行比较
		for name in self.user_and_passwd:
			if name['username'] == username:
				return True
		return False




