from time import time
from random import choice
from argparse import ArgumentParser
from NDresultsnew import NDresults
from NDChildnew import NDChild
from Sentence import Sentence
from sys import exit
import csv
from scipy.optimize import curve_fit
import math
import pandas as pd
from scipy.stats import truncnorm
from scipy.stats import truncnorm
import numpy as np
import matplotlib
matplotlib.use('Agg')
import numpy as np
from matplotlib import pyplot as plt
from csv import writer
import multiprocessing
import numpy as np
from multiprocessing import Queue
#GLOBALS
ns_list=[]
rate = 0.0005
conservativerate = 0.0001
from numpy import random
vtoirate=0.04

oprate=0.0001


#ahrate=0.001
threshold = .001
results=[]

def logifunc(x,x0,k):
    return 1 / (1 + np.exp(-k*(x-x0)))

def func(x, k, c):
    return k*x+c

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

def pickASentence(languageDomain,infl_list):
    #print(len(languageDomain))
    #print(infl_list)
    infl_list.sort()
    index1=infl_list.index("IMP")
    index2=infl_list.index("Q")
    list1=range(0,index1)+range(index2,len(infl_list))
    list2=range(index1,index2)
    ch = random.choice([choice(list1), choice(list2)], p=[0.8, 0.2])
    #print(list2)
    return languageDomain[ch]

def createLD(language):
    #languageDict = {'english': '611', 'french': '584', 'german': '2253', 'japanese': '3856'}
    langNum = language
    #print "type langnum"
    #print type(langNum)

    langNum=bin(int(langNum))[2:].zfill(13)
    #print(langNum)
    LD = []
    infl_list=[]
    with open('COLAG_2011_flat_formatted.txt','r') as infoFile:
        for line in infoFile:
            [grammStr, inflStr, sentenceStr] = line.split("\t")
            sentenceStr = sentenceStr.rstrip()
            inflStr=inflStr.replace(" ","")
            #print(sentenceStr)
            # constructor creates sentenceList
	    
            s = Sentence([grammStr, inflStr, sentenceStr])
            if grammStr == langNum:
                infl_list.append(inflStr)
                #print([grammStr, inflStr, sentenceStr])
                LD.append(s)
    #print("len of ld",len(LD))
    #print(len(infl_list)
    return LD,infl_list

def childLearnsLanguage(ndr, languageDomain,language,numberofsentences,infl_list,sl,c,growth):
    ndr.resetThresholdDict()
    aChild = NDChild(rate, conservativerate, language,sl,c,growth)
    rt1 = {}
    rt2 = {}
    # rt3={}
    ns_list=[]
    # rt4={}
    # print numberofsentences
    for j in xrange(numberofsentences):
        s = pickASentence(languageDomain,infl_list)
        aChild.consumeSentence(s, j)
        #aChild.adjustfaculty()
        # print(j)
        # print(aChild.grammar)
        # If a parameter value <= to the threshold for the first time,
        # this is recorded in ndr for writing output
        #ndr.checkIfParametersMeetThreshold(threshold, aChild.grammar, j)
        #print(aChild.grammar)
        ns_list.append(aChild.grammar['NS'])
        #print(ns_list)
        #if j == 50000:
            #rt1 = aChild.grammar.copy()
            #rt2 = ndr.thresholdDict.copy()
    #rt3 = aChild.grammar
    #rt4 = ndr.thresholdDict
    # print(rt1,rt2,rt3,rt4)
    return [ns_list]


def runSingleLearnerSimulation(languageDomain, numLearners, numberofsentences, language,q,infl_list,sl,c,growth):
    # Make an instance of NDresults and write the header for the output file
    ndr = NDresults()
    #ndr.writeOutputHeader(language, numLearners, numberofsentences)
    # Create an array to store the simulation
    # results to write to a csv after its ended

    print("Starting the simulation...")
    result = [childLearnsLanguage(ndr, languageDomain,language,numberofsentences,infl_list,sl,c,growth) for x in range(numLearners)]
    q.put(result)

def runOneLanguage(numLearners, numberofsentences, language,q,sl,c,growth):
    if numLearners < 1 or numberofsentences < 1:
        print('Arguments must be positive integers')
        exit(2)

    LD,infl_list = createLD(language)
    print(len(LD))
    runSingleLearnerSimulation(LD, numLearners, numberofsentences, language,q,infl_list,sl,c,growth)

# Run random 100 language speed run
def runSpeedTest(numLearners, numberofsentences):
    # Make dictionary containing first 100
    # language IDs from the full CoLAG domain

    languageDict = {}
    with open('COLAG_Flat_GrammID_Binary_List.txt','r') as myfile:
        head = [next(myfile) for x in xrange(3)]

    for line in head:
        binaryId, decimalId = line.split('\t')
        languageDict[binaryId] = []

    # Collect the corresponding sentences for each language
    with open('COLAG_2011_flat_formatted.txt', 'r') as infoFile:
        for line in infoFile:
            [grammStr, inflStr, sentenceStr] = line.split("\t")

            if grammStr in languageDict:
                sentenceStr = sentenceStr.rstrip()
                # constructor creates sentenceList
                s = Sentence([grammStr, inflStr, sentenceStr])
                languageDict[grammStr].append(s)

    # Run 100 eChildren for each language
    for key, value in languageDict.iteritems():
        language = str(int(key, 2))
        runSingleLearnerSimulation(value, numLearners, numberofsentences, language)

