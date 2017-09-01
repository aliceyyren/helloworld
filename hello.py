# -*- coding:utf-8 -*-
import os
from flask_mongoengine import MongoEngine
from flask_mail import Mail, Message
from flask import Flask,render_template,session,redirect,url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_moment import Moment
from wtforms.validators import Required,Length,Email,NumberRange
from wtforms import SubmitField,StringField,IntegerField,SelectField,PasswordField,TextAreaField,DateField,FileField

app=Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['MONGODB_SETTINGS'] = {'db':'test','host':'172.17.60.101','port': 27017}
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'ryy1129@126.com'
app.config['MAIL_PASSWORD'] = '787988si'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[HelloWorld]'
app.config['FLASKY_MAIL_SENDER'] = 'AliceTest<ryy1129@126.com>'

mail=Mail(app)
mdb = MongoEngine(app) 
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
PASTEBIN_LANGUAGES=[('eee','sss'),('22',2),('3s',1)]


class User(mdb.Document): 
    name = mdb.StringField()
    email=mdb.EmailField()
    content=mdb.StringField()
    def __str__(self):
        return "name:{}-email:{}-content:{}".format(self.name,self.email,self.content)


class newform(FlaskForm):
	name=StringField('name',validators=[Required()])
	#password=PasswordField('password',validators=[Length(min=5, max=6)])
	#text=TextAreaField('Text')
	#Date=DateField('Date',format='%Y-%m-%d')
	#age=IntegerField('age',validators=[NumberRange(min=16, max=70)])
	#language=SelectField('Programming Language', choices=PASTEBIN_LANGUAGES)
	email=StringField('email',validators=[Email()])
	submit=SubmitField('submit')

class userform(FlaskForm):
	content=TextAreaField(u'正文', validators=[Required(u'说点什么')])
	save=SubmitField('Save')


def send_mail():
	msg=Message('test',sender=app.config['FLASKY_MAIL_SENDER'],recipients=['ryy1129@126.com'])
	msg.body='test body'
	msg.html='<b>测试邮件</b>'
	mail.send(msg)



# @app.route('/',methods=['GET', 'POST'])
# def index():
# 	form=newform()
# 	if form.validate_on_submit():
# 		name=form.name.data
# 		user = User(name = name)
# 		user.save()
# 		send_mail()
# 			#session['name']=form.data.name
# 		return '测试测试'
# 	#return render_template('index.html', form=form,name=session.get('name'))
# 	return render_template('index.html', form=form)

# @app.route('/',methods=['GET', 'POST'])
# def index():
# 	form=newform()
# 	if form.validate_on_submit():
# 		old_name=session.get('name')
# 		name=form.name.data
# 		email=form.email.data
# 		if old_name!=name:
# 			user = User(name=name,email=email)
# 			user.save()
# 			#send_mail()
# 			session['name']=form.name.data
# 			return redirect(url_for('mypage',name=name, _external=True))
# 		else:
# 			flash('you input same name')
# 	return render_template('index.html', form=form,name = session.get('name'))


@app.route('/',methods=['GET', 'POST'])
def index():
	form=newform()
	if form.validate_on_submit():
		old_name=session.get('name')
		name=form.name.data
		email=form.email.data
		user = User(name=name,email=email)
		user.save()
		#send_mail()
		session['name']=form.name.data
		return redirect(url_for('mypage',name=name, _external=True))
	return render_template('index.html', form=form,name = session.get('name'))

@app.route('/user/<name>',methods=['GET', 'POST'])
def mypage(name):
	uform=userform()
	if uform.validate_on_submit():
		content=uform.content.data
		user=User(content=content)
	 	User.objects(name=name)[0].update(content=content)	
	return render_template('mypage.html',uform=uform)
	#return '<h1>hello%s</h1>'%User.objects(name=name)[0].email


# @app.route('/user/<name>',methods=['GET'])
# def mypage(name):
# 	uform=userform()
# 	return '<h1>hello %s<h1>' %name



if __name__=='__main__':
	manager.run()