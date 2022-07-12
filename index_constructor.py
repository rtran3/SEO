from collections import defaultdict
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import json
import os
import math
from heapq import heappush,heappop

class index_constructor:

    def __init__(self):
        self.index=defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        self.championList=defaultdict(lambda: defaultdict(float))
        self.championDocs=defaultdict(lambda: defaultdict(list))
        self.indexDocs=defaultdict(lambda: defaultdict(list))
        self.newIndex=defaultdict(lambda: defaultdict(float))
        self.sortIndex=defaultdict(list)
        self.bigram=defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        

    def buildIndex(self):
        stemmer=PorterStemmer()
        stopwords = [ "a","about","above","after","again","against","all","am","an","and","any","are","aren't",
                 "as","at","be","because","been","before","being","below","between","both","but","by","can't",
                 "cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during",
                 "each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he",
                 "he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i",
                 "i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more",
                 "most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours",
                 "ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some",
                 "such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they",
                 "they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't",
                 "we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while",
                 "who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your",
                 "yours","yourself","yourselves"]
        
       
        with open("bookkeeping.json", "r") as read_json:
            data = json.load(read_json)
            for key in data:
                path=os.path.join("C:/Users/Randy Tran/Desktop/WEBPAGES_RAW",key)
                with open(path,"r",encoding='utf-8') as read_file:
                    contents=BeautifulSoup(read_file, "lxml")
                                    
                    for tag in [tag.extract() for tag in contents.find_all(['title','strong','b','h1','h2','h3','h4','h5','h6','meta'])]:
                        result=""
                        bigramResult=""
                        bigramFlag=0
                        
                        if tag.name=="meta":
                            if (tag.get("name",None)=="keywords" or tag.get("name",None)=="description"
                            or tag.get("name",None)=="author" or tag.get("name",None)=="title" or tag.get("name",None)=="abstract"):
                                text=tag.get("content",None)
                                if text==None:
                                    continue
                            else:
                                continue
                        else:
                            text=tag.get_text()
                                
                        for character in text:  
                            if ((character.isalnum() and character.isascii()) or character=="'"):
                                result+=character
                            else:
                                if result !="":
                                    result=result.lower()
                                    if (result not in stopwords):
                                        stemmed=stemmer.stem(result)
                                        self.index[stemmed][key]["tf"]+=1
                                        self.index[stemmed][key]["tag"]+=0.5
                                        
                                        bigramFlag+=1
                                        if bigramFlag==1:
                                            bigramResult+=stemmed
                                        elif bigramFlag==2:
                                            bigramFlag=1
                                            bigramResult+=(" "+stemmed)
                                            self.bigram[bigramResult][key]["tf"]+=1
                                            self.bigram[bigramResult][key]["tag"]+=0.5
                                            bigramResult=stemmed
                                            
                                    result= ""
            
                        if result != "":
                            result=result.lower()
                            if (result not in stopwords):
                                stemmed=stemmer.stem(result)
                                self.index[stemmed][key]["tf"]+=1
                                self.index[stemmed][key]["tag"]+=0.5
                                      
                                bigramFlag+=1
                                if bigramFlag==2:
                                    bigramResult+=(" "+stemmed)
                                    self.bigram[bigramResult][key]["tf"]+=1
                                    self.bigram[bigramResult][key]["tag"]+=0.5
                                       
                    for tag in contents.find_all():
                        result=""
                        bigramResult=""
                        bigramFlag=0
                        for character in tag.get_text():
                            if ((character.isalnum() and character.isascii()) or character=="'"):
                                result+=character
                            else:
                                if result !="":
                                    result=result.lower()
                                    if (result not in stopwords):
                                        stemmed=stemmer.stem(result)
                                        self.index[stemmed][key]["tf"]+=1
                                        
                                        bigramFlag+=1
                                        if bigramFlag==1:
                                            bigramResult+=stemmed
                                        elif bigramFlag==2:
                                            bigramFlag=1
                                            bigramResult+=(" "+stemmed)
                                            self.bigram[bigramResult][key]["tf"]+=1
                                            bigramResult=stemmed
                                    result= ""

                        if result != "":
                            result=result.lower()
                            if (result not in stopwords):
                                stemmed=stemmer.stem(result)
                                self.index[stemmed][key]["tf"]+=1
                        
                                bigramFlag+=1
                                if bigramFlag==2:
                                    bigramResult+=(" "+stemmed)
                                    self.bigram[bigramResult][key]["tf"]+=1
                    
                      
        for term in self.index:
            df=len(self.index[term])
            for docID in self.index[term]:
                if "tag" in self.index[term][docID]:
                    tfidf=round(((1+math.log10(self.index[term][docID]["tf"]))*(math.log10(37497/df)))+self.index[term][docID]["tag"],2)
                else:
                    tfidf=round((1+math.log10(self.index[term][docID]["tf"]))*(math.log10(37497/df)),2)
                heappush(self.sortIndex[term], (-1*tfidf, docID))
        
        self.index.clear()
        
        for term in self.sortIndex:
            while self.sortIndex[term]:
                pair=heappop(self.sortIndex[term])
                docID=pair[1]
                tfidf=-1*pair[0]
                if tfidf>3:
                    self.championList[term][docID]=tfidf
                    self.championDocs[term]["docs"].append(docID)
                else:
                    self.newIndex[term][docID]=tfidf
                    self.indexDocs[term]["docs"].append(docID)   
                              
        with open('index.json', 'w',encoding="utf-8") as i:
            json.dump(self.newIndex, i)
        
        with open('championList.json', 'w',encoding="utf-8") as i:
            json.dump(self.championList, i)
        
        with open('championDocs.json', 'w',encoding="utf-8") as i:
            json.dump(self.championDocs, i)
        
        with open('indexDocs.json', 'w',encoding="utf-8") as i:
            json.dump(self.indexDocs, i)
        
        self.newIndex.clear()
        self.championList.clear()
        self.championDocs.clear()
        self.indexDocs.clear()
        self.sortIndex.clear() 
                        
        for term in self.bigram:
            df=len(self.bigram[term])
            for docID in self.bigram[term]:
                if "tag" in self.bigram[term][docID]:
                    tfidf=round(((1+math.log10(self.bigram[term][docID]["tf"]))*(math.log10(37497/df)))+self.bigram[term][docID]["tag"],2)
                else:
                    tfidf=round((1+math.log10(self.bigram[term][docID]["tf"]))*(math.log10(37497/df)),2)
                heappush(self.sortIndex[term], (-1*tfidf, docID))

        self.bigram.clear()
        
        for term in self.sortIndex:
            while self.sortIndex[term]:
                pair=heappop(self.sortIndex[term])
                docID=pair[1]
                tfidf=-1*pair[0]
                if tfidf>=4:
                    self.championList[term][docID]=tfidf
                    self.championDocs[term]["docs"].append(docID)
                else:
                    self.newIndex[term][docID]=tfidf
                    self.indexDocs[term]["docs"].append(docID)   
                    
        
        with open('bigramIndex.json', 'w',encoding="utf-8") as i:
            json.dump(self.newIndex, i)
        
        with open('bigramChampionList.json', 'w',encoding="utf-8") as i:
            json.dump(self.championList, i)
            
        with open('bigramChampionDocs.json', 'w',encoding="utf-8") as i:
            json.dump(self.championDocs, i)
        
        with open('bigramIndexDocs.json', 'w',encoding="utf-8") as i:
            json.dump(self.indexDocs, i)
    
if __name__ == "__main__":
    i = index_constructor()
    i.buildIndex()
    
                
        
                
                
        