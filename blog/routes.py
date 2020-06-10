from blog.models import User,Post
from flask import render_template,url_for,flash,redirect
from blog.forms import Registrationform,loginform,createblog,update
from blog import app
from blog import bcrypt
from blog import db
from flask_login import login_user,current_user,logout_user,login_required
from mailjet_rest import Client
import os
import requests
import urllib, json
from datetime import date





data=[{'blog_title':'first blog',
        'blog_date':'12/10/2019',
        'blog_author':'mayank',
         'blog_content':'this is second blog'
        },
        {
        'blog_title':'second blog',
        'blog_date':'20/10/2019',
        'blog_author':'atul',
        'blog_content':'this is second blog'
        } 
    ]


@app.route("/",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=loginform()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash(f'login successfully for user {form.email.data}!','success')
            return redirect(url_for('home'))
        else:
            flash(f'login failed please enter correct Email and Password !','danger')
    return render_template('login.html',form=form)

    
 

@app.route("/register", methods=['POST','GET'])
def register():
   
        form=Registrationform()
        if form.validate_on_submit():
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user=User(username=form.username.data,email=form.email.data,password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created successfully for user {form.username.data}!','success')
            return redirect(url_for('login'))
        return render_template('register.html',form=form)

@app.route("/home",methods=['POST','GET'])
def home():
    if current_user.is_authenticated:
        x=requests.get('http://localhost:1337/Posts')
        print(x.json())
        data=x.json()

        return render_template('home.html',data=data)
    else :
        return redirect(url_for('login'))
         


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
   return render_template('account.html',title="Account")


@app.route("/foo",methods=['GET', 'POST'])
def sendmail(): 
    api_key = 'ed7c842e32a26a4c2d6dc220c784d0cc'
    api_secret = 'c6a0c6ba6461173404196a258ae02739'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
         {
        "From": {
            "Email": "mayankjoshi996007@gmail.com",
            "Name": "Mayank"
         },
        "To": [
             {
            "Email": "mayankjoshi996007@gmail.com",
            "Name": "MJ"
            }
        ],
        "Subject": "testing my app",
        "TextPart": "My first Mailjet email",
        "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())

    return render_template('home.html',data=data)



@app.route("/create", methods=['POST','GET'])
@login_required
def create():
    form=createblog()
    url = 'http://localhost:1337/Posts'
    today = date.today()
    
   
    if form.validate_on_submit():
        Title=form.Title.data
        shortdesc=form.short_desc.data
        content=form.content.data
        myobject={
                'Title': Title,
                'shortdesc': shortdesc,
                'content': content, 
                'by': current_user.username,
                'Date':today
                }
        x = requests.post(url, data = myobject)
        print(x.text)
        flash(f'Post created Succesfully!','success')

        

      
    return render_template('create.html',form=form)


@app.route("/mypost", methods=['POST','GET'])
@login_required
def mypost():
    if current_user.is_authenticated:
        url='http://localhost:1337/Posts?by='+current_user.username
        x=requests.get(url)
        print(x.json())
        data=x.json()
        return render_template('mypost.html',data=data)
    else :
        return redirect(url_for('login'))



@app.route("/Edit/<id>", methods=['POST','GET'])
@login_required
def Edit(id):
    form=update()
    url='http://localhost:1337/Posts?id='+id
    x=requests.get(url)
    data=x.json()
    
    today = date.today()
    if current_user.is_authenticated:

        if form.validate_on_submit():
            Title=form.Title.data
            shortdesc=form.short_desc.data
            content=form.content.data

            url='http://localhost:1337/Posts/'+id
            myobject={
                    'Title': Title,
                    'shortdesc': shortdesc,
                    'content': content, 
                    'by': current_user.username,
                    'Date':today
                    }
            x=requests.put(url,data=myobject)
            flash(f'Post Updated Succesfully!','success')
            return redirect(url_for('home'))
        return render_template('Update.html',form=form,data=data)
    else :
        return redirect(url_for('login'))


@app.route("/Delete/<id>", methods=['POST','GET'])
@login_required
def Delete(id):
    
    if current_user.is_authenticated:
        url='http://localhost:1337/Posts/'+id
        x=requests.delete(url)
        print(x.text)
        flash(f'Post Deleted Succesfully!','success')
        return redirect(url_for('home'))
    else :
        return redirect(url_for('login'))


@app.route("/show/<id>", methods=['POST','GET'])
@login_required
def show(id):
    
    if current_user.is_authenticated:
        url='http://localhost:1337/Posts/'+id
        x=requests.get(url)
        datau=x.json()
        print("data is")
        print(data)

        return render_template('blog.html',data = datau)
    else :
        return redirect(url_for('login'))



