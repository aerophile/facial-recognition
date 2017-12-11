from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_wtf.file import FileField, FileRequired,FileAllowed
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
import cv2
import face_recognition
import urllib
import time


#DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
 
class FaceRecogForm(FlaskForm):
    name = TextField(' Name :', validators=[validators.required()])
    url = TextField('Image url:', validators=[validators.required()])
    #photo = FileField('Upload Image',validators=[FileRequired(),FileAllowed(['JPG','jpeg' ,'png'], 'Only Images can be uploaded to Precogniser!')]) #['jpg', 'png']
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = FaceRecogForm(request.form)
 
    print form.errors
    if request.method == 'POST':
        name=request.form['name']
	url=request.form['url']
        
 
        if form.validate():

            #flash('Hello ' + name)
            name = download_image(url)
            draw_face_boundary(name)
            flash(process_image(name))
            
        else:
            flash('All the form fields are required. ')
        

        '''
        if form.validate_on_submit():

            f = form.photo.data
            print "ppinstance path",app.instance_path

            
            filename = secure_filename(f.filtime.time()ename)
            f.save(os.path.join(app.instance_path, 'photos', filename))
           
        else:
            flash(form.errors)
        '''
    return render_template('hello.html', form=form)


def download_image(url):
    extension =  url[-4:]
    img_name = None
    if extension == '.jpg' or extension == '.png' or extension == 'jpeg':
       img_name =  str(time.time())+"_input_image"+extension
       
       urllib.urlretrieve(url, img_name)
    else:
        print "invalid url/non image url"
    return img_name

def draw_face_boundary(name):
    has_face = False
    img = cv2.imread(name,0)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img,1.1,5)
    if (len(faces)>0):
        has_face = True
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.imwrite(name, img)
    return has_face

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
