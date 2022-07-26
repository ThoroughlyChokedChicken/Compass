import os, os.path, subprocess, sys

CURR_DIR = os.getcwd() # current working directory
logFileLocation = CURR_DIR + "/dockerlog.log"
logFile = open(logFileLocation, "w")

#package = "pdftotext"
#try:
#    __import__(package) # For PDF OCR conversion
#except ImportError:
#    logFile.write("System doesn't have needed modules. Installing now...\n")
#    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
#    logFile.write("One time install of needed modules complete. Continuing with program...\n")

import pdftotext # needed for parsing text
logFile.write("pdftotext successfully installed.\n")

import docx2txt
logFile.write("docx2txt successfully installed.\n")

logFile.close()

# Global Variables
DEBUG_STATUS = True # extra records in the log files







# NOTES
# in terminal to convert a PDF to formatted text file try:
# pdftotext -layout INPUT.pdf OUTPUT.txt

def ConvertTemplateAssignment():
    pass
    # TODO: config call this if template assignment is a PDF



### CONVERT ALL WORD DOC'S TO TXT ###
def WordToTxt(SCANNING_DIR, TEXTDIR):

    global DEBUG_STATUS

    # Log to file
    logFileLocation = SCANNING_DIR + "/log.log"
    logFile = open(logFileLocation, "a")
    logFile.write("** BEGIN WORD DOC CONVERSION **\n")
    
    ### Begin Output Starting With Working Directories
    for root, dirs, files in os.walk(SCANNING_DIR):
        # select file name
        for file in files:
            
            # check the extension of files
            if file.endswith(".docx") or file.endswith(".doc"):
                if DEBUG_STATUS == True:
                    logFile.write(file)
                
                if file[0] != "~":

                    #fileWithLocation = SCANNING_DIR + "/" + file
                    fileWithLocation = str(os.path.join(root, file))

                    if DEBUG_STATUS == True:
                        logFile.write(fileWithLocation + "\n")
                    
                    text = docx2txt.process(fileWithLocation)
                    
                    # TODO: UPDATE OUTPUT LOCATION

                    # output file location
                    newFileName = SCANNING_DIR + "/" + file + ".txt" 
                    with open(newFileName, "w") as text_file:
                        print(text, file=text_file)

    
    logFile.write("** COMPELTED WORD DOC CONVERSION **\n")
    logFile.close()
        
        






### OCR ALL PDF's ###

def OcrPdf(SCANNING_DIR, TEXTDIR):

    global DEBUG_STATUS

    logFileLocation = SCANNING_DIR + "/log.log"
    logFile = open(logFileLocation, "a")
    logFile.write("** BEGIN OCR'ING PDF FILES **\n")
    logFile.close()


    # Converts all PDF documents into TXT docs and locates them in the TXT folder
    counter = 0

    for root, dirs, files in os.walk(SCANNING_DIR):
        # select file name
        for file in files:
            
            # check the extension of files
            if file.endswith('.pdf'):
                
                pdfFileToConvert = str(os.path.join(root, file))
                
                txtFileOutput = "\"" + TEXTDIR + "/output" + str(counter + 1) + ".txt" + "\""
                #print("txtFileOutput: " + txtFileOutput + "\n")

                # Command sequence that needs to be run by os.system
                stringForSubprocess = "pdftotext -layout \"" + pdfFileToConvert + "\" " + txtFileOutput
              
                # If debugging, log every attempted command
                if DEBUG_STATUS == True:
                    logFileLocation = SCANNING_DIR + "/log.log"
                    logFile = open(logFileLocation, "a")
                    logFile.write(stringForSubprocess + "\n")
                    logFile.close()


                os.system(stringForSubprocess) # Run the python command
        
                counter += 1
    
    # Completed OCR
    logFile = open(logFileLocation, "a")
    logFile.write("** COMPLETED OCR'ING PDF FILES **\n")
    logFile.close()


