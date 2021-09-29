'''
code for variational learner modeling the null subject acquisition in English. The normal
variational learner works and thus I have the entire thing about null subjects coded. uncomment
ch=2 line for vanilla variational learner.
'''

from __future__ import division
import csv
import time
import matplotlib
matplotlib.use('Agg')

from multiprocessing import Queue
import multiprocessing
import numpy as np
from matplotlib import pyplot as plt
from numpy import random
colag_file=open("colag_id.csv")
# readers are csv readers which is a library thing nothing impactful
reader=csv.reader(colag_file)
next(colag_file)
results=[]
LD={} # LD is for the regular language domain
### choosegrammar looks at the probabities for all the parameters and  chooses the current grammar
def choosegrammar(grammar):
    ret=""
    for g in grammar:
        #gl=random.choice([0,1],p=[1-g,g])
        rand=random.random()
        if rand < g:
            ret = ret + str(1)
        else:
            ret = ret + str(0)
        #ret=ret+str(gl)
    return ret

# this part sets the dictionary keys which are the grammars
def var_learner(r,R,IMP_list,DEC_Q_list,max_sentences,Gtarg,q,R1):
    global LD
    ####
    weights = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    #r=0.001
    faculty=0 # faculty is a variable indicating the ability of child to distinguish
    ns_list=[]
    for i in range(0,max_sentences): # iterating till max_sentences
        faculty = (i - (max_sentences*0.45)) / (max_sentences*0.4) # we start the faculty at 0.45
        # the max sentences like for 500000 it is approx 220000, and continues till 400000(linear increase)
        if faculty < 0:
            faculty = 0
        if faculty > 1:
            faculty = 1
    # the above block checks if faculty does not exceed 1 or fall below 0. if you look closely faculty
    # is 0 for sentence no. below max_sentences*0.45 and goes on to linearly increase for another
    # max_sentences*0.4 sentences.
        sent_choice = random.choice([1, 2], p=[0.2, 0.8])
        # print(LD[Gtarg][0])
        # sentence = random.choice(DEC_Q_list)
        if sent_choice == 1:
            sentence = random.choice(IMP_list)
        else:
            sentence = random.choice(DEC_Q_list)
        ch = random.choice([1, 2], p=[1 - faculty, faculty])
        # ch is choice if faulty is x then choice 1 will be chosen (1-x)% of the time. else it chooses
        # the other choice 2. choice 1 is basically IMP replaced by DEC. choice 2 is fully formed faculty
        # i.e. adult IMP and DEC differentiation
        #ch=2 #uncomment this to get the pure var learner which mmeans it will choose choice 2 all time
        grammar=""
        '''
            l is the current grammar. we choose l untill the l in in colag 
            domain and choosegrammar() has the probabilities right.
        '''
        while grammar not in LD.keys():
            grammar = choosegrammar(weights)

        sup_sub={6:"1"}
        sup_sub_k=sup_sub.keys()
        #random.shuffle(sup_sub_k)
        for i in sup_sub_k:
            if (sentence in LD[grammar[0:i] + sup_sub[i] + grammar[i+1:]]):
                grammar = grammar[0:i] + sup_sub[i] + grammar[i+1:]
            #else:
                #print(sentence)
                #print(grammar)
        #setchoice=[grammar[:3]+"001"+grammar[6:],grammar[:3]+"100"+grammar[6:],grammar[:3]+"110"+grammar[6:]]
        	#print(sentence)
        print(weights[4])
        ns_list.append(weights[4])
        #print(grammar)
	#ns_list.append(weights[4])
        if ch==1: # choice 1 for the IMP DEC business
            #print(g)
            #ns_list.append(weights[4])
            index = [0, 1, 2, 6, 7, 8, 9, 10, 11, 12]
            if sentence in LD[grammar[:3] + "000" + grammar[6:]]:
                grammar = grammar[:3] + "000" + grammar[6:]
                weights[3] = weights[3] - r * weights[3]
                weights[4] = weights[4] - r * weights[4]
                weights[5] = weights[5] - r * weights[5]

            else:
                # print(sentence)
                # print("000 grammar",grammar[:3]+"000"+grammar[6:])
                # print(sentence in grammar[:3]+"000"+grammar[6:])
                if sentence in LD[grammar[:3] + "100" + grammar[6:]]:
                    grammar = grammar[:3] + "100" + grammar[6:]
                    weights[3] = weights[3] + 0.05 * (1 - weights[3])
                    weights[4] = weights[4] - 0.01 * weights[4]
                    weights[5] = weights[5] - r * weights[5]
                else:
                    if sentence in LD[grammar[:3] + "001" + grammar[6:]] and sentence not in LD[
                        grammar[:3] + "110" + grammar[6:]]:
                        # print(sentence)
                        grammar = grammar[:3] + "001" + grammar[6:]
                        weights[3] = weights[3] - 0.95 * weights[3]
                        weights[4] = weights[4] - 0.9 * weights[4]
                        weights[5] = weights[5] + 0.9 * (1 - weights[5])
                    if sentence in LD[grammar[:3] + "110" + grammar[6:]] and sentence not in LD[
                        grammar[:3] + "001" + grammar[6:]]:
                        grammar = grammar[:3] + "110" + grammar[6:]
                        weights[3] = weights[3] + 0.95 * (1 - weights[3])
                        weights[4] = weights[4] + 0.9 * (1 - weights[4])
                        weights[5] = weights[5] - 0.9 * weights[5]
            # print(grammar)
            if sentence in LD[grammar]:  # checks if sentence is parsed by current grammar
                # print(grammar)
                for j in index:  # adjusts weights
                    if grammar[j] == '0':
                        if j == 6:
                            weights[j] = weights[j] - R * weights[j]
                        else:
                            weights[j] = weights[j] - r * weights[j]
                    else:
                        weights[j] = weights[j] + r * (1 - weights[j])
            #if sentence in LD[grammar
            #l=random.choice(LD1.keys())
            if sentence in LD[grammar]: # checks if sentence is parsed by current grammar
                for j in range(0,len(grammar)): # adjusts weights
                    #print(l[j])
                    if weights[j] > 0.02 and weights[j] < 0.98:
                        if grammar[j] == '0' :
                            if j==6:
                                weights[j] = weights[j] - R * weights[j]
                            else:
                                weights[j] = weights[j] - r * weights[j]
                        else:
                            if j == 4 or j==3 or j==5:
                                weights[j] = weights[j] + R * (1 - weights[j])
                            else:
                                weights[j] = weights[j] + r * (1 - weights[j])

        elif sent_choice==2: # choice 2 for vanilla language domain
            index=[0,1,2,6,7,8,9,10,11,12]

            if sentence in LD[grammar[:3] + "000" + grammar[6:]]:
                grammar = grammar[:3] + "000" + grammar[6:]
                weights[3] = weights[3] - r * weights[3]
                weights[4] = weights[4] - r * weights[4]
                weights[5] = weights[5] - r * weights[5]

            else:
                # print(sentence)
                # print("000 grammar",grammar[:3]+"000"+grammar[6:])
                # print(sentence in grammar[:3]+"000"+grammar[6:])
                if sentence in LD[grammar[:3] + "100" + grammar[6:]]:
                    grammar = grammar[:3] + "100" + grammar[6:]
                    weights[3] = weights[3] + 0.05 * (1 - weights[3])
                    weights[4] = weights[4] - 0.01 * weights[4]
                    weights[5] = weights[5] - r * weights[5]
                else:
                    if sentence in LD[grammar[:3] + "001" + grammar[6:]] and sentence not in LD[
                        grammar[:3] + "110" + grammar[6:]]:
                        # print(sentence)
                        grammar = grammar[:3] + "001" + grammar[6:]
                        weights[3] = weights[3] - 0.95 * weights[3]
                        weights[4] = weights[4] - 0.9 * weights[4]
                        weights[5] = weights[5] + 0.9 * (1 - weights[5])
                    if sentence in LD[grammar[:3] + "110" + grammar[6:]] and sentence not in LD[
                        grammar[:3] + "001" + grammar[6:]]:
                        grammar = grammar[:3] + "110" + grammar[6:]
                        weights[3] = weights[3] + 0.95 * (1 - weights[3])
                        weights[4] = weights[4] + 0.9 * (1 - weights[4])
                        weights[5] = weights[5] - 0.9 * weights[5]
            #print(grammar)
            if sentence in LD[grammar]: # checks if sentence is parsed by current grammar
                #print(grammar)
                for j in index: # adjusts weights
                    if grammar[j] == '0':
                        if j == 6:
                            weights[j] = weights[j] - R * weights[j]
                        else:
                            weights[j] = weights[j] - r * weights[j]
                    else:
                            weights[j] = weights[j] + r * (1 - weights[j])

                
                
                 #writer.writerow(sentence)
    q.put(ns_list)  # this is not in loop hence will only be printed once.
    #results.append(ns_list)
    #print(Gtarg)
    #q.put([Gtarg]+weights)
