# Following Instructions from:
# https://pyshark.com/containerize-a-flask-application-using-docker/

# Also flask tutorials
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

# Uploading files
# https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
import os, os.path, random, pathlib
from unzip import UnZipFiles


##### NOTES ######
# You need to stop each container and delete it before recompiling
# You also need to delete the image in docker
# Then in terminal "docker build -t flask-image ."
# The run it "docker run -d -p 80:80 flask-image "
# If it doesn't show running in Docker, click it and see the error log
# PRIVACY: log file is recording raw file names. Will it need to be censored?


app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5000 #limit to 5000 mb's
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

# Global Variables
uniqueID = 0
savedID = 0






@app.route('/')
def index():
    
    # TODO: HOW DO YOU REMEMBER THE CURRENT UNIQUE ID WHEN RELOADING A PAGE?? OR PASSING IT ON??
    global uniqueID 
    
    uniqueID = random.randint(1,10000)
    # TODO: read all folder names in uploads and make sure the uniqueID is not a match for one that already exists there
    os.mkdir('uploads/' + str(uniqueID))
    app.config['UPLOAD_PATH'] = 'uploads/' + str(uniqueID)

    # Var's here are the variables in the template that will be updated
    user = {'username': 'DockerMan'}
    title = "Compass - Comparison Of Multiple Projects And Student Schoolwork"
    CURR_DIR = os.getcwd() # current working directory
    


    # this loads/returns the index.html from /templates and fills any variables
    return render_template('index.html', title=title, user=user, location=CURR_DIR)







@app.route('/postUpload')
def postUpload():
    global savedID # The unique ID that now has all the uploaded files

    phrase = "SHE WORKED!!"

    CURR_DIR = os.getcwd() # current working directory
    SCAN_DIR = CURR_DIR + '/uploads/' + str(savedID) # location of zipped files
    
    # Unzip all files, then check that there were no zipped files inside those zipped files
    UnZipFiles(SCAN_DIR) # unzip all files

    #TODO: START HERE!!!! YOU NOW HAVE ALL FILES UPLOADED!!
    # That could have taken some time, so how do we update the user that action is happening??
    # Then scan for #'s of file extensions

    return render_template('postupload.html', intro = phrase, ID = savedID)







@app.route('/', methods=['POST'])
def upload_files():
    global uniqueID
    global savedID

    savedID = uniqueID

    logFileLocation = "uploads/" + str(savedID) + "/log.log"
    logFile = open(logFileLocation, "w")
    logFile.write("Log file for ID " + str(savedID) + "\n\n")
    logFile.write("** UPLOADING FILES **\n")
    

    #### THIS COLLECTS THE STARTER ASSIGNMENT FILE ####
    #uploaded_file = request.files['file'] #just any file type. We wanted the named one
    uploaded_file = request.files.get('baseAssignment') #var is of type 'FileStorage'
    ogfilename = uploaded_file.filename
    ogfilenamesecure = secure_filename(uploaded_file.filename)

    if ogfilenamesecure != '':
        #filename = secure_filename(uploaded_file.filename)
        file_ext = uploaded_file.filename.split('.')[-1] # split extension. -1 to get last entry
        filename = secure_filename("starter_assignment." + str(file_ext)) #rename starter file but keep extenstion
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    


    #### THIS COLLECTS ALL FILES TO BE SCANNED ####
    #uploaded_file = request.files.get('files')
    #print(uploaded_file)

    for uploaded_file in request.files.getlist('files'):
        if uploaded_file.filename != '' and uploaded_file.filename == ogfilename:
            # TODO: log this filename somewhere for debugging. If there are several then there's a problem.
            logFile.write("WARNING: Upload of content file ignored as it had the same name as the original assignment file: ")
            logFile.write(uploaded_file.filename)
            logFile.write("\n")
            pass

        if uploaded_file.filename != '' and uploaded_file.filename != ogfilename:
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename))
            logFile.write("Uploaded: ")
            logFile.write(uploaded_file.filename)
            logFile.write("\n")


    #if filename != '':
    #    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    
    

     

    logFile.write("** UPLOADING COMPLETED **\n")
    logFile.close()
    return redirect(url_for('postUpload'))


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)





if __name__ == '__main__':
    # Needed for dockerizing. Can't user 127.0.0.1 or port 5000
   app.run(host='0.0.0.0', port=80)



