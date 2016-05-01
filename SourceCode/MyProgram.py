'''
Created on Apr 13, 2016

@author: ABHISHEK PRASAD
'''

import sys
import copy
from decimal import *

def normalize(QX):
    tot = 0.0
    for val in QX.values():
        tot += val
    if not (1.0-epsilon < tot < 1.0+epsilon):
        for key in QX.keys():
            QX[key] /= tot
    return QX 
   
epsilon = 0.001

def Prb(var, val, e):
    parents = prob_dict[var][0]
    if len(parents) == 0:
        truePrb = prob_dict[var][1][None]
    else:
        parentVals = [e[parent] for parent in parents]
        truePrb = prob_dict[var][1][tuple(parentVals)]
    if truePrb=='decision':
        return 1.0
    if val==True: return truePrb
    else: return 1.0-truePrb

def enumerationAsk(X, e, vars1):
    QX = {}
    parents = prob_dict[X][0]
    if len(parents) == 0:
        truePrb = prob_dict[X][1][None]
        if truePrb=='decision':
            QX[False]=1.0
            QX[True]=1.0
            return QX
        
    for xi in [False,True]:
        e[X] = xi
        QX[xi] = enumerateAll(vars1,e)
        del e[X]
    return normalize(QX)

def enumerateAll(vars1, e):
    if len(vars1) == 0: return 1.0
    Y = vars1.pop()
    if Y in e:
        val = Prb(Y,e[Y],e) * enumerateAll(vars1,e)
        vars1.append(Y)
        return val
    else:
        total = 0
        e[Y] = True
        total += Prb(Y,True,e) * enumerateAll(vars1,e)
        e[Y] = False
        total += Prb(Y,False,e) * enumerateAll(vars1,e)
        del e[Y]
        vars1.append(Y)
        return total    


global prob_dict
global decn
global util
prob_dict={}
util={}
bn=[]
decn=[]
fo = open("output.txt", "w")
boolcomb={1:[[True],[False]],2:[[True,False],[True,True],[False,False],[False,True]],3:[[True,True,True],[True,True,False],[True,False,True],[True,False,False],[False,True,True],[False,True,False],[False,False,True],[False,False,False]]}    
f = open(sys.argv[len(sys.argv)-1],"r")
inputlines=f.read().splitlines()
num_line=len(inputlines)
index=0;
while(inputlines[index]!='******'):
    index=index+1
index=index+1

while(index<num_line and inputlines[index]!='******'):
    str_line=inputlines[index].split('|');
    if len(str_line)==1:
        bn.insert(0, inputlines[index])
        if inputlines[index+1]=='decision':
            prob_dict.update({inputlines[index]:[[],{None:'decision'}]})
            decn.append(inputlines[index])
        else:
            prob_dict.update({inputlines[index]:[[],{None:float(inputlines[index+1])}]})
        index=index+2;
    elif len(str_line)>1:
        parent1=str_line[1].strip().split(' ')
        index=index+1;
        dict_val={}
        bn.insert(0, str_line[0].strip())
        while(index<num_line and inputlines[index]!='***' and inputlines[index]!='******'):
            spl_val=inputlines[index].split(' ')
            combin=[]
            for j in range(1,len(spl_val)):
                if spl_val[j]=='+':
                    combin.insert(j-1,True)
                else:
                    combin.insert(j-1, False)
            dict_val.update({tuple(combin):float(spl_val[0])})
            prob_dict.update({str_line[0].strip():[parent1,dict_val]})
            index=index+1;
        if (index<num_line and inputlines[index]=='******'):
            break
    index=index+1
if (index<num_line and inputlines[index]=='******'):
    index=index+1
    dict_val1={}
    str_line=inputlines[index].split('|')
    parent2=str_line[1].strip().split(' ')
    index=index+1
    while(index<num_line):
        spl_val1=inputlines[index].split(' ')
        combin=[]
        for j in range(1,len(spl_val1)):
            if spl_val1[j]=='+':
                combin.insert(j-1,True)
            else:
                combin.insert(j-1, False)
        dict_val1.update({tuple(combin):float(spl_val1[0])})
        util.update({str_line[0].strip():[parent2,dict_val1]})
        index=index+1
