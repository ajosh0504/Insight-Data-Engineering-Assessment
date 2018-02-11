# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 18:29:25 2018

@author: Apoorva
"""
#import pandas as pd
#dataset= pd.read_csv('appujo.txt',sep='|',header= None,encoding='latin1')
import hashlib
import datetime
import re
import math
import sys

filepath= sys.argv[1]
outputfile = sys.argv[3]
percent_file = sys.argv[2]

#Dictionary to detect repeat donors
dict_repeatdonor={}
#Reading the input file line by line
with open(filepath) as fp:
    for line in fp:
        line=line.strip()
        line=line.split('|')
        try:
            #Checking for malformed date or zipcode
            datetime.datetime(int(line[13][4:8]), int(line[13][0:2]), int(line[13][2:4]))
            int(line[10])
        except:
            continue
        #If correctly formatted name, zipcode, empty Other_ID, non-empty recipient ID, non-empty transaction amount
        if re.match(r'\A(.)+,\s(.)+',line[7],re.I) and len(line[10]) >= 5 and len(line[15])==0 and len(line[0]) > 0 and len(line[14]) > 0:
            #Creating hashes identifying a donor-recipient pair
            mystring= line[0]+line[7]+(line[10])[0:5] 
            hash_obj= hashlib.md5(mystring.encode())
            x = hash_obj.hexdigest()
            try:
                #If the pair already exists, set the value to True to indicate repeat donor
                if dict_repeatdonor[x] == False:
                    dict_repeatdonor[x] = True
                    
            except:
                #Add first occurence of a donor-recipient pair to the dictionary
                dict_repeatdonor[x] = False
fp.close()
#Dictionary that keeps record of donations made to a recipient from
#repeat donors associated with a particular zipcode, for each calendar year                
dict_recipient={}
#Read percentile from percentile.txt
with open(percent_file) as fp:
    P= fp.readline()
    P= P.strip()
    P=int(P) 
#Function to compute running percentile, total donations and printing out to 
#an output file
with open(outputfile, 'w+') as f:    
    def computations(recipient,zipcode,yr):
        
            perc_index= math.ceil(P*len(dict_recipient[recipient][zipcode][yr])/100.0)
            percentile= sorted(dict_recipient[recipient][zipcode][yr])[perc_index]
            total_donation= sum(dict_recipient[recipient][zipcode][yr])
            f.write(recipient+'|'+zipcode+'|'+yr+'|'+str(percentile)+'|'+str(total_donation)+'|'+str(len(dict_recipient[recipient][zipcode]['donor_set']))+'\n')
        
        
    #Reading through the input file line by line
    with open(filepath) as fp:
        for line in fp:
            line= line.strip()
            line=line.split('|')
            #Creating hashes
            mystring= line[0]+line[7]+(line[10])[0:5] 
            hash_obj= hashlib.md5(mystring.encode())
            x = hash_obj.hexdigest()
            recipient=line[0]
            zipcode= (line[10])[0:5]
            yr=(line[13])[4:8]
            donation= int(line[14])
            
            try: 
                #For each repeat donor
                if dict_repeatdonor[x]:
                    #If the recipient already exists
                    if recipient in dict_recipient.keys():
                        #if the zipcode already exists
                        if zipcode in dict_recipient[recipient].keys():
                            #keep track of repeat donors
                            try:
                                dict_recipient[recipient][zipcode]['donor_set'].add(x)
                            except:
                                dict_recipient[recipient][zipcode]['donor_set'] = set([x])
                            #if the year already exists
                            if yr in dict_recipient[recipient][zipcode].keys():
                                #Add the donation of the repeat donor to the 
                                #recipient,from that particular zipcode, for that calendar year
                                dict_recipient[recipient][zipcode][yr].append(donation)
                                computations(recipient,zipcode,yr)
                                
                            else:
                                #Else create a new entry for each new year encountered 
                                #and then add donation
                                dict_recipient[recipient][zipcode][yr]= [donation]
                                computations(recipient,zipcode,yr)
                        else:
                           
                            #Create a new entry for each zipcode encountered and 
                            #then add donation for that calendar year
                            dict_recipient[recipient][zipcode]={}
                            dict_recipient[recipient][zipcode][yr]= [donation]
                            try:
                                dict_recipient[recipient][zipcode]['donor_set'].add(x)
                            except:
                                dict_recipient[recipient][zipcode]['donor_set'] = set([x])
                            computations(recipient,zipcode,yr)
                    else:
                        #Create a new entry for each new recipient encountered and add donation
                        #for that zipcode and year. 
                        dict_recipient[recipient]={}
                        dict_recipient[recipient][zipcode]={}
                        dict_recipient[recipient][zipcode][yr]= [donation]
                        try:
                            dict_recipient[recipient][zipcode]['donor_set'].add(x)
                        except:
                            dict_recipient[recipient][zipcode]['donor_set'] = set([x])
                        computations(recipient,zipcode,yr)
            except:
                continue
f.close() 

        
        
