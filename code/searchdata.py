import crawler
import json
import os

# Searchdata is only responsible for calling all crawled data that is stored
# No calculation is being done
# Title is derived from the last part of the URL for the page to avoid reading URLs that does not exist
#############################################################################################
def get_outgoing_links(URL): 
    title = crawler.get_url_title(URL) 

    if not os.path.isfile(f"./crawled/{title}.txt"): #if URL is not crawled 
        return None
    with open(f"./crawled/{title}.txt", "r") as file:
        links = file.readline()
    links = links.replace(" ", "").replace("[\'","").replace("\']\n","")
    links = links.split("\',\'") #get list of all outgoing links
    return links
#############################################################################################
def get_incoming_links(URL): 
    title =  crawler.get_url_title(URL)

    if not os.path.isfile(f"./crawled/{title}.txt"):    
        return None
    with open("./crawled/incoming.json") as file:
        incoming_data = json.load(file)
    try:
        links = incoming_data[URL] # get incoming links from the key URL
    except KeyError: #if the key from the dictionary does not exist, return None
        return None
    return links
#############################################################################################
def get_page_rank(URL):
    title = crawler.get_url_title(URL)

    if not os.path.isfile(f"./crawled/{title}.txt"): # if given url not found in all crawled pages
        return -1
    else:
        with open("./crawled/matrix.txt", "r") as file:
            line = file.readline().strip("\n")
            while line != "":
                line = line.split(" ")
                if title == line[0]: # if matching page rank for the URL is found
                    rank = line[1] # get page rank
                    break
                line = file.readline().strip("\n")
        return float(rank)
#############################################################################################
def get_tf(URL, word):
    title = crawler.get_url_title(URL) 

    if not os.path.isfile(f"./crawled/{title}.txt"): #if URL not found, return 0
        return 0
    else:
        filename = title + word #get the filename in td-tfidf directory
        if not os.path.isfile(f"./tf-tfidf/{filename}.txt"): #if word not found
            return 0
        else:
            with open(f"./tf-tfidf/{filename}.txt", "r") as file:
                tf = file.readline().strip("\n") # first line of the file stores tf
            return float(tf)
#############################################################################################
def get_idf(word): #HAVE TO SEE CRAWL OR USE READ DIRECTORY
    if not os.path.isfile(f"./idf/{word}.txt"): #if word not presented in any crawled documents
        return 0
    else:
        with open(f"./idf/{word}.txt", "r") as file:
            idf = file.readline()
        return float(idf) #return idf of the word
#############################################################################################
def get_tf_idf(URL, word):
    title = crawler.get_url_title(URL) 

    if not os.path.isfile(f"./crawled/{title}.txt"): #if URL not found
        return 0
    else:
        filename = title + word  #get the filename in td-tfidf directory
        if not os.path.isfile(f"./tf-tfidf/{filename}.txt"): #if word not found
            return 0
        else:
            with open(f"./tf-tfidf/{filename}.txt", "r") as file:
                next(file)
                tfidf = file.readline().strip("\n") # tfidf is stored in the second line of the file
            return float(tfidf)