def runAllCoLAGLanguages(numLearners, numberofsentences):
    # Build a dictionary that contains the sentences that
    # correspond to every language
    languageDict = {}
    with open('COLAG_2011_flat_formatted.txt', 'r') as sentencesFile:
        for line in sentencesFile:
            [grammStr, inflStr, sentenceStr] = line.split("\t")

            sentenceStr = sentenceStr.rstrip()
            # constructor creates sentenceList
            s = Sentence([grammStr, inflStr, sentenceStr])
            languageDict[grammStr].append(s)

    # Iterate therough the dictionary and run a simulation for each language
    for key, value in languageDict.iteritems():
        language = str(int(key, 2))
        runSingleLearnerSimulation(value, numLearners, numberofsentences, language)

def prepare_stats(num):
    y1 = get_truncated_normal(mean=0.4, sd=0.1785, low=0, upp=0.75)
    y2 = get_truncated_normal(mean=0.64, sd=0.43, low=0.25, upp=1)
    y3 = get_truncated_normal(mean=0.9, sd=0.179, low=0.25, upp=1)

    NFS1=y1.rvs(num)
    NFS2=y2.rvs(num)

    NFS3=y3.rvs(num)

    NFS1.sort()
    NFS2.sort()
    NFS3.sort()

    x1 = get_truncated_normal(mean=2.73, sd=0.1, low=2.54, upp=2.96)
    x2 = get_truncated_normal(mean=3.3, sd=0.1, low=3.12, upp=3.48)
    x3 = get_truncated_normal(mean=3.82, sd=0.1, low=3.64, upp=3.98)

    age1=x1.rvs(num)
    age2=x2.rvs(num)
    age3=x3.rvs(num)

    age1.sort()
    age2.sort()
    age3.sort()
    x0=[]
    slope=[]
    for i in range(0,num):
        x=np.asarray([3566209.688+(age1[i]-2)*2044182.5,5610392.188+(age2[i]-3)*2177498.75,5610392.188+(age3[i]-3)*2177498.75],dtype=np.float)
        y=np.asarray([NFS1[i],NFS2[i],NFS3[i]],dtype=np.float)
        popt, pcov = curve_fit(func,x,y,p0=[5000000,0.000001])
        #print(popt)
        slope.append(popt[0])
        x0.append(popt[1])
    return slope,x0

if __name__ == '__main__':
    start = time()
    global results
    global ns_list
    ns_list=[]
    q=Queue()
    # The argument keeps track of the mandatory arguments,
    # number of learners, max number of sentences, and target grammar
    parser = ArgumentParser(prog='Doing Away With Defaults', description='Set simulation parameters for learners')
    parser.add_argument('integers', metavar='int', type=int, nargs=3,
                        help='(1) The number of learners (2) The number of '
                         'sentences consumed')
    #parser.add_argument('strings', metavar='str', type=str, nargs=1)
                        #help='The name of the language that will be used.'
                                #'The current options are English=611, '
                                #'German=2253, French=584, Japanese=3856')

    args = parser.parse_args()
    #numLearners = 0

    # Test whether certain command line arguments
    # can be converted to positive integers
    numLearners = args.integers[0]
    numberofsentences = args.integers[1]
    growth=args.integers[2]
    #language = str(args.strings[0]).lower()

    # if language == "alllanguages":
    #     runAllCoLAGLanguages(numLearners, numberofsentences)
    # elif language == "speedtest":
    #     runSpeedTest(numLearners, numberofsentences)
    # else:
    languages=['611']*100





















    #with open('100.txt','rb') as tsvin:
        #tsvin = csv.reader(tsvin,delimiter='\t')
        #for row in tsvin:
            #languages.append(row.pop(0))
    print(languages)

    print(numberofsentences)
    print(numLearners)
    jobs = []
    param=[]
    n=0
    if growth==1:    
    	with open('linear_param.csv', 'rb') as f:
    		reader = csv.reader(f)
    		param = list(reader)
    else:
	with open('e_param.csv', 'rb') as f:
    		reader = csv.reader(f)
    		param = list(reader)
    print(param)

    while n<len(languages):
        #q = Queue()

	#sl,c=prepare_stats(100)
        for i in range(0,100):
	
            if n>=len(languages):
                break
            p = multiprocessing.Process(target=runOneLanguage, args=(numLearners, numberofsentences, languages[n],q,param[n][0],param[n][1],growth))
            n=n+1
            #print(n)
            jobs.append(p)
            p.start()
            #results.append(q.get())
        while 1:
            running = any(p.is_alive() for p in jobs)
            while not q.empty():
                results.append(q.get())
            if not running:
                break
        #print(results)
    #runOneLanguage(numLearners, numberofsentences, language)

    #outFile = open("production-output1.csv", "a+b")
    #outFile1 = open("production-output2.csv", "a+b")
    # with open(self.outputfile,"a+b") as outFile and open(self.outputfile1,"a+b") as outFile1:
    #outWriter = writer(outFile)
    #outWriter1 = writer(outFile1)
    pList = ["lang", "OPT", "NS", "NT", "TM"]
    #print(len(results[0][0]))
    print("--- %s seconds ---" % (time() - start))
    print("results:",len(results[0][0][0]))
    ns_list=np.zeros_like(results[0][0][0][0:numberofsentences])
    n_list=[]
    for result in results:
        n_list.append(result[0][0][0:numberofsentences])
        ns_list+=np.array(result[0][0][0:numberofsentences])
    #ns_list=results[0][0][4][0:numberofsentences]
    print("n_list is:",ns_list)
    res=map(list, zip(*n_list))
    with open("output_ns.csv", "wb") as f:
       writer = csv.writer(f)
       writer.writerows(res)

    x=np.arange(0,len(ns_list))
    y=ns_list/100
    plt.xlabel("No. of sentences")
    plt.ylabel("NS parameter value")
    plt.plot(x, y)
    #plt.xlim([150000,500000])
    plt.savefig('NDL_ns2.png')