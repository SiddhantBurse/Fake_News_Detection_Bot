# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 00:01:38 2019

@author: ashu_
"""

# -*- coding: utf-8 -*-
import math
import numpy as np
from scipy import spatial
import string
from nltk.tokenize import word_tokenize
import joblib
from warnings import simplefilter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import random
from readability.readability import Document

simplefilter(action='ignore', category=FutureWarning)
filename = 'word_to_vec.sav'
model = joblib.load(filename)
vocab = list(model.wv.key_to_index)
stopWords = ['be', 'which', 'y', 'myself', 'our', 'doing', 'isn', 'ma', 'o', 'yourself', 's', 'itself', 'ourselves',
             'does', 'has', 'my', 'll', 'he', 'own', 'or', 'having', 'mustn', 'at', 'too', 'herself', 'other',
             'themselves', 'very', 'don', 'me', 'these', 'with', "she's", 'can', 'is', 'off', 'in', 'to', 'shan',
             'those', 'most', 'himself', 'them', 'there', 'ain', 'hasn', 'their', 'nor', 've', 'she', 'was', 'hadn',
             'being', 'both', "it's", 'just', 'up', 'as', 'wouldn', 'aren', 'some', 'his', 'we', 'same', 'and', 'more',
             'ours', 'because', 'mightn', 'of', 'will', 'do', 'on', 'are', 'no', 'if', "you're", 't', 'about', 'so',
             'after', 'few', 'had', 'yourselves', 'while', 'd', 'over', 'this', 'any', 'its', 'once', 'that', 'a',
             'again', 'how', 'it', 'who', 'than', "you'd", 'but', 'until', 'each', 'why', "you'll", 'you', 'from',
             'further', 'an', 'through', 'yours', 'have', 'into', 'your', 'should', "mightn't", 'all', 'were', 'by',
             're', 'been', 'hers', 'haven', 'him', "that'll", 'during', 'down', 'they', 'out', "should've", 'theirs',
             'm', 'the', 'whom', 'when', 'what', 'did', 'her', 'here', 'where', "you've", 'am', "shan't", 'only',
             'such', "mustn't", 'then', 'needn', "hadn't", 'weren', 'under', 'i', 'for']


def extract(statement):
    text = str(statement)
    global bodys
    safe_text = text

    # list_news_sources = [' "inshorts"', ' "the hindu"', ' "india today"', ' "news18"',
    #                      ' "times of india"', ' "free press"', ' "livemint"',
    #                      ' "reuters"', '"hindustan times"', '"business insider"']
    # list_news_links = ["https://inshorts.com/en/news/",
    #                    "https://www.thehindu.com/",
    #                    "https://www.indiatoday.in/",
    #                    "https://www.news18.com/news/",
    #                    "https://timesofindia.indiatimes.com/",
    #                    "https://www.freepressjournal.in/",
    #                    "https://www.livemint.com/",
    #                    "https://www.reuters.com/",
    #                    "hindustantimes.com/",
    #                    "https://www.businessinsider.in/",
    #                    ]
    list_news_sources = [' inshorts', ' the hindu', ' india today',
                         ' times of india', ' free press', ' livemint', ' hindustan times', ' economic times']
    list_news_links = ["https://inshorts.com/en/news/",
                       "https://www.thehindu.com/",
                       "https://www.indiatoday.in/",
                       "https://timesofindia.indiatimes.com/",
                       "https://www.freepressjournal.in/",
                       "https://www.livemint.com/",
                       "hindustantimes.com/",
                       "https://economictimes.indiatimes.com/"
                       ]

    bodys = []

    pages_links = []

    k = 0

    for k in range(0, len(list_news_sources)):
        text = safe_text
        text = text + list_news_sources[int(k)]
        print(list_news_sources[int(k)])
        print(text)

        A = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
             )
        Agent = A[random.randrange(len(A))]
        print(type(Agent))
        print(Agent)

        headers = {'user-agent': Agent}
        options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument("user-agent="+str(Agent))
        driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
        #driver = webdriver.Chrome(executable_path="./chromedriver")
        #driver = webdriver.Chrome("./chromedriver")  # path for Chromedriver
        #driver.execute_cdp_cmd('Network.setUserAgentOverride', {'user-agent': Agent})
        list_se_links = ["https://www.google.com/"]
        se = list_se_links[random.randrange(len(list_se_links))]
        driver.get(se)  # Opens a google page in chrome browser
        search_box = driver.find_element_by_xpath('//input[@name="q"]')  # Find the google search box
        search_box.send_keys(text)  # Enter the keyword "Python"
        search_box.send_keys(Keys.ENTER)  # Clicks the search button

        page_no_ref = driver.find_elements_by_xpath("//table[@class='AaVjTc']/tbody/tr/td/a")
        no_of_pages = len(page_no_ref)
        print("Total Pages: ", no_of_pages + 1)

        second_check = None
        rotation = None
        i = 0

        while True:
            print("Page: ", i + 1)
            page_no = driver.find_elements_by_xpath("//table[@class='AaVjTc']/tbody/tr/td/a")
            try:
                if i != 0:
                    page_no[i].click()
                else:
                    pass
            except IndexError:
                print("\nBreak 1\n")
                break
            else:
                print("\nPages in loop \n")
                print(page_no)

                first_check = 0
                value = driver.find_elements_by_xpath("//a[@href]")
                for each_val in value:
                    link = each_val.get_attribute('href')
                    print("Links Gotten")
                    if list_news_links[k] in link:
                        pages_links.append(link)
                        print("Link: ", link)
                        try:
                            r = requests.get(link, headers=headers)
                            doc = Document(r.text)
                            print(doc.short_title())
                            print(doc.title())
                            headlines = doc.short_title()
                        except:
                            print("No headline")
                        else:
                            print("\nGot Healines: " + headlines + "\n")
                            bodys.append(headlines)
                        first_check += 1
                print("\nNumber of links: " + str(len(pages_links)) + "\n")

                if first_check == 0:
                    print("\nNot Found\n")
                    if second_check is None:
                        second_check = 1
                        rotation = i
                    elif second_check == 1 and i == rotation + 1:
                        second_check = 2
                        print("\n Second Check at end : " + str(second_check) + "\n")
                        break
                    elif second_check == 1:
                        second_check = 1
                        rotation = i
                    else:
                        second_check = None
                    print("\n Second Check Value: " + str(second_check) + "\n")

                i += 1
        text = safe_text
        driver.quit()

    print("Complete links", "\n".join(pages_links))
    print("Complete headlines", "\n".join(bodys))
    print(bodys)


def remove_stopwords(data):
    wordsFiltered = []
    global stopWords
    words = word_tokenize(data)
    for w in words:
        w = w.lower()
        if w not in stopWords:
            wordsFiltered.append(w)
    table = str.maketrans('', '', string.punctuation)
    for i in range(len(wordsFiltered)):
        wordsFiltered[i] = wordsFiltered[i].translate(table)
    ans = ""
    for i in range(len(wordsFiltered)):
        ans = ans + " " + wordsFiltered[i]
    print("Extract Rem Stop Words: ", ans)
    return ans


def avg_feature_vector(sen, model, num_features, vocab):
    words = sen.split()
    feature_vec = np.zeros((num_features,), dtype='float32')
    n_words = 0
    for word in words:
        if word in vocab:
            n_words += 1
            feature_vec = np.add(feature_vec, model.wv[word])
    if n_words > 0:
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec


def frequency_bias(headline):
    global bodys
    head = remove_stopwords(headline)
    try:
        count = 0
        naive_list = []
        for body in bodys:
            statement = remove_stopwords(body)
            naive_list.append(statement)
            count = count + 1
            if count == 5:
                break
        head_list = head.split(' ')
        scarp_map = dict()
        for statement in naive_list:
            scrap_data = statement.split(' ')
            check = dict()
            for word in scrap_data:
                if word and not check.get(word):
                    check[word] = 1
                    if scarp_map.get(word):
                        scarp_map[word] = scarp_map[word] + 1
                    else:
                        scarp_map[word] = 1
        probality_list = []
        for word in head_list:
            if scarp_map.get(word):
                probality_list.append(scarp_map[word] / len(naive_list))
            else:
                probality_list.append(0)
        final_probality = sum(probality_list) / len(probality_list)
        for word in head_list:
            try:
                num = int(word)
                if scarp_map.get(word) and scarp_map[word] <= 2:
                    final_probality = final_probality - 0.1
            except ValueError:
                continue
        return (final_probality)
    except:
        print("FB 3")
        return 0


def max_min_func(headline):
    global bodys
    head = remove_stopwords(headline)
    print(head)
    print("MM 1")
    try:
        print("MM 2")
        count = 0
        max_res = 0
        min_res = 2.0
        print(bodys)
        for body in bodys:
            print("MM For 4")
            print("MM For 43")
            statement = remove_stopwords(body)
            print(statement)
            print("MM For 44")
            s1_afv = avg_feature_vector(head, model=model, num_features=100, vocab=vocab)
            s2_afv = avg_feature_vector(statement, model=model, num_features=100, vocab=vocab)
            print(s1_afv)
            print(s2_afv)
            s1_afv_is_all_zero = np.all((s1_afv == 0))
            s2_afv_is_all_zero = np.all((s2_afv == 0))
            if s1_afv_is_all_zero or s2_afv_is_all_zero:
                cos = 1
            else:
                cos = spatial.distance.cosine(s1_afv, s2_afv)
            sim = 1 - cos
            print("\nSimilarity: ", sim)

            if math.isnan(sim) != True:
                if sim > max_res:
                    max_res = sim
                if sim < min_res:
                    min_res = sim
            count = count + 1
            if count == 5:
                break
        return [max_res, min_res]
    except:
        print("MM 3")
        return []


filename1 = 'SVM_model.sav'
model_svm = joblib.load(filename1)

filename2 = 'LR_model.sav'
model_lr = joblib.load(filename2)

filename3 = 'Final_model.sav'
model_final = joblib.load(filename3)

while True:
    prob1 = 0
    prob2 = 0
    prob3 = 0
    prob4 = 0
    pro1 = 0
    pro2 = 0
    statement = input("Enter the Statement: ")
    extract(statement)
    max_val = 0
    min_val = 2.0
    max_min = max_min_func(statement)
    if max_min:
        max_val = max_min[0]
        min_val = max_min[1]
    if max_val != 0 and min_val != 2.0:
        prob1 = model_svm.predict_proba([[max_val, min_val]])
        pro1 = prob1[0][1]
        prob2 = model_lr.predict_proba([[max_val, min_val]])
        pro2 = prob2[0][1]
    prob3 = frequency_bias(statement)
    print(pro1, pro2, prob3)
    prob4 = model_final.predict_proba([[prob3, pro1, pro2]])
    print("\nStatement is true by "+str(prob4[0][1] * 100)+" %")
    print("\n")
    inp = input("do you want to continue? Yes=1 No=0")
    if inp == '0':
        break
