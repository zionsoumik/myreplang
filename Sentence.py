class Sentence(object):
    def __init__ (self, infoList):
        self.language = infoList[0]
        self.inflection = infoList[1]
        self.sentenceStr = infoList [2]
        self.sentenceList = infoList[2].split()

    #indexString returns index of word in sentenceList if key string is contained in that word.
    #Returns -1 if key string is not in sentence
    def indexString(self,key):
        for word in self.sentenceList:
            if key in word:
                return self.sentenceList.index(word)
        return -1
    def fullhouse(self):
        Sindex = self.indexString("S")
        O1index = self.indexString("O1")
        O2index = self.indexString("O2")
        Pindex = self.indexString("P")
        O3index = self.indexString("O3")
        Advindex=self.indexString("Adv")
        if (Sindex==0):
            if (O2index==O1index+1 and Pindex==O2index+1 and O3index==Pindex+1 and Advindex==O3index+1):
                return True
            elif (O1index==O2index+1 and Pindex+1==O2index and O3index+1==Pindex and Advindex+1==O3index):
                return True
            else:
                return False
    #outOblique checks to see if something other than subject has been topicalized ie. moved out of canonical argument order
    #not checking for presence of Adv topicalized, maybe add later (this is sufficient but Adv could be informative for longitudinal study)
    def outOblique(self):
        O1index = self.indexString("O1")
        O2index = self.indexString("O2")
        Pindex = self.indexString("P")
        O3index = self.indexString("O3")

        if (O1index != -1 and O1index < O2index < Pindex and O3index == Pindex+1):
            return False
        elif (O3index != -1 and O3index < O2index < O1index and Pindex == O3index+1):
            return False
        elif (O1index != -1 and O2index != -1 and Pindex != -1 and O3index != -1):
            return True
