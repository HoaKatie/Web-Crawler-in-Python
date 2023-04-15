import os
import webdev
import myqueue
import json
import math
import matmult

#############################################################################################
def get_title(html_string): # get title from the in between the <title> and </title> tags within the page
    if html_string == "":  # if string is empty, return None
        return None
    else:
        title = html_string.split("<title>")[1].split("</title>")[0] # title is in between the <title> and </title> tags within the page
        return title

# Note: since  the title from <title> may not match the last part of the URL for the page
# Hence, title from the last part of the URL is being used to name files for easy access of data
# This function is NOT BEING USED but JUST TO SHOW how to retrieve title from the page

def get_url_title(URL): # get title from the last part of the URL for the page 
    return URL.split("/")[-1].split(".")[0] 
#############################################################################################
def get_data(html_string):
    if html_string == "":  # if string is empty, return None
        return None
    else:
        body = html_string.split("</p>")[0].split(">")[-1].split("\n") # assuming <p> has attributes, hence, <p> cannot used for split
        return body[1:-1]  # remove empty strings in the list
#############################################################################################
def get_links(html_string, base):  
    if html_string == "":  # if string is empty
        return None
    else:
        urls = html_string.split('href=\"')[1:] #each element will contain absolute or relative url with some extra tags to be removed
        link_ids = list()
        for url in urls:
            if url[:2] == "./": #if url is a relative url
                link_ids.append(base + url[2:].split('\">')[0])
            else: #if url is an absolute url that starts with "http://"
                link_ids.append(url.split('\">')[0])
    return link_ids # the links retrieved from the page is also outgoing links of the page
#############################################################################################
def create_dir(name):
    if os.path.isdir("./" + name): #if the directory already exists
        files = os.listdir("./" + name)  # get list of all files in the directory
        for file in files:
            os.remove(os.path.join("./" + name, file)) # remove all files in subfolder from previous crawl
    else:
        os.makedirs("./" + name)  # if directory not yet present, make new directory
#############################################################################################
def make_idf():  # HAVE TO SEE CRAWL OR USE READ DIRECTORY
    with open("./crawled/html.txt", "r") as f:
        links = f.readline()
        words = f.readline()
    links = links.replace(" ", "").replace("[", "").replace("]", "").replace("\'", "") # remove unnecessary characters or space
    links = links.split(",") # get list of all links (including seed webpage and all interlinked webpages)
    words = words.replace(" ", "").replace("[", "").replace("]", "").replace("\'", "") # remove unnecessary characters or space
    words = words.split(",") # get list of all words that have appeared in any page, in all pages

    total_count = len(links) #total number of documents

    for word in words:
        count = 0
        for url in links:
            title = get_url_title(url)
            with open(f"./crawled/{title}.txt", "r") as file:
                next(file)
                line = file.readline() #get the contents of the page
            line = line.replace(" ", "").replace("[", "").replace("]", "").replace("\'", "")
            line = line.split(",") # a list of all words in the url page
            if word in line:
                count += 1 #count is the number of documents word appears in

        calc = total_count / (1 + count)
        idf = math.log2(calc) # inverse document frequency of that word within the crawled page

        with open(f"./idf/{word}.txt", "w") as file:
            file.write(str(idf)) # the file name is the word while the files store the idf of the word

#############################################################################################
def make_tf_tfidf():
    with open("./crawled/html.txt", "r") as file:
        links = file.readline()
    links = links.replace(" ", "").replace("[", "").replace("]", "").replace("\'", "") # remove unnecessary characters or space
    links = links.split(",") # get list of all links

    for url in links:
        title = get_url_title(url)
        with open(f"./crawled/{title}.txt", "r") as file:
            next(file) 
            line = file.readline()
        line = line.replace(" ", "").replace("[", "").replace("]", "").replace("\'", "")
        line = line.split(",")  # get a list of the words of the page

        total_words = len(line) #total number of words in the document - for idf

        words_lst = list()
        for i in line:
            if i not in words_lst:
                words_lst.append(i) #get list of unique words that appears in the page

        for word in words_lst:
            with open(f"./idf/{word}.txt", "r") as file: #get idf value for the word to calculate tfidf
                stridf = file.readline().strip("\n")
            idf = float(stridf) # all unique words' idfs in all pages have been calculated, hence, unnecessary to check if the idf of the word exists
            
            count = 0
            for item in line:
                if item == word:
                    count += 1   #number of occurence of word in the document

            tf = count / total_words  

            calc = 1 + tf
            tfidf = math.log2(calc) * idf

            filename = title + word # (ie: N-0apple)
            with open(f"./tf-tfidf/{filename}.txt", "w") as file: #create new file to store tfs and tfidfs
                file.write(str(tf))
                file.write("\n")
                file.write(str(tfidf))

