import os, os.path


DEBUG_STATUS = True


def CheckFileExtensions(SCANNING_DIR):
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
    
    if DEBUG_STATUS == True:
        logFileLocation = SCANNING_DIR + "/log.log"
        logFile = open(logFileLocation, "a")
        logFile.write("** FILE EXTENSIONS FOUND: **\n")
        logFile.write(str(fileExtensionsDict))
        logFile.write("\n\n")
        logFile.close()

    return fileExtensionsDict
                    
                    
                