import re
index=0;
while(inputlines[index]!='******'):
    eobserved_var={}
    match = re.match(r'P\((.*)\|(.*)\)', inputlines[index])
    match1 = re.match(r'P\((.*)\)', inputlines[index])
    match2 = re.match(r'EU\((.*)\|(.*)\)', inputlines[index])
    match3 = re.match(r'EU\((.*)\)', inputlines[index])
    match4 = re.match(r'MEU\((.*)\|(.*)\)', inputlines[index])
    match5 = re.match(r'MEU\((.*)\)', inputlines[index])
    
    if match:
        F = match.group(1).strip()
        observed_var1 = match.group(1).strip().split(',')
        observed_var = match.group(2).strip().split(',')
        val_cal=1.0;
        for x in observed_var:
            x_spl=x.strip().split(' ')
            if  x_spl[2]=='+':
                eobserved_var.update({x_spl[0]:True})
            else:
                eobserved_var.update({x_spl[0]:False})
        for x in observed_var1:
            x_spl1=x.strip().split(' ')
            if  x_spl1[2]=='+':
                val_cal=val_cal*enumerationAsk(x_spl1[0],eobserved_var,bn).get(True)
                eobserved_var.update({x_spl1[0]:True})
            else:
                val_cal=val_cal*enumerationAsk(x_spl1[0],eobserved_var,bn).get(False)
                eobserved_var.update({x_spl1[0]:False})
        fo.write(str(Decimal(str(val_cal)).quantize(Decimal('.01'))))

    elif match1:
        dictnew={}
        observed_var = match1.group(1).strip().split(',')
        val_cal=1.0;
        for x in observed_var:
            x_spl=x.strip().split(' ')
            if  x_spl[2]=='+':
                val_cal=val_cal*enumerationAsk(x_spl[0],dictnew,bn).get(True)
                dictnew.update({x_spl[0]:True})
            else:
                val_cal=val_cal*enumerationAsk(x_spl[0],dictnew,bn).get(False)
                dictnew.update({x_spl[0]:False})
        fo.write(str(Decimal(str(val_cal)).quantize(Decimal('.01'))))
    elif match2:
        dictnew={}
        query1={}
        dictn={}
        observed_var = match2.group(1).strip().split(',')
        observed_var1 = match2.group(2).strip().split(',')
        for x in observed_var:
            x_spl=x.strip().split(' ')
            if  x_spl[2]=='+':
                dictnew.update({x_spl[0]:True})
            else:
                dictnew.update({x_spl[0]:False})
        
        for x in observed_var1:
            x_spl=x.strip().split(' ')
            if  x_spl[2]=='+':
                dictnew.update({x_spl[0]:True})
            else:
                dictnew.update({x_spl[0]:False})
        val_cal=1.0;prob=0;
        combn = util['utility'][1]
        parentval1= util['utility'][0]    
        for x in combn:
            sq=0
            w=list(x)
            query1={}
            flag=0
            for z in parentval1:
                query1[z]=w[sq]
                if z in dictnew:
                    if query1.get(z)!=dictnew.get(z):
                        flag=1;
                        break;
                sq=sq+1;
            if flag==1:
                continue;
            val_cal=1.0
            dictn=copy.deepcopy(dictnew)
            for y in query1:
                if  query1[y]==True:
                    val_cal=val_cal*enumerationAsk(y,dictn,bn).get(True)
                    dictn.update({y:True})
                else:
                    val_cal=val_cal*enumerationAsk(y,dictn,bn).get(False)
                    dictn.update({y:False})
            prob=prob+val_cal*util['utility'][1][tuple(w)]
        prob=prob+0.00000001
        fo.write(str(int(round(prob))))
 
    elif match3:
        dictnew={}
        query1={}
        dictn={}
        observed_var = match3.group(1).strip().split(',')
        for x in observed_var:
            x_spl=x.strip().split(' ')
            if  x_spl[2]=='+':
                dictnew.update({x_spl[0]:True})
            else:
                dictnew.update({x_spl[0]:False})
        
        val_cal=1.0;prob=0;
        combn = util['utility'][1]
        parentval1= util['utility'][0]    
        for x in combn:
            sq=0
            w=list(x)
            query1={}
            flag=0
            for z in parentval1:
                query1[z]=w[sq]
                if z in dictnew:
                    if query1.get(z)!=dictnew.get(z):
                        flag=1;
                        break;
                sq=sq+1;
            if flag==1:
                continue;
            val_cal=1.0
            dictn=copy.deepcopy(dictnew)
            for y in query1:
                if  query1[y]==True:
                    val_cal=val_cal*enumerationAsk(y,dictn,bn).get(True)
                    dictn.update({y:True})
                else:
                    val_cal=val_cal*enumerationAsk(y,dictn,bn).get(False)
                    dictn.update({y:False})
            prob=prob+val_cal*util['utility'][1][tuple(w)]
        prob=prob+0.00000001
        fo.write(str(int(round(prob))))
    elif match4:
        dictnew={}
        query1={}
        dictn={}
        answ={}
        observed_var = match4.group(1).strip().split(',')
        observed_var1 = match4.group(2).strip().split(',')
        
        for x in observed_var1:
            x_spl=x.strip().split(' ')
            if  x_spl[2]=='+':
                dictnew.update({x_spl[0]:True})
            else:
                dictnew.update({x_spl[0]:False})
        prev= -sys.maxint-1
        for perm in boolcomb[len(decn)]:
            ind1=0
            for x in decn:
                x_spl=x.strip()
                if  perm[ind1]==True:
                    dictnew.update({x_spl:True})
                else:
                    dictnew.update({x_spl:False})
                ind1=ind1+1
            val_cal=1.0;prob=0;
            combn = util['utility'][1]
            parentval1= util['utility'][0]    
            for x in combn:
                sq=0
                w=list(x)
                query1={}
                flag=0
                for z in parentval1:
                    query1[z]=w[sq]
                    if z in dictnew:
                        if query1.get(z)!=dictnew.get(z):
                            flag=1;
                            break;
                    sq=sq+1;
                if flag==1:
                    print 'hello'
                    continue;
                
                val_cal=1.0
                dictn=copy.deepcopy(dictnew)
                for y in query1:
                    if  query1[y]==True:
                        val_cal=val_cal*enumerationAsk(y,dictn,bn).get(True)
                        dictn.update({y:True})
                    else:
                        val_cal=val_cal*enumerationAsk(y,dictn,bn).get(False)
                        dictn.update({y:False})
                prob=prob+val_cal*util['utility'][1][tuple(w)]
            print prob
            if(prev < prob):
                prev=prob
                for finval in observed_var:
                    answ.update({finval.strip():dictnew.get(finval.strip())})
        pt_str=""
        for finval in observed_var:
            if answ.get(finval.strip())==True:
                pt_str=pt_str+'+'+' '
            else:
                pt_str=pt_str+'-'+' '
        prev=prev+0.00000001
        pt_str = pt_str+str(int(round(prev)))
        fo.write(pt_str) 
    elif match5:
        dictnew={}
        query1={}
        dictn={}
        answ={}
        observed_var = match5.group(1).strip().split(',')
        
        prev= -sys.maxint-1
        for perm in boolcomb[len(decn)]:
            ind1=0
            for x in decn:
                x_spl=x.strip()
                if  perm[ind1]==True:
                    dictnew.update({x_spl:True})
                else:
                    dictnew.update({x_spl:False})
                ind1=ind1+1
            val_cal=1.0;prob=0;
            combn = util['utility'][1]
            parentval1= util['utility'][0]    
            for x in combn:
                sq=0
                w=list(x)
                query1={}
                flag=0
                for z in parentval1:
                    query1[z]=w[sq]
                    if z in dictnew:
                        if query1.get(z)!=dictnew.get(z):
                            flag=1;
                            break;
                    sq=sq+1;
                if flag==1:
                    continue;
                val_cal=1.0
                dictn=copy.deepcopy(dictnew)
                for y in query1:
                    if  query1[y]==True:
                        val_cal=val_cal*enumerationAsk(y,dictn,bn).get(True)
                        dictn.update({y:True})
                    else:
                        val_cal=val_cal*enumerationAsk(y,dictn,bn).get(False)
                        dictn.update({y:False})
                prob=prob+val_cal*util['utility'][1][tuple(w)]
            if(prev<prob):
                prev=prob
                for finval in observed_var:
                    answ.update({finval.strip():dictnew.get(finval.strip())})
        pt_str=""
        for finval in observed_var:
            if answ.get(finval.strip())==True:
                pt_str=pt_str+'+'+' '
            else:
                pt_str=pt_str+'-'+' '
        prev=prev+0.00000001
        pt_str = pt_str+str(int(round(prev)))
        fo.write(pt_str)
    if inputlines[index+1]!='******':
        fo.write('\n')   
    index=index+1
fo.close()