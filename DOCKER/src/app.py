# Following Instructions from:
# https://pyshark.com/containerize-a-flask-application-using-docker/

# Also flask tutorials
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

# Uploading files
# https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
import os, os.path, random, pathlib, string


from unzip import UnZipFiles
from conversion import OcrPdf
from conversion import WordToTxt
from conversion import ConvertStarterAssignment
from analyse import FilesToScan
from analyse import CheckFileExtensions
from buster import StarterAssignment



##### NOTES ######
# You need to stop each container and delete it before recompiling
# You also need to delete the image in docker
# Then in terminal "docker build -t flask-image ."
# The run it "docker run -d -p 80:80 flask-image "
# If it doesn't show running in Docker, click it and see the error log
# PRIVACY: log file is recording raw file names. Will it need to be censored?


app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5000 #limit to 5000 mb's
#app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

# Global Variables
DEBUG_STATUS = True
uniqueID = "0"
savedID = "0"
USE_ONLY_APPROVED_EXTENSIONS = True # make true if you want to limit file extensions for scanning
APPROVED_EXTENSIONS = [".txt", ".rtf", ".cs", ".py", ".gdscript"] # DON'T ADD DOC OR PDF TO THIS!!






@app.route('/')
def index():
    
    global uniqueID 
    
    # CREATE UNIQUE ID
    uniqueID = ''.join(random.choices(string.ascii_letters + string.digits, k=12))


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
    global USE_ONLY_APPROVED_EXTENSIONS
    global APPROVED_EXTENSIONS
    global DEBUG_STATUS

    listOfFilesToScan = [] # Contains list of a txt and code files to scan
    
    phrase = "Files Successfully Uploaded."

    # Set the working directory ID for future functions.
    CURR_DIR = os.getcwd() # current working directory
    SESSION_DIR = CURR_DIR + '/uploads/' + str(savedID) # location of zipped files
    UPLOAD_DIR = SESSION_DIR + "/assignment_uploads/"
    
    # UNZIP all files, then check that there were no zipped files inside those zipped files
    UnZipFiles(UPLOAD_DIR, SESSION_DIR) # unzip all files

    # Collect all file extensions in a dictonary (do this before converting word/pdf)
    fileExtensionsDict = CheckFileExtensions(SESSION_DIR, UPLOAD_DIR, uniqueID, USE_ONLY_APPROVED_EXTENSIONS, APPROVED_EXTENSIONS)

    # CONVERT TEMPLATE FILE IF NEEDED
    ConvertStarterAssignment(SESSION_DIR)

    # OCR all PDF's
    listOfFilesToScan = OcrPdf(UPLOAD_DIR, SESSION_DIR, listOfFilesToScan) #need to cleanup output location

    # WORD DOC CONVERSION
    listOfFilesToScan = WordToTxt(UPLOAD_DIR, SESSION_DIR, listOfFilesToScan) #need to cleanup output location



    
    # SETUP TEMPLATE ASSIGNMENT IF NEEDED
    templatePresent, originalAssignmentLinesNoWhitespace = StarterAssignment(SESSION_DIR, UPLOAD_DIR)
    
    # COMPLETE LIST OF ALL FILES TO SCAN
    # Currently has word and pdf files only.
    # Add all .rtf and .txt files (if they aren't already in the list)
    # Then add all code files

    listOfFilesToScan = FilesToScan(UPLOAD_DIR, SESSION_DIR, USE_ONLY_APPROVED_EXTENSIONS, APPROVED_EXTENSIONS, listOfFilesToScan)

    if DEBUG_STATUS == True:
        logFileLocation = "uploads/" + str(savedID) + "/log.log"
        logFile = open(logFileLocation, "a")
        logFile.write("\n\nFiles To Scan:\n")
        logFile.write(str(listOfFilesToScan))
        logFile.close()


    ###### START HERE:
    # We now have list of all files in list form (listOfFilesToScan) and written to file
    # Also have the inital assignment file stripped of whitespace and each line in a list
    # NOW WE START COMPARING!!!

    # BEGIN BUSTER COMPARISON

    # TODO: Display "ready" screen to user OR load up some sort of status page
    # That could have taken some time, so how do we update the user that action is happening??
    # Look up some flask progress pages












    # PLANNING: HOW ARE WE SHOWING THE RESULTS??
    # This needs to be modular for expansions in data analysis (word/var renaming for example)
    
    # TODO: Show results (this is temp/debugging at the moment)
    # if text/word doc, in the results GIVE NOTES to check for imagine files if they were detected in the zip (.png/.jpg/.jpeg/etc)
    simpleList = []
    totalFiles = 0
    for each in listOfFilesToScan:
        itemToAdd = each.lstrip(UPLOAD_DIR)
        newItem = itemToAdd.rstrip(".txt")
        simpleList.append(newItem)
        totalFiles += 1
    
    return render_template('postupload.html', intro = phrase, ID = savedID, fileList = simpleList, total = totalFiles)







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
    uploaded_file = request.files.get('baseAssignment') #var is of type 'FileStorage'
    ogfilename = uploaded_file.filename
    ogfilenamesecure = secure_filename(uploaded_file.filename)

    # Assignment Template Filename Location
    starterFilename = "uploads/" + str(savedID) + "/assignments.log"
    logStarterFile = open(starterFilename, "w")

    if ogfilenamesecure != '':
        #filename = secure_filename(uploaded_file.filename)
        file_ext = uploaded_file.filename.split('.')[-1] # split extension. -1 to get last entry
        filename = secure_filename("starter_assignment." + str(file_ext)) #rename starter file but keep extenstion
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

        # Make note of template assignment file name in it's own log file for later retrieval
        logStarterFile.write(str(filename))
    else:
        logStarterFile.write("NO STARTER FILE")
    
    logStarterFile.close()

    


    #### THIS COLLECTS ALL STUDENT ASSIGNMENT FILES TO BE SCANNED ####
    # Create upload folder if it doesn't exist
    UPLOAD_DIR = "uploads/" + str(savedID) + '/assignment_uploads' 
    os.mkdir(UPLOAD_DIR)

    # Set upload path for assignment files
    app.config["UPLOAD_PATH"] = UPLOAD_DIR


    for uploaded_file in request.files.getlist('files'):

        # DISABLED: If uploaded file is the same as the original assignment, avoid it
        #if uploaded_file.filename != '' and uploaded_file.filename == ogfilename:
        #    logFile.write("WARNING: Upload of content file ignored as it had the same name as the original assignment file: ")
        #    logFile.write(uploaded_file.filename)
        #    logFile.write("\n")
            

        #if uploaded_file.filename != '' and uploaded_file.filename != ogfilename:
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename))
            logFile.write("Uploaded: ")
            logFile.write(uploaded_file.filename)
            logFile.write("\n")
     
    # Upload Completed
    logFile.write("** UPLOADING COMPLETED **\n")
    logFile.close()

    return redirect(url_for('postUpload'))



@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)





if __name__ == '__main__':
    # Needed for dockerizing. Can't user 127.0.0.1 or port 5000
   app.run(host='0.0.0.0', port=80)



