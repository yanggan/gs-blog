#!env/bin/python
#coding:utf-8
"""

"""
############################导入区
from flask import Flask,render_template,request,session,redirect,url_for,flash
from post import Post # import Class Post write for myself
from user import User # import class User 
from functools import wraps
import os,sys

reload(sys)
sys.setdefaultencoding('utf8')
############################类的什么的对象创建都放在这里
app = Flask(__name__)
app.config.from_object('config')
MyPost = Post() #my post object
blogUser = User()
app.secret_key = app.config['SECRET_KEY']#要使用session必须要secret_key

###########################自己的视图装饰器

#这个试图用于判断每次登录是是否存在用户
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

###########################路由信息放在这里
@app.route('/')
@app.route('/index')
def index():
	give_post = MyPost.get_all_Post()
	#返回index.html页面
	username = session.get('username')
	return render_template(
		'default/index.html',
		title=app.config['BLOG_TITLE'],
		username=username,
		posts=give_post,
		)
#post 

@app.route('/page/',defaults={'page_numbers':1})
@app.route('/page/<int:page_numbers>')
def pages(page_numbers):

	give_post = MyPost.get_all_Post()
	#返回index.html页面
	username = session.get('username')
	posts = MyPost.get_Post_by_Pagenumber(page_numbers)
	print len(posts)
	return render_template(
		'default/index.html',
		title=app.config['BLOG_TITLE'],
		username=username,
		posts=posts
		)

@app.route('/list/')
@app.route('/list')
def list():
	give_post = MyPost.get_all_Post()
	username = session.get('username')
	return render_template(
		'default/list.html',
		title=app.config['BLOG_TITLE'],
		username=username,
		posts=give_post
		)
#制定参数
#@app.route('/post/',defaults={'post_id':1})
@app.route('/post/<int:post_id>')
def show_post(post_id):
	return "这是第 " + str(post_id) + " 篇文章"	

#by permalink
@app.route('/post/<permalink>')
def get_post_by_permalink(permalink):
	username = session.get('username')
	posts = MyPost.get_Post_byPermalink(permalink=permalink)[0]
	print posts
	return render_template('default/single_post.html',username=username,posts=posts)


# edit post
@app.route('/edit/<_id>',methods=['GET','POST'])
@login_required
def edit_post(_id):
	if request.method == "POST":
		dict = {'title':request.form.get('title'),'posts':request.form.get('posts')}
		result = MyPost.update_by_id(_id,new=dict)
		if result:
			return "success"
	post = {}
	posts = MyPost.get_by_id(_id)
	print posts
	return render_template('default/edit.html',posts=posts[0])


#del post
@app.route('/del/<_id>')
@login_required
def del_post(_id):
	result = MyPost.del_Post(_id=_id)
	if result:
		flash('del success')
		return redirect(url_for('list'))
	return "del faied 这是 " + str(_id) + " 文章"	

@app.route('/login',methods=['GET','POST'])
def login():
	error = ""	
	if request.method == 'POST':
		#get the user and passw to userclass to comp
		username = request.form.get('username')
		password = request.form.get('password')
		result = blogUser.login(username,password)
		error = result['reason']
		# result['result'],result['readson'],result['username'],result['email']
		if result['result'] == False:
			error = result['reason']
		else:
			#用户登录成功了哦,把session当字典用,记录用户
			flash("登录成功")
			session['username'] = username
			if request.args.has_key('next') or request.args['next']!=None:
				#redirect to before want to
				return redirect(request.args.get('next'))
			return redirect(url_for('index'))
	elif request.method == 'GET':
		if session.get('username'):
			flash("你已经登录过")
			return redirect(url_for('index'))
	#默认情况下，返回这些
	return render_template('default/login.html',title=app.config['BLOG_TITLE'],error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('username',None)
	flash("注销成功")
	return redirect	(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register():
	#用户请求注册，要验证1.是否存在该用户名字？2.是否开放注册？
	error = None
	can_register = True #是否可以注册?
	#看看是否开放注册?
	if not blogUser.can_register()['result']:
		can_register = blogUser.can_register() #返回字典
	#用户未注销而访问这个页面，
	if session.get('username'):
		#用flash来提示用户
		flash(u'your login now please logout')
		return redirect(url_for('index'))
	#用户提交表单后
	if request.method == "POST":
		#用户表单传过来帐号密码信息
		username = request.form.get('username')
		email = request.form.get('email')
		password = request.form.get('password')
		print request.form.get('xx')
		#有为空的表单吗?
		if username or email or password:
			error = "输入信息异常"
		add_user_result = blogUser.add_User(username=username,email=email,password=password)
		print add_user_result
		#add_user_result 类型为{"result":true,"reason":"xxx"} 
		if add_user_result['result']:
			flash("注册成功")
			return redirect(url_for('login'))
		else:
			#失败就把失败信息填好
			error = add_user_result['reason']

	return render_template('/default/register.html',title=app.config['BLOG_TITLE'],error=error,can_register=can_register)

@app.route('/newpost',methods=['GET','POST'])
@login_required
def new_post():
	username = session.get('username')
	if request.method == 'POST':
		title = request.form.get('title')
		contents = request.form.get('contents')
		blog = {'title':unicode(title),'posts':unicode(contents),'username':session['username']}
		MyPost.new_Post(blog)
	return render_template('/default/newpost.html',title=app.config['BLOG_TITLE'],username=username)

@app.route('/about')
def about():
	return render_template('/default/about.html',title=app.config['BLOG_TITLE']	)
###########################运行区
if __name__ == "__main__":
	app.debug = app.config['DEBUG'] #原来配置文件要这样读
	app.run(host="0.0.0.0",port=5000)