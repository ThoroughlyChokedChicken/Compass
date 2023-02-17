
class Result:
    def __init__(self,percentOne,percentTwo,highestPercent,fileOne,linesOfWorkOne,fileTwo,linesOfWorkTwo,matchingOriginalLines,totalOriginalLines,differenceInTotalLines,delta,matchingLinesBetweenAssignments,totalLines):
        self.percentOne = percentOne
        self.percentTwo = percentTwo
        self.highestPercent = highestPercent
        self.fileOne = fileOne
        self.linesOfWorkOne = linesOfWorkOne
        self.fileTwo = fileTwo
        self.linesOfWorkTwo = linesOfWorkTwo
        self.matchingOriginalLines = matchingOriginalLines
        self.totalOriginalLines = totalOriginalLines
        self.differenceInTotalLines = differenceInTotalLines
        self.delta = delta
        self.matchingLinesBetweenAssignments = matchingLinesBetweenAssignments
        self.totalLines = totalLines


