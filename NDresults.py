from csv import writer
from os import remove, path

class NDresults(object):
    def __init__ (self):
        self.thresholdDict = {"lang":-1,"SP": -1, "HIP": -1, "HCP": -1, "OPT": -1, "NS": -1, "NT": -1, "WHM": -1, "PI": -1, "TM": -1, "VtoI": -1, "ItoC": -1,"AH": -1, "QInv": -1}
        self.outputfile = ''

    def resetThresholdDict(self):
        self.thresholdDict = {"lang":-1,"SP": -1, "HIP": -1, "HCP": -1, "OPT": -1, "NS": -1, "NT": -1, "WHM": -1, "PI": -1, "TM": -1, "VtoI": -1, "ItoC": -1,"AH": -1, "QInv": -1}

    # Check if the threshold hasn't been met before and if so, check if current
    # parameter value meets it
    def checkIfParametersMeetThreshold(self, threshold, grammar, currSentenceNum):
        for key, value in grammar.items():
            if self.thresholdDict[key] < 0 and (value <= threshold or value >= (1-threshold)):
                self.thresholdDict[key] = currSentenceNum


    # Write the header columns to the output file
    def writeOutputHeader(self, language, numEChildren, numSentences):
        # Delete the old version of the output file if it exists
        self.outputfile ='simulation-output.csv'

        with open(self.outputfile,"a+") as outFile:
            outWriter = writer(outFile)
            # r1 = language
            # outWriter.writerow([r1])
            # r2 = "{} eChildren".format(numEChildren)
            # outWriter.writerow([r2])
            # r3 = "{} sentences".format(numSentences)
            # outWriter.writerow([r3])
            pList = ["SP", " ", "HIP", " ", "HCP", " ", "OPT", " ", "NS", " ", "NT", " ", "WHM", " ", "PI",
                             ' ', "TM", " ", "VtoI", " ", "ItoC", " ", "AH", " ", "QInv", " "]
            r4 = [' '] + ['{}'.format(p) for p in pList]
            outWriter.writerow(r4)


    def writeResults(self, results):
        self.outputfile = 'simulation-output3.csv'
        with open(self.outputfile,"a+b") as outFile:
            outWriter = writer(outFile)
            pList = ["lang","SP", "HIP", "HCP", "OPT", "NS", "NT", "WHM", "PI", "TM", "VtoI", "ItoC","AH", "QInv"]
            for index, result in enumerate(results):
                str1 = 'eChild {}'.format(index)
                r1 = []
                for p in pList:
                    r1.append(result[0][p])
                    r1.append(result[1][p])
                outWriter.writerow(r1)
