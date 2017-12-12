from flask import Flask, render_template, flash, request,redirect,url_for
from wtforms import Form, TextField, TextAreaField,SelectField, validators, StringField, SubmitField
from flask_wtf.file import FileField, FileRequired,FileAllowed
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
import cv2
import face_recognition
import urllib
import time
import pprint

#DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
 
class FaceRecogForm(FlaskForm):
    #name = TextField(' Name :', validators=[validators.required()])
    name = SelectField("Technique", [validators.required()], choices=[("technique 1","Technique 1"),("technique 2","Technique 2")])
    url = TextField('Image url:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = FaceRecogForm(request.form)
 
    print form.errors
    if request.method == 'POST':
        technique = request.form['name']
	url = request.form['url']
        
 
        if form.validate():
            #flash('Hello ' + name)
            print 'Hello ' + technique
            name = download_image(url)
            draw_face_boundary(name)
            message_response = process_image(name)
            #flash(message_response)
            #return show_result(name,message_response) works

    	    #result(name,message_response)
            return render_template('results.html', img_name=name,message_response=message_response)
            
        else:
            flash('All the form fields are required. ')
        

    return render_template('hello.html', form=form)

@app.route("/results/")
def result(name,message_response):
    return render_template('results.html', img_name=name,message_response=message_response)

def download_image(url):
    extension =  url[-4:]
    img_name = None
    if extension == '.jpg' or extension == '.png' or extension == 'jpeg':
       img_name =  str(int(time.time()))+"_input_image"+extension
       
       urllib.urlretrieve(url, img_name)
    else:
        print "invalid url/non image url"
    return img_name

def draw_face_boundary(name):
    has_face = False
    img = cv2.imread(name,0)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    faces = face_cascade.detectMultiScale(img,1.3,5)
    if (len(faces)>0):
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.imwrite(name, img)

            #resize_and_save(name,img,150,50)

            cv2.imwrite("static/"+name,img)
            has_face = True
    return has_face

def resize_and_save(name,cv2_img,width,height,location="static/"):
    '''takes in cv2 image object, resizes and saves it'''
    img = cv2.resize(cv2_img,(width,height))
    cv2.imwrite(location+"resized_"+name,img)
        

def is_kejriwal(name):
    
    pic_ak = face_recognition.load_image_file("static/ak.jpg")
    unknown_picture = face_recognition.load_image_file(name)
    ak_encoding = face_recognition.face_encodings(pic_ak)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_picture)[0]
    results = face_recognition.compare_faces([ak_encoding], unknown_encoding)
    return results[0]
     

def is_modi(name):
    
    pic_nm = face_recognition.load_image_file("static/nm.jpg")
    unknown_picture = face_recognition.load_image_file(name)
    nm_encoding = face_recognition.face_encodings(pic_nm)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_picture)[0]
    results = face_recognition.compare_faces([nm_encoding], unknown_encoding)
    return results[0]

def process_image(name):
    img_response = {}
    img_response["Face Present"]=draw_face_boundary(name)
    img_response["Narendra Modi"]=is_modi(name)
    img_response["Arvind Kejriwal"]=is_kejriwal(name)
    return img_response
     
 
       
 
if __name__ == "__main__":
    app.run()
