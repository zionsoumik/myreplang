from __future__ import division
from numpy import random
import math

class NDChild(object):
    def __init__(self, learningrate, conslearningrate, language,sl,c,growth):

        self.grammar = {"lang": language, "OPT": .5, 'OPT': 0.5, 'NS': 0.5, 'NT': 0.5, 'TM': 0.5}
        self.r = learningrate  # simulation will pass child a learning rate
        self.conservativerate = conslearningrate
        self.faculty=1.0
        #self.oprate = oprate
        #self.vtoirate=vtoirate
        self.sl=sl
        self.x0=c
	self.growth=growth

    def consumeSentence(self, s,j):  # child is fed a list containing [lang, inflec, sentencestring]
        #self.spEtrigger(s)  # parameter 1
        #self.hipEtrigger(s)  # parameter 2
        #self.hcpEtrigger(s)  # parameter 3
	#print(self.growth)
	if self.growth==1:
        	self.faculty=float(self.sl)*j+float(self.x0)
		#self.faculty=0.00000021*j-0.68697880
        	if self.faculty<0:
            		self.faculty=0
        	if self.faculty>1:
            		self.faculty=1
	else:
        	#self.faculty=(math.tanh((j-75000-182500)/37500)+1)/2
        	self.faculty=1/(1+math.exp(-float(self.x0)*(j-float(self.sl))))
        	#self.faculty=1/(1+math.exp(-0.000001*(j-5530818.042)))

        ch=random.choice([1,2],p=[1-self.faculty,self.faculty])
	#ch=2
        #print(self.faculty)
        #print(ch)
        #if j<250000:
        if ch==1:
            #self.opt1Etrigger(s)  # parameter 4
            self.ns1Etrigger(s)  # parameter 5
            #self.nt1Etrigger(s)
        else:
            #self.optEtrigger(s)  # parameter 4
            self.nsEtrigger(s)  # parameter 5
            #self.ntEtrigger(s)  # parameter 6
        # self.whmEtrigger(s)  # parameter 7
        # self.piEtrigger(s)  # parameter 8
        #self.tmEtrigger(s)  # parameter 9
        # self.VtoIEtrigger(s)  # parameter 10
        # self.ItoCEtrigger(s)  # parameter 11
        # self.ahEtrigger(s)  # parameter 12
        # self.QInvEtrigger(s)  # parameter 13
        ##print(self.grammar)
    # etriggers for parameters
    # first parameter Subject Position
    # def spEtrigger(self, s):
    #     # Check if O1 and S are in the sentence and sent is declarative
    #     if "O1" in s.sentenceList and "S" in s.sentenceList and s.inflection == "DEC":
    #         O1index = s.sentenceList.index("O1")
    #         Sindex = s.sentenceList.index("S")  # Sindex is position of S in sentList
    #         # Make sure O1 is non-sentence-initial and before S
    #         if O1index > 0 and O1index < s.sentenceList.index("S"):
    #             # set towards Subject final
    #             self.adjustweight("SP", 1, self.r)
    #         # S occurs before 01
    #         elif Sindex > 0 and O1index > s.sentenceList.index("S"):  # S cannot be Sent initial
    #             # set towards Subject initial
    #             self.adjustweight("SP", 0, self.r)
    #
    # # second parameter Head IP, VP, PP, etc
    # def hipEtrigger(self, s):
    #     if "O3" in s.sentenceList and "P" in s.sentenceList:
    #         O3index = s.sentenceList.index("O3")
    #         Pindex = s.sentenceList.index("P")
    #         # O3 followed by P and not topicalized
    #         if O3index > 0 and Pindex == O3index + 1:
    #             self.adjustweight("HIP", 1, self.r)
    #         elif O3index > 0 and Pindex == O3index - 1:
    #             self.adjustweight("HIP", 0, self.r)
    #
    #     # If imperative, make sure Verb directly follows O1
    #     elif s.inflection == "IMP" and "O1" in s.sentenceList and "Verb" in s.sentenceList:
    #         if s.sentenceList.index("O1") == s.sentenceList.index("Verb") - 1:
    #             self.adjustweight("HIP", 1, self.r)
    #         elif s.sentenceList.index("Verb") == (s.sentenceList.index("O1") - 1):
    #             self.adjustweight("HIP", 0, self.r)

    # third parameter Head in CP
    # def hcpEtrigger(self, s):
    #     if s.inflection == "Q":
    #         # ka or aux last in question
    #         if s.sentenceList[-1] == 'ka' or ("ka" not in s.sentenceList and s.sentenceList[-1] == "Aux"):
    #             self.adjustweight("HCP", 1, self.r)
    #         # ka or aux first in question
    #         elif s.sentenceList[0] == "ka" or ("ka" not in s.sentenceList and s.sentenceList[0] == "Aux"):
    #             self.adjustweight("HCP", 0, self.r)

    # fourth parameter Optional Topic (0 is obligatory,  1 is optional)
    def opt1Etrigger(self, s):
        if  s.inflection != "Q" and self.grammar["TM"] > 0.5 and self.grammar[
            "NT"] < 0.5 and "[+WA]" not in s.sentenceStr:
            self.adjustweight("OPT", 1, self.r)
        #elif s.inflection == "DEC" and self.grammar["TM"] > 0.5 and self.grammar[
            #"NT"] < 0.5 and "[+WA]" in s.sentenceStr:
            #self.adjustweight("OPT", 0, self.conservativerate)

        elif s.inflection == "Q" and self.grammar["TM"] > 0.5 and self.grammar[
            "NT"] < 0.5 and "[+WA]" not in s.sentenceStr and "+WH" in s.sentenceStr:
            self.adjustweight("OPT", 1, self.r)
        #first word in sentence is any of those & overt subject and full complemenets in VP

        elif (self.grammar["NT"] < 0.5):
            if (s.inflection != "Q" and s.sentenceList[0] in ["Verb", "Aux", "Not", "Never"]):
                self.adjustweight("OPT", 1, self.r)  # Opt to 1 unambig
                ##print("ka in DEC")
            if (s.sentenceList[0] in ["ka","Verb", "Aux", "Not", "Never"] and ("+WH" in s.sentenceStr)  and s.inflection=="Q"):
                self.adjustweight("OPT",1,self.r)
                ##print("ka in Q")
            #elif self.grammar["NT"] < 0.5:
                #self.adjustweight("OPT", 0, self.conservativerate)
                ##print("fullhouse")
        #if s.fullhouse():
            #self.adjustweight("OPT",1,self.conservativerate)

    def optEtrigger(self, s):
        if s.inflection == "DEC" and self.grammar["TM"] > 0.5 and self.grammar[
            "NT"] < 0.5 and "[+WA]" not in s.sentenceStr:
            self.adjustweight("OPT", 1, self.r)
        #elif s.inflection == "DEC" and self.grammar["TM"] > 0.5 and self.grammar[
            #"NT"] < 0.5 and "[+WA]" in s.sentenceStr:
            #self.adjustweight("OPT", 0, self.conservativerate)

        elif s.inflection == "Q" and self.grammar["TM"] > 0.5 and self.grammar[
            "NT"] < 0.5 and "[+WA]" not in s.sentenceStr and "+WH" in s.sentenceStr:
            self.adjustweight("OPT", 1, self.r)
        #first word in sentence is any of those & overt subject and full complemenets in VP

        elif (self.grammar["NT"] < 0.5):
            if (s.inflection == "DEC" and s.sentenceList[0] in ["Verb", "Aux", "Not", "Never"]):
                self.adjustweight("OPT", 1, self.r)  # Opt to 1 unambig
                ##print("ka in DEC")
            if (s.sentenceList[0] in ["ka","Verb", "Aux", "Not", "Never"] and ("+WH" in s.sentenceStr)  and s.inflection=="Q"):
                self.adjustweight("OPT",1,self.r)
                ##print("ka in Q")
            #elif self.grammar["NT"] < 0.5:
                #self.adjustweight("OPT", 0, self.conservativerate)
                ##print("fullhouse")
        #if s.fullhouse():
            #self.adjustweight("OPT",1,self.conservativerate)

    def ns1Etrigger(self, s):
        if s.inflection != "Q" and "S" not in s.sentenceStr:
            self.adjustweight("NS", 1, self.r)
            #self.adjustweight("OPT", 1, self.r)


        elif s.inflection != "Q" and "S" in s.sentenceStr:
            self.adjustweight("NS", 0, self.conservativerate)

    def nt1Etrigger(self, s):
        if  s.inflection != "Q" and "O2" in s.sentenceStr and "O1" not in s.sentenceStr:
            self.adjustweight("NT", 1, self.r)
            self.adjustweight("OPT", 0, self.r)  # null topic necessitates obligatory topic

        elif s.inflection != "Q" and "O2" in s.sentenceStr and "O1" in s.sentenceStr and "O3" in s.sentenceStr and "S" in s.sentenceStr and "Adv" in s.sentenceStr:
            self.adjustweight("NT", 0, self.conservativerate)
        self.adjustweight("OPT", 0, self.conservativerate)

    def nsEtrigger(self, s):
        if s.inflection == "DEC" and "S" not in s.sentenceStr:
            self.adjustweight("NS", 1, self.r)
            #self.adjustweight("OPT", 1, self.r)

        elif s.inflection == "DEC" and "S" in s.sentenceStr:
            self.adjustweight("NS", 0, self.conservativerate)

    def ntEtrigger(self, s):
        if s.inflection == "DEC" and "O2" in s.sentenceStr and "O1" not in s.sentenceStr:
            self.adjustweight("NT", 1, self.r)
            self.adjustweight("OPT", 0, self.r)  # null topic necessitates obligatory topic

        elif s.inflection == "DEC" and "O2" in s.sentenceStr and "O1" in s.sentenceStr and "O3" in s.sentenceStr and "S" in s.sentenceStr and "Adv" in s.sentenceStr:
            self.adjustweight("NT", 0, self.conservativerate)
	    self.adjustweight("OPT", 0, self.conservativerate)

        # if all possible complements of VP are in sentence, then the sentence is not Null Topic

    # def whmEtrigger(self, s):
    #     if s.inflection == "Q" and "+WH" in s.sentenceStr:
    #         if ("+WH" in s.sentenceList[0]) or ("P" in s.sentenceList[0] and "O3[+WH]" == s.sentenceList[1]):
    #             self.adjustweight("WHM", 1, self.conservativerate)
    #         else:
    #             self.adjustweight("WHM", 0, self.r)
    #
    # def piEtrigger(self, s):
    #     pIndex = s.indexString("P")
    #     O3Index = s.indexString("O3")
    #     if pIndex > -1 and O3Index > -1:
    #         if abs(pIndex - O3Index) > 1:
    #             ##print("pos",s.sentenceStr)
    #             self.adjustweight("PI", 1, self.r)
    #
    #         elif ((pIndex + O3Index) == 1):
    #             #print("amb:",s.sentenceStr)
    #             self.adjustweight("PI", 0, self.conservativerate)
    #
    def tmEtrigger(self, s):
        if "[+WA]" in s.sentenceStr:
            self.adjustweight("TM", 1, self.r)
        elif "O1" in s.sentenceList and "O2" in s.sentenceList and (
                abs(s.sentenceList.index("O1") - s.sentenceList.index("O2")) > 1):
            self.adjustweight("TM", 0, self.r)
    #
    # def VtoIEtrigger(self, s):
    #
    #     # if self.grammar["HIP"]<0.5 and self.grammar["SP"]<0.5 and "Verb" in s.sentenceStr and "Not" in s.sentenceStr and 'Aux' not in s.sentenceStr and s.inflection=="DEC":
    #     #     Notindex = s.indexString("Not")
    #     #     #Neverindex= s.indexString("Never")
    #     #     if Notindex != 0 and (s.indexString("Verb") - Notindex) <= -1:
    #     #         ##print(s.indexString("Verb"))
    #     #         ##print( Notindex)
    #     #         #print("Not before:",s.sentenceStr)
    #     #         self.adjustweight("VtoI", 1, self.r)
    #     #         self.adjustweight("AH", 0, self.r)
    #     # elif self.grammar["HIP"]<0.5  and self.grammar["SP"]<0.5 and "Verb" in s.sentenceStr and "Never" in s.sentenceStr and 'Aux' not in s.sentenceStr and s.inflection=="DEC":
    #     #     Neverindex = s.indexString("Never")
    #     #     if Neverindex!= 0 and (s.indexString("Verb") - Neverindex) <= -1:
    #     #         #print("never before",s.sentenceStr)
    #     #         self.adjustweight("VtoI", 1, self.r)
    #     #         self.adjustweight("AH", 0, self.r)
    #     # elif self.grammar["HIP"] > 0.5  and self.grammar["SP"]<0.5 and "Verb" in s.sentenceStr and "Not" in s.sentenceStr and 'Aux' not in s.sentenceStr and s.inflection == "DEC":
    #     #     Notindex = s.indexString("Not")
    #     #     # Neverindex= s.indexString("Never")
    #     #     if Notindex != 0 and (s.indexString("Verb") - Notindex) >= 1:
    #     #         ##print(s.indexString("Verb"))
    #     #         ##print( Notindex)
    #     #         #print("Not before:", s.sentenceStr)
    #     #         self.adjustweight("VtoI", 1, self.r)
    #     #         self.adjustweight("AH", 0, self.r)
    #     # elif self.grammar["HIP"]>0.5  and self.grammar["SP"]<0.5 and "Verb" in s.sentenceStr and "Never" in s.sentenceStr and 'Aux' not in s.sentenceStr and s.inflection=="DEC":
    #     #     Neverindex = s.indexString("Never")
    #     #     if Neverindex!= 0 and (s.indexString("Verb") - Neverindex) >= 1:
    #     #         #print("never before",s.sentenceStr)
    #     #         self.adjustweight("VtoI", 1, self.r)
    #     #         self.adjustweight("AH", 0, self.r)
    #     if "Verb" in s.sentenceStr and "O1" in s.sentenceStr and 'Aux' not in s.sentenceStr and s.inflection == "DEC":
    #         o1index = s.indexString("O1")
    #         if o1index != 0 and abs(s.indexString("Verb") - o1index) > 1:
    #             # #print(s.indexString("Verb"))
    #             # #print(Notindex)
    #             ##print("01 v separate", s.sentenceStr)
    #             self.adjustweight("VtoI", 1, self.r)
    #             self.adjustweight("AH", 0, self.r)
    #
    #         # no need to explicitly check inflection because only Q and DEC have AUX
    #     elif "Aux" in s.sentenceList:
    #         ##print(s.sentenceStr)
    #         self.adjustweight("VtoI", 0, self.conservativerate)
    #
    # def ItoCEtrigger(self, s):
    #     sp = self.grammar['SP']
    #     hip = self.grammar['HIP']
    #     hcp = self.grammar['HCP']
    #
    #     if s.inflection == "DEC" and "S" in s.sentenceList and "Aux" in s.sentenceList:
    #         if sp < 0.5 and hip < 0.5:  # (Word orders 1, 5) subject and IP initial, aux to the right of Subject
    #             Sindex = s.sentenceList.index("S")
    #             if Sindex > 0 and s.sentenceList.index("Aux") == Sindex + 1:
    #                 self.adjustweight("ItoC", 0, self.r)
    #
    #                 ##print(s.sentenceStr)
    #
    #             elif hcp < 0.5 and (s.sentenceList.index("Aux") - s.sentenceList.index("S")) < 0:
    #                 # above code aux - s position less than 0 means aux precedes s
    #                 self.adjustweight("ItoC", 1, self.r)
    #                 self.adjustweight("AH", 0, self.r)
    #
    #             elif hcp > 0.5 and s.sentenceList[-1] == "Aux":
    #                 self.adjustweight("ItoC", 1, self.r)
    #                 self.adjustweight("AH", 0, self.r)
    #
    #
    #         elif sp > 0.5 and hip > 0.5:  # (Word orders 2, 6) #subject and IP final, aux to the left of subject
    #             AuxIndex = s.sentenceList.index("Aux")
    #             if (AuxIndex > 0 and s.sentenceList.index("S") == AuxIndex + 1):
    #                 self.adjustweight("ItoC", 0, self.r)
    #                 ##print(s.sentenceStr)
    #
    #             elif hcp > 0.5 and s.sentenceList[-1] == "Aux" and s.sentenceList.index("S") == (AuxIndex - 1):
    #                 self.adjustweight("ItoC", 1, self.r)
    #                 self.adjustweight("AH", 0, self.r)
    #                 #print("itoc1",s.sentenceStr)
    #
    #
    #             elif hcp < 0.5 and s.sentenceList.index("Aux") == 0:
    #                 self.adjustweight("ItoC", 1, self.r)
    #                 self.adjustweight("AH", 0, self.r)
    #                 #print("itoc1", s.sentenceStr)
    #             elif hcp < 0.5 and (s.sentenceList.index("Aux") < s.sentenceList.index("Verb")):
    #                 self.adjustweight("ItoC", 1, self.r)
    #                 self.adjustweight("AH", 0, self.r)
    #                 #print("itoc1", s.sentenceStr)
    #
    #
    #
    #         elif sp > 0.5 and hip < 0.5 and hcp > 0.5 and "Verb" in s.sentenceList:  # subject and C initial, IP final, Aux immediately precedes verb
    #             if s.sentenceList.index("Verb") == s.sentenceList.index("Aux") + 1:
    #                 #print(s.sentenceStr)
    #                 self.adjustweight("ItoC", 0, self.r)
    #             elif "Not" in s.sentenceList and (
    #                     s.sentenceList.index("Verb") == s.sentenceList.index("Not") + 1 and s.sentenceList.index(
    #                     "Verb") == s.sentenceList.index("Aux") + 2):
    #                 #print(s.sentenceStr)
    #                 self.adjustweight("ItoC", 0, self.r)
    #             elif "Never" in s.sentenceList and (
    #                     s.sentenceList.index("Verb") == s.sentenceList.index("Never") + 1 and s.sentenceList.index(
    #                     "Verb") == s.sentenceList.index("Aux") + 2):
    #                 #print(s.sentenceStr)
    #                 self.adjustweight("ItoC", 0, self.r)
    #             else:
    #                 self.adjustweight("ItoC", 1, self.r)
    #                 #print("else:",s.sentenceStr)
    #                 # will experiment with aggressive rate
    #                 self.adjustweight("AH", 0, self.r)
    #
    #         elif sp < 0.5 and hip > 0.5 and hcp < 0.5 and "Verb" in s.sentenceList:  # subject and C initial, IP final, Aux immediately precedes verb
    #             if s.sentenceList.index("Aux") == s.sentenceList.index("Verb") + 1:
    #                 self.adjustweight("ItoC", 0, self.r)
    #             elif "Not" in s.sentenceList and (
    #                     s.sentenceList.index("Aux") == s.sentenceList.index("Not") + 1 and s.sentenceList.index(
    #                     "Aux") == s.sentenceList.index("Verb") + 2):
    #                 self.adjustweight("ItoC", 0, self.r)
    #             elif "Never" in s.sentenceList and (
    #                     s.sentenceList.index("Aux") == s.sentenceList.index("Never") + 1 and s.sentenceList.index(
    #                     "Aux") == s.sentenceList.index("Verb") + 2):
    #                 self.adjustweight("ItoC", 0, self.r)
    #             else:
    #                 self.adjustweight("ItoC", 1, self.r)
    #                 self.adjustweight("AH", 0, self.r)
    #                 #print("itoc1", s.sentenceStr)
    #                 # will experiment with aggressive rate
    #
    #
    #
    #
    #         elif "Aux" in s.sentenceStr and "Verb" in s.sentenceList:  # check if aux and verb in sentence and something comes between them
    #             Vindex = s.sentenceList.index("Verb")
    #             Auxindex = s.sentenceList.index("Aux")
    #             indexlist = []  # tokens that would shed light if between
    #             if "S" in s.sentenceList:
    #                 Sindex = s.sentenceList.index("S")
    #                 indexlist.append(Sindex)
    #
    #             if "O1" in s.sentenceList:
    #                 O1index = s.sentenceList.index("O1")
    #                 indexlist.append(O1index)
    #
    #             if "O2" in s.sentenceList:
    #                 O2index = s.sentenceList.index("O2")
    #                 indexlist.append(O2index)
    #
    #             if abs(Vindex - Auxindex) != 1:  # if verb and aux not adjacent
    #                 for idx in indexlist:
    #                     if (Vindex < idx < Auxindex) or (Vindex > idx > Auxindex):  # if item in index list between them
    #                         self.adjustweight("ItoC", 1, self.r)
    #                         self.adjustweight("AH", 0, self.r)# set toward 1
    #                         ##print("itoc1", s.sentenceStr)
    #                         break
    #
    #     elif s.inflection == "DEC" and "Never" in s.sentenceStr and "Verb" in s.sentenceStr and "O1" in s.sentenceStr and (
    #             "Aux" not in s.sentenceStr):
    #         neverPos = s.indexString("Never")
    #         verbPos = s.indexString("Verb")
    #         O1Pos = s.indexString("O1")
    #
    #         if (neverPos > -1 and verbPos == neverPos + 1 and O1Pos == verbPos + 1 and self.grammar["HIP"]<0.5 ) or (
    #                 O1Pos > 0 and verbPos == O1Pos + 1 and neverPos == verbPos + 1 and self.grammar["HIP"]>0.5):
    #             self.adjustweight("ItoC", 0, self.r)
    #             #print("o1 v",s.sentenceStr)
    #
    #     # elif ((sp < 0.5 and hip > 0.5 and hcp > 0.5) or (sp > 0.5 and hip < 0.5 and hcp < 0.5))  and "Verb" in s.sentenceList and "Aux" not in s.sentenceList and "Never" in s.sentenceList:
    #     #     self.adjustweight("ItoC", 1 , self.r)
    #         # Following line outlines conservative trigger for +ItoC in SOVIC and CIVOS languages. These languages will always have an aux in consv trigger is evidence towards 1 because it is contrary to VPedge triggers
    #     elif ((sp > 0.5 and hcp < 0.5 and hip < 0.5) or (
    #             sp < 0.5 and hcp > 0.5 and hip > 0.5)) and "Never" in s.sentenceStr and "Aux" in s.sentenceStr and "Verb" in s.sentenceStr:
    #         self.adjustweight("ItoC", 1, self.conservativerate)
    #
    #
    # def ahEtrigger(self, s):
    #     ##print(s.sentenceStr)
    #     if (s.inflection == "DEC" and self.grammar["ItoC"]<0.5) and (
    #             "Aux" not in s.sentenceStr and ("Never" in s.sentenceStr or "Not" in s.sentenceStr) and "Verb" in s.sentenceStr and "O1" in s.sentenceStr):
    #         neverPos = s.indexString("Never")
    #         verbPos = s.indexString("Verb")
    #         O1Pos = s.indexString("O1")
    #         notPos = s.indexString("Not")
    #         if (neverPos > -1 and verbPos == neverPos + 1 and O1Pos == verbPos + 1 and self.grammar["HIP"]<0.5) or (
    #                 O1Pos > -1 and verbPos == O1Pos + 1 and neverPos == verbPos + 1 and self.grammar["HIP"]>0.5):
    #             print("never verb 01",s.sentenceStr)
    #             self.adjustweight("AH", 1, self.r)
    #             self.adjustweight("VtoI", 0, self.r)
    #
    #         if (notPos > -1 and verbPos == notPos + 1 and O1Pos == verbPos + 1 and self.grammar["HIP"]<0.5) or (
    #                 O1Pos > -1 and verbPos == O1Pos + 1 and notPos == verbPos + 1 and self.grammar["HIP"]>0.5):
    #             print("not verb 01",s.sentenceStr)
    #             self.adjustweight("AH", 1, self.r)
    #             self.adjustweight("VtoI", 0, self.r)
    #
    #     elif "Aux" in s.sentenceStr:
    #         self.adjustweight("AH", 0, self.conservativerate)
    #         # if self.grammar["VtoI"] > 0.5: #If not affix hopping language, vtoi is either 0 or 1, but if evidence of vtoi towards 1 has alreadybeen observed, increase confidence 1VtoI given 0AH
    #         #   self.adjustweight("VtoI", 1, self.conservativerate)
    #
    # def QInvEtrigger(self, s):
    #     if s.inflection == "Q" and "ka" in s.sentenceStr:
    #         self.adjustweight("QInv", 0, self.r)
    #         self.adjustweight("ItoC", 0, self.r)
    #
    #     elif s.inflection == "Q" and "ka" not in s.sentenceStr and "WH" not in s.sentenceStr:
    #         self.adjustweight("QInv", 1, self.r)
    #
    # #            self.adjustweight("ItoC", 1, self.conservativerate)

    def adjustweight(self, parameter, direction, rate):
        if direction == 0:
            self.grammar[parameter] -= rate * self.grammar[parameter]
        elif direction == 1:
            self.grammar[parameter] += rate * (1 - self.grammar[parameter])

