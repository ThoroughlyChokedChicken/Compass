import os.path

DEBUG_STATUS = True


def StarterAssignment(SESSION_DIR, UPLOAD_DIR):
    global DEBUG_STATUS

    ###### VERIFY PRESENCE OF TEMPLATE FILE AND IT'S FULL FILE LOCATION ######

    templateFileName = "" # File name for the template file
    templatePresent = False

    # Pull and log the template assignment name from the main user folder
    starterFilename = SESSION_DIR + "/assignments.log"
    logStarterFile = open(starterFilename, "r")
    templateFileName = logStarterFile.readline()
    logStarterFile.close()

    # Open main log file
    logFileLocation = SESSION_DIR + "/log.log"
    logFile = open(logFileLocation, "a")
    logFile.write("\n** STARTER FILE ANALYSIS **\n")

    # Convert template file to txt if needed
    if str(templateFileName).endswith(".docx") or str(templateFileName).endswith(".doc") or str(templateFileName).endswith(".pdf"):
        logFile.write("Starter template is a word or pdf file\n")
        templateFileName.strip('\n')
        templateFileName = templateFileName + ".txt"
        logStarterFile = open(starterFilename, "w")
        logStarterFile.write(templateFileName + "\n")
        logStarterFile.close()

    # Log action to main log file
    if templateFileName != "NO STARTER FILE":
        logFile.write("Template Assignment Name: " + str(templateFileName) + "\n")
        templatePresent = True
    else:
        logFile.write("Template Assignment Name: NO TEMPLATE UPLOADED\n")
        
    
    ## We now know if there IS or IS NOT a starter template file and it's location
    if templatePresent == True:
        startingAssignmentFullFilePath = SESSION_DIR + "/" + templateFileName
        logFile.write(startingAssignmentFullFilePath)
        logFile.write("\n")
    
    logFile.write("Starter File Present: " + str(templatePresent) + "\n")
    logFile.write("** STARTER FILE ANALYSIS COMPLETE**\n\n.")
    logFile.close()
    
    
    
    ###### IF PRESENT, READ TEMPLATE FILE LINES INTO MEMORY ######
    originalAssignmentLinesNoWhitespace = []
    
    if templatePresent == True:
        originalAssignmentLinesNoWhitespace = OriginalAssignmentInput(startingAssignmentFullFilePath)
        
        if DEBUG_STATUS == True:
            logFileLocation = SESSION_DIR + "/log.log"
            logFile = open(logFileLocation, "a")
            logFile.write("\n** STARTER FILE LINES **\n")
            logFile.write(str(originalAssignmentLinesNoWhitespace))
            logFile.close()
    
    return templatePresent, originalAssignmentLinesNoWhitespace


    





def OriginalAssignmentInput(originalFileLocation):
    
    startingLines = []
    
    # Convert original to temp file and remove whitespace
    o1 = open(originalFileLocation, "a")
    o1.close()
    o1 = open(originalFileLocation, "r")
    
        
    # Temp files. Don't change this
    f1 = open("temporiginal.txt", "w")

    # Strip blank lines from  file and store them in temporiginal
    for line in o1:
        if not line.isspace():
            f1.write(line)
            tempLine = line.replace(" ", "")
            if tempLine[0] != "#": # Don't count original lines if they are comments for code
                startingLines.append(tempLine.strip()) 
    o1.close()
    f1.close()


    return startingLines




























########################### ORIGINAL BUSTER BELOW ###########################