def main():
    global LD
    jobs = []
    #sup_sub={4:1, 5:1}
    languages = ['0001001100011']
    n = 0
    # results=[]
    q=Queue()
    numLearners = 1
    max_sentences = 50000
    #Gtarg = "0001001100011"

    for row in reader:
        LD[row[5]] = set()  # initializes the grammars as empty set of sentence
    ####
    #languages=LD.keys()    
    colag_file.close()
    file_again = open("colag_id.csv")
    # same thing with reader1 just for library reads the csv file as a csv reader object
    reader1 = csv.reader(file_again)
    next(reader1) 
    IMP=set()
    DEC=set()
    for row1 in reader1:
        LD[row1[5]].add(int(row1[1]))
        if row[3]=="IMP":
            IMP.add(int(row1[1]))
        elif row[3]=="DEC":
            DEC.add(int(row1[1]))

        # q = Queue()
    #print(LD)

    results=[]
    # R=0.02
    ns_list = []
    n=0
    languages=languages*numLearners
    while n<len(languages):
        for i in range(42):
	    if n>=len(languages):
                break
            IMP_list = []
            DEC_Q_list = []
            Gtarg=languages[n]
            for sent in LD[Gtarg]:
                if sent in IMP:
                    IMP_list.append(sent)
                else:
                    DEC_Q_list.append(sent)
            #pool = multiprocessing.Pool(processes=40)
            #print(DEC_Q_list)
            #for i in range(numLearners):
                #pool.apply_async(var_learner, args=(0.0004, 0.02, IMP_list, DEC_Q_list, max_sentences, Gtarg))
            #pool.close()
            #pool.join()
            #pool = mp.Pool(processes=4)
            
            p = multiprocessing.Process(target=var_learner, args=(0.0001,0.9,IMP_list,DEC_Q_list,max_sentences,Gtarg,q,0.1))
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
    with open("output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)
    # print(result_list)
    # print(output)
    print(results)
    #print(np.array(results).shape)
    ns_list = np.zeros_like(results[0])
    for result in results:
        ns_list += np.array(result)
    x = np.arange(0, len(ns_list))
    y = ns_list / numLearners
    plt.xlabel("No. of sentences")
    plt.ylabel("NS parameter value")
    plt.plot(x, y)
    #plt.xlim([150000,500000])
    plt.savefig('var_ns.png')
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