#############################################################################################
def make_page_rank():
    matrix = list()
    sites = list()

    with open("./crawled/incoming.json", "r") as file:
        data = json.load(file) # get a dictionary of the incoming links of the page

    for link in data:
        sites.append(link) # get all links from crawled - same as the URLs stored in 'html.txt'
    # Note: the order of urls in sites is important to map to the correct pagerank, which derived from the keys of incoming dictionary. 
    # The order is different from URLs stored in 'html.txt'

    N = len(data) # N number of pages to generate NxN adjacency matrix
    
    for i in range(N):  # CREATE  ADJACENCY MATRIX NxN
        temp = [] # row
        for j in range(N):
            if sites[j] in data[sites[i]]:
                temp.append("1")
            else:
                temp.append("0")
        matrix.append(temp)
        print(temp)

    for i in matrix: # Initial transition probability matrix (by dividing rows by number of 1s):
        if "1" in i:
            count = i.count("1") # count number of 1s in row
            value = 1/count
            for j in range(N):
                if i[j] == "1":
                    i[j] = value
                else:
                    i[j] = 0
        else:
            value = 1/N
            for j in range(N):
                i[j] = value

    matrix = matmult.mult_scalar(matrix, 0.9)
        
    for i in matrix:
        for j in range(N):
            i[j] += (0.1/N) # add alpha/N to each entry of resulting matrix for alpha = 0.1

    prev = [[1/N for i in range(N)], ]
    curr = matmult.mult_matrix(prev, matrix)
    e_dist = matmult.euclidean_dist(prev, curr)

    while e_dist > 0.0001: # stop iteration when Euclidean distance is less than or equal to 0.0001
        prev, curr = curr, matmult.mult_matrix(curr, matrix)
        e_dist = matmult.euclidean_dist(prev, curr)

    with open("./crawled/matrix.txt", "w") as file:
        for i in range(len(curr[0])):  # curr[0] is a list that stores all page rank with index corresponds to the sites 
            title = get_url_title(sites[i])
            line = title + " " + str(curr[0][i])
            file.write(f"{line}\n") # example format: N-3 0.0123456

#############################################################################################

# crawl the webpages and store relevant data
def crawl(seed):

    create_dir('crawled')  # create new directory for the seed URL

    q = myqueue.Queue() # creating object q of the class Queue
    q.put(seed) # put seed url into the queue

    done = set()
    incoming = dict()

    base = seed[::-1].split("/", 1)[1][::-1] + '/' # the base of the absolute url without the name of the url
    all_words = list()

    while not q.empty(): 
        link = q.get() # get the link from the queue while q is not empty
        if link in done: # ignore if link has already been parsed
            continue
        else:
            done.add(link) # add to crawled url list

        html_string = webdev.read_url(link)
        links = get_links(html_string, base)
        data = get_data(html_string)

        for ele in data:
            if ele not in all_words:
                all_words.append(ele) # get all unique words that appears in any pages

        with open(f"./crawled/{get_url_title(link)}.txt", "w") as file:
            file.write(str(links)) # writes OUTGOING LINK as the first line in the file
            file.write("\n")
            file.write(str(data))  # writes DATA of the link into the file

        for i in links:
            if i in incoming:
                incoming[i].append(link)  # if the key url is already inside the incoming dictionary, append the incoming link
            else:
                incoming[i] = [link, ] # if url not yet a key in the dictionary- create new key url and add incoming links
            if i not in done: # enqueue the url if url is not parsed
                q.put(i)

    with open("./crawled/html.txt", "w") as file:
        crawled_links = list(done)  # convert a set of all urls into a list
        file.write(str(crawled_links)) # store all links
        file.write("\n")
        file.write(str(all_words)) # store all unique_words

    with open("./crawled/incoming.json", "w") as json_file: # json file that stores incoming and outgoing links
        json.dump(incoming, json_file) # outgoing is the key of the dictionary while incoming is the items of the key

    create_dir('idf')  # new dir- name idf
    make_idf() # call function to store idf values

    create_dir('tf-tfidf')  # new dir- name tf
    make_tf_tfidf() # call function to store tf and tfidf values

    make_page_rank() # call function to store all page rank values

    return len(done)