def OLDRUNBUSTER():

    

    # Ask if they want to filter out original assignment
    userFilterOriginal = input("\nDo you want to filter out the boiler-plate material (original assignment or initally given work) from the rest of content in a submission?\nYou would use this if you provided a starter document or initial code users were supplied. This prevents having matching lines across files when it's simpily directions or initial content given to the user.\n(Y)es or (N)o?: ")

    if userFilterOriginal.upper() == "Y":
        print(f"\nThe default original file must be in the same folder as the files being scanned.\n")
        ORIGINAL_ASSIGNMENT_NAME = input("Enter the starter file file name (include the file extension): ")
        print(f"\n{ORIGINAL_ASSIGNMENT_NAME}   <- is the starting assignment to that's going to be used.")
        FILTER_ORIGINAL_ASSIGNMENT_OUT = True
        
    else:
        FILTER_ORIGINAL_ASSIGNMENT_OUT = False


    # Ask the user what % cutoff they want (as a number)
    userCutoff = input(f"\n\nWhat percent similarity cutoff do you want? {DEFAULT_LINE_LIMIT}% is the current default.\nEnter 67.5% as 67.5 for example: ")
    if userCutoff == "":
        MATCHING_LINE_LIMIT = DEFAULT_LINE_LIMIT
    else:
        try:
            MATCHING_LINE_LIMIT = float(userCutoff)
        except:
            print("Input failed. Exiting...")
            exit()


    userDelta = input(f"\nEnter the delta cutoff (% difference between two files) you'd like to see. {DEFAULT_DELTA}% is the current default: ")
    if userDelta == "":
        DELTA_BETWEEN_TWO_FILES = DEFAULT_DELTA
    else:
        try:
            DELTA_BETWEEN_TWO_FILES = float(userDelta)
        except:
            print("Input failed. Exiting...")
            exit()





    # Determine file type
    while True:
        userFileType = input("\n\nWhat do you want to do?\n(W)ord docs scanned\n(P)ython files scanned\n(C)# files scanned\n(U)nzip files in the folder\n(M)oss Output from Stanford\n(Q)uit\n")
        if userFileType.upper() == "W":
            TYPE_OF_FILE_TO_SCAN = ".docx" # Set to docx for conversion
            ConvertWordToTxt() # First convert all docx's to txt, then continue
            # TODO: modded from .txt to .py for MOSS testing
            TYPE_OF_FILE_TO_SCAN = ".py" # Then set to txt to scan
            break
        
        elif userFileType.upper() == "P":
            TYPE_OF_FILE_TO_SCAN = ".py"
            break
        
        elif userFileType.upper() == "C":
            TYPE_OF_FILE_TO_SCAN = ".cs"
            break
        
        elif userFileType.upper() == "U":
            UnZipFiles()
        
        elif userFileType.upper() == "M":
            
            if MOSS_FILE_EXISTS == True:
                # Check if user even entered an original assignment. If yes...
                if FILTER_ORIGINAL_ASSIGNMENT_OUT == True:
                    useStarter = input("Do you want to factor in starter assignment? (Y)es or (N)o: ").upper()
                    if useStarter == "Y":
                        mossOutputLine = MossOutput(True)
                    else:
                        mossOutputLine = MossOutput(False)
                # If no, don't ask to include it. Continue with not using it
                else:
                    mossOutputLine = MossOutput(False)
                
                runMoss = input("Would you like to run the MOSS scan now? (Y)es or (N)o?: ").upper()
                if runMoss == "Y":
                    os.system(mossOutputLine)
                else:
                    print("If you decide to later, here is the line to run:\n\n")
                    print(mossOutputLine)
                runMoss = "" # Clear variable
            else:
                # Moss.pl does NOT exist
                print("\nThe \"moss.pl\" file does not exist. MOSS functions are turned off.\n\nPlease visit http://theory.stanford.edu/~aiken/moss/ to enroll and setup MOSS.\n\nOnce enrolled, keep moss.pl in the same folder as this script and this feature will work.\n")

        elif userFileType.upper() == "Q":
            print("Goodbye\n\n")
            exit()
        else: 
            print("Invalid selection.")






    ### Begin Output Starting With Working Directories

    if DEBUG_STATUS == True: 
        print(f"\nThe current directory is: {CURR_DIR}")
        print(f"The scanning directory containing files is: {SCANNING_DIR}\n")


    # File all file names/paths and add them to a list
    filesToScanList = []
    filesToScanList = ListOfFilesToScan()





    #################### FILE MATCHING SCAN ####################

    print(f"\n\nThis may take a couple minutes. Please be patient.\nBeginning file line matching scan...\n\n\n")



    # Reterive original assignment lines
    startingAssignmentFullFilePath = SCANNING_DIR + "/" + ORIGINAL_ASSIGNMENT_NAME
    if DEBUG_STATUS == True:
        print(f"Starting Assignment Location: {startingAssignmentFullFilePath}\n\n")

    if FILTER_ORIGINAL_ASSIGNMENT_OUT == True:
        ORIGINAL_ASSIGNMENT_LINES = OriginalAssignmentInput(startingAssignmentFullFilePath)
        if DEBUG_STATUS == True:
            print(f"The original assignment lines are:\n\n{ORIGINAL_ASSIGNMENT_LINES}\n\n")





    # Call function to scan matching lines in files and save results into MATCHING_POSITIVE_HITS
    MATCHING_POSITIVE_HITS = ScanExactLineCopies(ORIGINAL_ASSIGNMENT_LINES, MATCHING_LINE_LIMIT, filesToScanList)





    # NEGATIVE OUTPUT
    if INCLUDE_NEG_RESULTS == True:
        NegativeSimilarity()





    # POSITIVE OUTPUT
    MatchingOutput(MATCHING_POSITIVE_HITS, DELTA_BETWEEN_TWO_FILES, ORIGINAL_ASSIGNMENT_LINES)





    # REMOVE BASE DIR TEMP FILES
    try:
        os.remove("temp1.py")
        os.remove("temp2.py")
        os.remove("temporiginal.py")
    except:
        print("Failed to cleanup some temp files.")





