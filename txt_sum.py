import pdf_access as pa
import re,heapq,nltk






def clean_text(ip):
    
    # Removing Square Brackets and Extra Spaces
    ip = re.sub(r'\[[0-9]*\]', ' ', ip)
    ip=  re.sub('etc.',' ',ip)
    ip = re.sub(r'\s+', ' ', ip)

    # Removing special characters and digits
    formip = re.sub('[^a-zA-Z]', ' ', ip )  
    formip = re.sub(r'\s+', ' ', ip)
    
    return formip

def summarize(ip,opt='1'):

    formip=clean_text(ip)
    stopwords = nltk.corpus.stopwords.words('english')
    
    #Find Weighted Frequency of Occurrence
    word_frequencies = {}
    sentence_list = nltk.sent_tokenize(formip)
    for word in nltk.word_tokenize(formip):  
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        
    #Calculating Sentence Scores
    sentence_scores = {}  
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 60:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences=[]
    if opt =='1':
        sum_limit=int(input("enter manual summary limit"))
        summary_sentences = heapq.nlargest(sum_limit, sentence_scores, key=sentence_scores.get)
        return([summary_sentences,sentence_list])
    if opt =='2':
        maxi=max(sentence_scores.values())
        maxi=(maxi/100)*80
        for a,b in sentence_scores.items():
            if b>maxi:
                summary_sentences.append(a)
        return([summary_sentences,sentence_list])

def get_text(opt):
    if opt=='pdf': 
        obj=pa.main()
        text=pa.get_text(obj)
        ans=summarize(text,input('enter 1 for particular number of summaries and 2 for all sentencs with higer importance'))
        sum_txt,sentence_list=ans[0],ans[1]
        get_flow(sentence_list,sum_txt)
        #for i in sum_txt:
         #   print (i)
    if opt =='txt':
        text=''
        fh=open(input('enter file name  '),'r')
        for line in fh:
            text=text+line
        ans=summarize(text,int(input('enter 1 for particular number of summaries and 2 for all sentencs with higer importance')))
        sum_txt,sentence_list=ans[0],ans[1]
        get_flow(sentence_list,sum_txt)
def get_flow(sentence_list,sum_txt):
    final_sum=[]
    for i in sentence_list:
        if i in sum_txt:
            final_sum.append(i)
    j=0
    set_sum=set(final_sum)
    for k in final_sum:
        if k in set_sum:
            j=j+1
            print(j,')  ',k,'done \n')
            set_sum.remove(k)
    
if __name__=='__main__':
    
    get_text('txt')

                        
