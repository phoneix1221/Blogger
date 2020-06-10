from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from blog.routes import User

class Registrationform(FlaskForm):
    username = StringField('Username ', validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email ', validators=[DataRequired(),Length(min=2,max=30),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=2,max=30)])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign up')

    # fuction to check if user already exist in database compare to username
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError('username already exist please use a different username')


class loginform(FlaskForm):
   
    email=StringField('Email ', validators=[DataRequired(),Length(min=2,max=30),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=2,max=30)]) 
    remember=BooleanField('remember me')   
    submit=SubmitField('login')
     # fuction to check if user already exist in database compare to email
    def validate_email(self,email):
        user=User.query.filter_by(username=email.data).first()
        if user :
            raise ValidationError('email already exist please use a different email')



class createblog(FlaskForm):
   
    Title=StringField('Title ', validators=[DataRequired(),Length(min=2,max=100)])
    short_desc=StringField('Short Description',validators=[DataRequired(),Length(min=2,max=80)]) 
    content=TextAreaField('Content',validators=[DataRequired(),Length(min=2,max=1000000000)])   
    submit=SubmitField('Create')
     # fuction to check if user already exist in database compare to email
    
class update(FlaskForm):
   
    Title=StringField('Title ', validators=[DataRequired(),Length(min=2,max=100)])
    short_desc=StringField('Short Description',validators=[DataRequired(),Length(min=2,max=80)]) 
    content=TextAreaField('Content',validators=[DataRequired(),Length(min=2,max=1000000000)])   
    submit=SubmitField('Update')
