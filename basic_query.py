import json
from nltk.stem import PorterStemmer
import math
from heapq import heappush, heapify,heappop

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
        

def search(i,champDocs, idxDocs, index,championIndex):

    filteredQT=dict()
    for term in i:
        if term in index and term in championIndex:
            df=len(index[term])+len(championIndex[term])
        elif term in index:
            df=len(index[term])
        elif term in championIndex:
            df=len(championIndex[term])
            
        idf=math.log10(37497/df)
        filteredQT[term]=idf
    
    queryLength=math.sqrt(sum(i*i for i in filteredQT.values()))
    for term in filteredQT:
        filteredQT[term]=filteredQT[term]/queryLength

    docLength=None
    docWeight=None
    scoreDictLength=0
    
    heap=[]
    heapify(heap)
    
    for docID in champDocs:
        docWeight=dict()
        docLength=0
        for term in i:
            if docID in championIndex[term]:
                tfidf=championIndex[term][docID]
                docWeight[term]=tfidf
                docLength+=(tfidf*tfidf)
            else:
                docWeight[term]=0
        if docLength!=0: 
            sqrtDocLength=math.sqrt(docLength)
            for term in docWeight:
                docWeight[term]=docWeight[term]/sqrtDocLength
            
            scoreCount=0
            for term in filteredQT:
                scoreCount+=filteredQT[term]*docWeight[term]
                
            heappush(heap, (-1*(scoreCount),docID))
            scoreDictLength+=1
          
    if scoreDictLength<20:
        for docID in idxDocs:
            docWeight=dict()
            docLength=0
            for term in i:
                if docID in index[term]:
                    tfidf=index[term][docID]
                    docWeight[term]=tfidf
                    docLength+=(tfidf*tfidf)
                else:
                    docWeight[term]=0
            
            if docLength!=0:       
                sqrtDocLength=math.sqrt(docLength)
                for term in docWeight:
                    docWeight[term]=docWeight[term]/sqrtDocLength
                
                scoreCount=0
                for term in filteredQT:
                    scoreCount+=filteredQT[term]*docWeight[term]
                    
                heappush(heap, (-1*(scoreCount),docID))
    
    return heap
           
with (open("bookkeeping.json", "r", encoding='utf-8') as read_bookkeeping, open("index.json", "r", encoding='utf-8') as read_json, 
    open("championList.json", "r", encoding='utf-8') as read_json1,open("championDocs.json", "r", encoding='utf-8') as docs, 
    open("indexDocs.json", "r", encoding='utf-8') as docs1, open("bigramIndex.json", "r", encoding='utf-8') as bigram_read_json,
    open("bigramChampionList.json", "r", encoding='utf-8') as bigram_read_json1, open("bigramChampionDocs.json", "r", encoding='utf-8') as bigramDocs,
    open("bigramIndexDocs.json","r",encoding="utf-8") as bigramDocs1):

    bookkeeping=json.load(read_bookkeeping)
    
    index = json.load(read_json)
    championIndex=json.load(read_json1)
    championDocs=json.load(docs)
    indexDocs=json.load(docs1)
    
    bigramIndex = json.load(bigram_read_json)
    bigramChampionIndex=json.load(bigram_read_json1)
    bigramChampionDocs=json.load(bigramDocs)
    bigramIndexDocs=json.load(bigramDocs1)

    def search_function(search_query):

        # Filter out stopwords from search query and run it through the stemmer.
        i=[stemmer.stem(token) for token in search_query.split() if token not in stopwords]

        results_array = []
        print("Results:")

        queryLength=len(i)
        if queryLength==1:
            for docID in championIndex[i[0]]:
                print(bookkeeping[docID])
                results_array.append(bookkeeping[docID])
            if len(championIndex[i[0]])<20:
                for docID in index[i[0]]:
                    print(bookkeeping[docID])
                    results_array.append(bookkeeping[docID])
                
        elif queryLength==2:
            new_i=[" ".join(i)]
            heap1=search(new_i, bigramChampionDocs[new_i[0]]["docs"], bigramIndexDocs[new_i[0]]["docs"],bigramIndex, bigramChampionIndex)
            while heap1:
                heap_link1 = bookkeeping[heappop(heap1)[1]]
                print(heap_link1)
                results_array.append(heap_link1)
            if len(heap1)<20:
                champDocs={docId for term in i for docId in set(championDocs[term]["docs"])-(set(bigramChampionDocs[new_i[0]]["docs"]).union(set(bigramIndexDocs[new_i[0]]["docs"])))}
                idxDocs={docId for term in i for docId in set(indexDocs[term]["docs"])-(set(bigramChampionDocs[new_i[0]]["docs"]).union(set(bigramIndexDocs[new_i[0]]["docs"])))}
                heap2=search(i, champDocs, idxDocs, index, championIndex)
                while heap2:
                    heap_link2  =bookkeeping[heappop(heap2)[1]]
                    print(heap_link2)
                    results_array.append(heap_link2)
        else:
            champDocs={docID for term in i for docID in championDocs[term]["docs"]}
            idxDocs={docID for term in i for docID in indexDocs[term]["docs"]}
            heap1=search(i, champDocs, idxDocs,index, championIndex)
            while heap1:
                heap_link3 = bookkeeping[heappop(heap1)[1]]
                print(heap_link3)
                results_array.append(heap_link3)
                
        print()
        return results_array

                

if __name__ == "__main__":
    search_query = input("Search: ")
    search_function(search_query)