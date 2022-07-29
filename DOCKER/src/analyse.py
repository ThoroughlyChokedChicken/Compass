import os, os.path


DEBUG_STATUS = True


def CheckFileExtensions(SESSION_DIR, SCANNING_DIR, uniqueID, USE_ONLY_APPROVED_EXTENSIONS, APPROVED_EXTENSIONS):
    global DEBUG_STATUS
    
    fileExtensionsDict = {}


    for root, dirs, files in os.walk(SCANNING_DIR):
        # select file name
        for file in files:
            
            # Extract file extension from file
            filename, file_extension = os.path.splitext(file)

            # Verify file isn't a temp or hidden file
            if file[0] != "~" or file[0] != "." :
                if file_extension in fileExtensionsDict:
                    # add one to the item in the list
                    fileExtensionsDict[str(file_extension)] += 1

                else:
                    # add a new dict entry for the file extension
                    if file_extension == ".log":
                        pass
                    elif str(file_extension) == ".zip":
                        pass
                    else:
                        fileExtensionsDict.update({str(file_extension): 1})
                
                if USE_ONLY_APPROVED_EXTENSIONS == True:
                    pass

    
    # User specific log for debugging
    if DEBUG_STATUS == True:
        logFileLocation = SESSION_DIR + "/log.log"
        logFile = open(logFileLocation, "a")
        logFile.write("** FILE EXTENSIONS FOUND: **\n")
        logFile.write(str(fileExtensionsDict))
        logFile.write("\n\n")
        logFile.close()

    # Record on server log the userID and their total file extensions for future stats collection
    CURR_DIR = os.getcwd() # current working directory
    serverFileLocation = CURR_DIR + "/dockerlog.log"
    serverFile = open(serverFileLocation, "a")
    serverFile.write(uniqueID + ": Extensions: " + str(fileExtensionsDict) + "\n")
    serverFile.close()

    # Return total extensions back to main app
    return fileExtensionsDict
                    
                    
def FilesToScan(UPLOAD_DIR, SESSION_DIR, USE_ONLY_APPROVED_EXTENSIONS, APPROVED_EXTENSIONS, listOfFilesToScan):
    for root, dirs, files in os.walk(UPLOAD_DIR):
        # select file name
        for file in files:
            # Extract file extension from file

            # Get Fill File Path
            fullFilePath = str(os.path.join(root, file))
            
            # Extract file extension from file
            filename, file_extension = os.path.splitext(file)

            if file[0] != "~" or file[0] != "." :
                if USE_ONLY_APPROVED_EXTENSIONS == True:
                    if str(file_extension) in APPROVED_EXTENSIONS:
                        if fullFilePath in listOfFilesToScan:
                            pass # skip, it's already there
                        else:
                            listOfFilesToScan.append(str(fullFilePath))
                    
                else: # add file if it's not already in list since we don't care about file extensions
                    if fullFilePath in listOfFilesToScan:
                        pass # skip, it's already there
                    elif fullFilePath + ".txt" in listOfFilesToScan:
                        pass # skip, it's already there
                    else:
                        listOfFilesToScan.append(str(fullFilePath))

    
    fileLocation = SESSION_DIR + "/filesToScan.log"
    listFile = open(fileLocation, "w")
    for each in listOfFilesToScan:
        listFile.write(str(each) + "\n")
    listFile.close()      

    return listOfFilesToScan     
