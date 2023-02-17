import sys, os, os.path, zipfile # Needed to unzip files

# Global Variables
DEBUG_STATUS = False # extra records in the log files


def UnZipFiles(SCANNING_DIR, SESSION_DIR):
    
    global DEBUG_STATUS

    logFileLocation = SESSION_DIR + "/log.log"
    logFile = open(logFileLocation, "a")
    logFile.write("\n** UNZIPPING FILES STARTED **\n")
    logFile.close()
  
  
    zipFilesToUnzip = [] # will house fill file path of all zip files to unzip
    
    zipFilesToUnzip = ScanForZipFiles(SCANNING_DIR, SESSION_DIR, zipFilesToUnzip) # 1st Scan
    PerformUnZip(SCANNING_DIR, SESSION_DIR, zipFilesToUnzip) # Actually Unzip

    logFileLocation = SESSION_DIR + "/log.log"
    logFile = open(logFileLocation, "a")
    logFile.write("First scan and unzip complete.\n")

    
    listOfKnownZips = zipFilesToUnzip # What we know is present
    logFile.write("Initalizing second scan...\n")
    logFile.close()
    zipFilesToUnzip = ScanForZipFiles(SCANNING_DIR, SESSION_DIR, zipFilesToUnzip) # 2nd Scan of ALL zips present

    # Loops to catch zip files inside other zip files
    while(True):
        if listOfKnownZips == zipFilesToUnzip:
            logFile = open(logFileLocation, "a")
            logFile.write("No recursive zip files found. Done unzipping.\n")
            logFile.close()
            break
        else:
            logFile = open(logFileLocation, "a")
            logFile.write("Further zip files found!\n")
            
            # TODO: Currenty this reunzips everything. If needed for performance, isolate only the new zip files and only unzip those

            listOfKnownZips = zipFilesToUnzip
            logFile.write("Scanning for further zip files.\n")
            logFile.close()

            zipFilesToUnzip = ScanForZipFiles(SCANNING_DIR, zipFilesToUnzip) # Additional Scans
            logFile = open(logFileLocation, "a")
            logFile.write("Unzipping additional files.\n")
            logFile.close()
            PerformUnZip(SCANNING_DIR, zipFilesToUnzip) # Actually Unzip


    logFile = open(logFileLocation, "a")
    logFile.write("** UNZIPPING COMPLETED **\n\n")
    logFile.close()

    #### LOG ALL FILES
    COMPLETE_FILE_LIST = []
    for root, dirs, files in os.walk(SCANNING_DIR):
    # select file name
        for file in files:
            COMPLETE_FILE_LIST.append(file)

    return COMPLETE_FILE_LIST











def ScanForZipFiles(SCANNING_DIR, SESSION_DIR, knownZipFiles):
    global DEBUG_STATUS

    logFileLocation = SESSION_DIR + "/log.log"
    logFile = open(logFileLocation, "a")
    logFile.write("Beginning Scan of Files\n")
    
  
  
    zipFilesToUnzip = [] # will house fill file path of all zip files to unzip
    
    ## RECORD ALL ZIPPED FILES TO A LIST (zipFilesToUnzip)
    for root, dirs, files in os.walk(SCANNING_DIR):
    # select file name
        for file in files:
        
            

        # check the extension of files
            #if file.endswith(".zip") and file not in knownZipFiles:
            if file.endswith(".zip"):
                
                # Note full path to zip
                fullZipPath = root + "/" + file
                if DEBUG_STATUS == True:
                    logFile.write("Found zip file: " + fullZipPath + "\n") # List all files to be unzipped

                zipFilesToUnzip.append(fullZipPath) # Add all files you need to scan to a list

    logFile.write("Scanning task completed\n")
    logFile.close()

    return zipFilesToUnzip




def PerformUnZip(SCANNING_DIR, SESSION_DIR, zipFilesToUnzip):
    
    global DEBUG_STATUS

    logFileLocation = SESSION_DIR + "/log.log"
    logFile = open(logFileLocation, "a")
    logFile.write("Beginning unzip of files\n")
    
   
    # Unzip all files in the scanning directory
    for each in zipFilesToUnzip:
        #path_to_zip_file = SCANNING_DIR + "/" + each
        
        path_to_zip_file = each
        
        if DEBUG_STATUS == True:
            logFile.write("Unzipping File: " + path_to_zip_file + "\n")
        
        try:
            with zipfile.ZipFile(path_to_zip_file, mode = 'r', allowZip64 = True) as zip_ref:
                
                fileNameWithoutExtension = each[:-4] # Strip .zip from file location
                zipFileExtractLocation = fileNameWithoutExtension # unzip file to folder with same name
                zip_ref.extractall(zipFileExtractLocation)

        except:
            logFile.write("Issue with unzipping file: " + path_to_zip_file + "\n")
    
    logFile.write("Unzipping task completed\n")
    logFile.close()