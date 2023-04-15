import math
import crawler
import searchdata

#############################################################################################
def mergesort(lst):
	if len(lst) >= 2: #if there is at least 2 elements to divide into 2 lists
		midi = len(lst) // 2 # Finding the middle of the list

		# Dividing the initial list into 2
		left = lst[:midi]
		right = lst[midi:]

		mergesort(left) # Recursive sorting the first half
		mergesort(right) # Recursive sorting the second half

		i = j = k = 0

		while i < len(left) and j < len(right):
			if left[i]['score'] >= right[j]['score']: # if score of url in L is >= score of url in R, put dictionary in L to original lst
				lst[k] = left[i]
				i += 1
			else: # if score of url in L is smaller than score of url in R, put dictionary in R to original lst
				lst[k] = right[j]
				j += 1
			k += 1

		# If there is remaining dictionary in L or R, put into lst
		while i < len(left):
			lst[k] = left[i]
			i += 1
			k += 1
		while j < len(right):
			lst[k] = right[j]
			j += 1
			k += 1
#############################################################################################
def search(phrase, boost):
    unique_words = phrase.split(" ") #phrase can contain repeated words
    #unique_words is a list
    query_tfidf = dict()

    for ele in unique_words: # for words in the phrase (no need for condition for word capitalization)
        if ele not in query_tfidf: 
            idf = searchdata.get_idf(ele)
            print("idf" + str(idf))
            calc = 1 + unique_words.count(ele) / len(unique_words)
            print("calc" + str(calc))
            tfidf =  math.log2(calc) * idf
            print("tfidf" + str(tfidf))
            query_tfidf[ele] = tfidf # calculate idf for the query and store in a dictionary

    
    with open("./crawled/html.txt", "r") as file:
        links = file.readline()
    links = links.replace(" ","").replace("[", "").replace("]", "").replace("\'", "").replace("\n", "")
    links = links.split(",") # get all urls from crawled pages

    result = list()
    for url in links:
        link_score = dict()
        numerator = leftdemon = rightdemon = 0
        for word in query_tfidf:
            page_tfidf = searchdata.get_tf_idf(url, word)
            numerator += query_tfidf.get(word) * page_tfidf
            leftdemon += query_tfidf.get(word) * query_tfidf.get(word)
            rightdemon += page_tfidf * page_tfidf
        denominator = (math.sqrt(leftdemon) * math.sqrt(rightdemon)) # perform the necessary calculation
        print("denom " + str(denominator))
        if denominator == 0: # to avoid zero division error
            cosine_similarity = 0
        else:
            cosine_similarity = numerator / denominator 
            print("cosine" + str(cosine_similarity))

        link_score["url"] = url
        t = crawler.get_url_title(url)
        link_score["title"] = t
        if boost: #if boost is True, multiple cosine similarity with page rank
            pagerank = searchdata.get_page_rank(url) 
            link_score["score"] = cosine_similarity * pagerank
            print( "title " + str(t)+ "score "+ str(cosine_similarity * pagerank))
        else:
            link_score["score"] = cosine_similarity 

        result.append(link_score) #currently returning all 
    
      
    #result.sort(key=lambda x: x.get('score'), reverse=True) #-BUILT-IN SORT
    mergesort(result) # I have tried timsort, built-in sort and mergesort and has derived that for large data sets like fruit, merge sort is the most efficient

    return result[:10] #return top 10 ranked search results


search('coconut coconut orange blueberry lime lime lime tomato',True)