def ScanExactLineCopies(ORIGINAL_ASSIGNMENT_LINES, MATCHING_LINE_LIMIT, filesToScanList):
    
    global DEBUG_STATUS
    global LIST_OF_NEGATIVE_HITS
    global LIST_OF_EMPTY_HITS
    global userFileType

    totalFilesToScan = len(filesToScanList)
    print("Progress...\n")

    try:
        percentCompletedPerFile = 100 / totalFilesToScan
    except:
        if DEBUG_STATUS == True:
            print("Error calculating percentage completion of files")
            percentCompletedPerFile = 1

    


    if DEBUG_STATUS == True:
        print(f"We are going to print the following list of files:\n{filesToScanList}")

    LIST_OF_POSITIVE_HITS = []
    

    studentCounter = 0

    while studentCounter < len(filesToScanList):

        
        baseFile = filesToScanList[studentCounter]
        
        counter2 = studentCounter + 1 # Don't compare two of the same files. Also every file previous has already been compared. ##IMPORTANT!

        try: 
            percentCompleted = studentCounter * percentCompletedPerFile
        except:
            if DEBUG_STATUS == True:
                print("Error calculating percentage completion of files")
                percentCompleted = 1

        
        # PRINT THE PROGRESS ON SCREEN
        print(f"{round(percentCompleted, 1)}%")
        

        while counter2 < len(filesToScanList):
        
            readyToFlipFiles = False
            bothFilesCompared = False

            while bothFilesCompared == False:
                
                
                
                
                # FILES NEED TO BE COMPARED TO EACH OTHER (A to B then B to A)
                # Use READY TO FLIP FILES for this (change o1 and o2)




                ###fileToCheck = SCANNING_DIR + "/" + filesToScanList[counter2]
                fileToCheck = filesToScanList[counter2]
                
                #########################################################################################################

                if readyToFlipFiles == False:
                # Open both files and strip any blank lines from each. Store the results into 2 temp files
                    o1 = open(baseFile, "r")
                    o2 = open(fileToCheck, "r")

                    if DEBUG_STATUS == True:
                        print(f"Currently checking baseFile: {baseFile}")
                        print(f"Currently checking fileToCheck: {fileToCheck}\n\n")

                    # Temp files. Don't change these
                    f1 = open("temp1.py", "w")
                    f2 = open("temp2.py", "w")


                    # Strip blank lines from each file and store them in temp1 and temp2
                    for line in o1:
                        if not line.isspace():
                            f1.write(line)


                    for line in o2:
                        if not line.isspace():
                            f2.write(line)

                    o1.close()
                    o2.close()
                    f1.close()
                    f2.close()
                else:
                    o2 = open(baseFile, "r")
                    o1 = open(fileToCheck, "r")

                    if DEBUG_STATUS == True:
                        print(f"Currently checking baseFile: {baseFile}")
                        print(f"Currently checking fileToCheck: {fileToCheck}\n\n")

                    # Temp files. Don't change these
                    f1 = open("temp1.py", "w")
                    f2 = open("temp2.py", "w")


                    # Strip blank lines from each file and store them in temp1 and temp2
                    for line in o1:
                        if not line.isspace():
                            f1.write(line)


                    for line in o2:
                        if not line.isspace():
                            f2.write(line)

                    o1.close()
                    o2.close()
                    f1.close()
                    f2.close()

                    bothFilesCompared = True # Done comparing both files so reset for the next round.



                # Now open and compare temp files
                f1 = open("temp1.py", "r")


                # Vars for comparing from File 1
                i = 0
                totalLinesFile1 = 0
                sameLines = 0
                totalLinesInFile2 = 0
                percentSimilar = 0.0
                codeLinesFile1 = 0
                commentedLinesFile1 = 0
                listOfSameLines = []
                originalAssignLineComfirmed1 = 0





                # Compare each seperate line in file 1 with each individual line in file 2
                for line in f1:

                    totalLinesFile1 += 1
                    
                    # Remove spaces from each line
                    strippedLine1 = line.replace(" ", "")
                    

                    # Check to see if it's a python comment. If it is, count it as a comment
                    if line[0] == "#" or strippedLine1[0] == "#":
                        commentedLinesFile1 += 1
                        if DEBUG_STATUS == True:
                            print(f"Commened line: {line}")
                    
                    
                    ## ORIGINAL ASSIGNMENT CODE
                    
                    elif (strippedLine1.strip() in ORIGINAL_ASSIGNMENT_LINES):
                        # If strippedLine1 is in the original assignment, don't mark it as a same line (ie, do nothing here)
                        originalAssignLineComfirmed1 += 1

                        

                        if DEBUG_STATUS == True:
                            print(f"Currently checking baseFile: {baseFile}")
                            print(f"Currently checking fileToCheck: {fileToCheck}\n\n")
                            print(strippedLine1)
                            print(originalAssignLineComfirmed1)
                            
                            print("Line is from original assignment in file 1.")
                            print(strippedLine1)

                    # Otherwise it's a usable line
                    else:
                        codeLinesFile1 += 1
                    
                    
                    









                    f2SingleSimilarLineMonitor = False # This is method 1 of preventing multiple of the same lines to register as hits in file 2
                    f2LineNumber = 0
                    totalLinesInFile2 = 0
                    commentedLinesFile2 = 0
                    codeLinesFile2 = 0
                    originalLineComfirmed = 0
                    originalAssignLineComfirmed2 = 0

                    # Keep opening and closing file 2 to look at every line
                    f2 = open("temp2.py", "r")
                    for line2 in f2:
                        
                        totalLinesInFile2 += 1
                        strippedLine2 = line2.replace(" ", "")
                        

                        # Lines can be only COMMENTED, ORIGINAL, OR CODELINES
                        if line2[0] == "#" or strippedLine2[0] == "#":
                            commentedLinesFile2 += 1

                        elif (strippedLine2.strip() in ORIGINAL_ASSIGNMENT_LINES):
                            # If strippedLine1 is in the original assignment, don't mark it as a same line (ie, do nothing here)
                            originalAssignLineComfirmed2 += 1

                            if DEBUG_STATUS == True:
                                print("Line is from original assignment in file 2.")
                                print(strippedLine2)
                                
                        # Otherwise it's a usable line
                        else:
                            codeLinesFile2 += 1


                        f2LineNumber += 1 # Taking note of what line number we are on in F2. Needed to ensure they are not repeated.
                        

                        
                        if strippedLine1.strip() == strippedLine2.strip() and strippedLine2[0] != "#" and f2LineNumber not in listOfSameLines:       
                            if DEBUG_STATUS == True:
                                print("Identical Line Found")                        
                                print(line.strip())
                                print(line2.strip())
                                print(f"On file 2 line number: {f2LineNumber}\n")
                                
                            # Either a same line or an assignment line. Never both.
                            if (strippedLine1.strip() in ORIGINAL_ASSIGNMENT_LINES):
                                # This matched line is from the original, ignore.
                                if DEBUG_STATUS == True:
                                    print("Skipping matched line. This is in the original assignment.")
                            else:
                                sameLines += 1 # THE LINES ARE THE SAME HERE


                            # Same line recording
                            listOfSameLines.append(f2LineNumber)
                            
                        
                        # elif ADD ACCEPTIABLE SIMILARITY CHECK HERE!!!

                    f2.close()





                # closing file1
                f1.close()									
                    
                # sameLines = lines that are the same to another file. Are verified not in original assignment
                # totalLinesFile1 = Overall number of lines in File 1
                # codeLinesFile1 = Number of code/text lines that are not any other category
                # commentedLinesFile1 = comments in code. They start with #
                # originalAssignLineComfirmed1 = Num of lines that match the original assignment. Comments were removed when building this list

                # TotalLines = codeLines + originalLines + commentedLines
                # Note how same is not part of this equation.

                # TotalLines - OrginalLines - CommentedLines = CodeLines
                # If CodeLines = 0 then they didn't write anything (use 100 - x as in 100% - x = percent written)
                # Amount User Wrote = CodeLines / (Total - Commented)
                # 

                

                # Note file names and paths
                if readyToFlipFiles == False:
                    file1 = filesToScanList[studentCounter]
                    file2 = filesToScanList[counter2]
                elif readyToFlipFiles == True:
                    file1 = filesToScanList[counter2]
                    file2 = filesToScanList[studentCounter]
                    


                if DEBUG_STATUS == True:
                    print(f"\n\nNumber of similar lines: {sameLines}\n")
                    
                    print(f"File 1: {file1}")
                    print(f"Total number of coded lines in File 1: {codeLinesFile1}")
                    print(f"Total commented lines in File 1: {commentedLinesFile1}")
                    print(f"Overall total number of lines in File 1: {totalLinesFile1}")
                    print(f"The number of lines in File 1 that matches the original assignment: {originalAssignLineComfirmed1}")
                    
                    print("\n")
                    
                    print(f"File 2: {file2}")
                    print(f"Total number of coded lines in File 2: {codeLinesFile2}")
                    print(f"Total commented lines in File 2: {commentedLinesFile2}")
                    print(f"Overall total number of lines in File 2: {totalLinesInFile2}")
                    print(f"The number of lines in File 1 that matches the original assignment: {originalAssignLineComfirmed2}")

                    print("\n")




                # TODO: THIS AREA DOES CALCULATION OF LINE SIMILARY. CAN IT SHOW:
                # % Original is included in assignment
                # % Diff of original to assignment
                # Can I get a % similar overall (but STILL include the perfect matches?)
                # 100% match is correct but I want to see the % of diff/addition as well

                ######## Can I give a number that REMOVES the original assignment in the %same comparison?




                if commentedLinesFile1 + originalAssignLineComfirmed1 + codeLinesFile1 == totalLinesFile1:
                    if DEBUG_STATUS == True:
                        print("All lines accounted for in search")
                else:
                    if DEBUG_STATUS == True:
                        print("\n\nLINES MISSING IN COUNT! Check commented, coded, and total lines above.")
                    

                
                if codeLinesFile2 != 0:
                    percentSimilar = (sameLines / codeLinesFile2) * 100 # COMPARED TO FILE TWO USEABLE LINES, how many were the same?
                    
                    percentSimilar = round(percentSimilar, 3)
                    diffInTotalLines = totalLinesFile1 - totalLinesInFile2
                    if diffInTotalLines < 0:
                        diffInTotalLines *= -1
                
                else:
                    diffInTotalLines = totalLinesFile1 - totalLinesInFile2
                    

                if DEBUG_STATUS == True:
                    print(f"\nPercent similar: {percentSimilar}%\n\n")

                if readyToFlipFiles == False:
                    tempPercentSimilar = percentSimilar
                    
                    

                ######### RECORD HITS TO RECORD
                if readyToFlipFiles == True and (percentSimilar >= MATCHING_LINE_LIMIT or tempPercentSimilar >= MATCHING_LINE_LIMIT):
                    LIST_OF_POSITIVE_HITS.append(tempPercentSimilar)
                    LIST_OF_POSITIVE_HITS.append(percentSimilar)

                    LIST_OF_POSITIVE_HITS.append(diffInTotalLines)

                    LIST_OF_POSITIVE_HITS.append(filesToScanList[studentCounter])
                    LIST_OF_POSITIVE_HITS.append(filesToScanList[counter2])

                    LIST_OF_POSITIVE_HITS.append(originalAssignLineComfirmed1)

                    LIST_OF_POSITIVE_HITS.append(codeLinesFile1)
                    LIST_OF_POSITIVE_HITS.append(codeLinesFile2)

                    


                else:
                    LIST_OF_NEGATIVE_HITS.append(tempPercentSimilar)
                    LIST_OF_NEGATIVE_HITS.append(percentSimilar)

                    LIST_OF_NEGATIVE_HITS.append(diffInTotalLines)

                    LIST_OF_NEGATIVE_HITS.append(filesToScanList[studentCounter])
                    LIST_OF_NEGATIVE_HITS.append(filesToScanList[counter2])
                    
                
                # Empty Files are Noted
                if codeLinesFile1 == 0 and readyToFlipFiles == False:
                    if filesToScanList[studentCounter] not in LIST_OF_EMPTY_HITS:
                        LIST_OF_EMPTY_HITS.append(filesToScanList[studentCounter])
                        
                

                ### Both Files
                readyToFlipFiles = True

            
            
            
            


            
            #########################################################################################################
            counter2 += 1 # Increment to next file to compare to

        studentCounter += 1 # Start comparing file #2, then 3, etc

    ## END OF FUNCTION
    return LIST_OF_POSITIVE_HITS