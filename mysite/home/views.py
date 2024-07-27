from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from urllib.parse import unquote
from mysite import settings
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
import os
import time

BASE_DI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("Base Directory: ", BASE_DI)

chatbot = ChatBot('PSBot',
                  storage_adapter="chatterbot.storage.SQLStorageAdapter",
                  database=settings.DATABASES,
                  )

trainer1 = ChatterBotCorpusTrainer(chatbot)

trainer1.train("chatterbot.corpus.english.conversations")
trainer1.train("chatterbot.corpus.english.greetings")

trainer = ListTrainer(chatbot)

trainer.train([
    "Who made this website",
    "Sarvesh Agrawal, Naman Bhansali, Raj Bora, Siddhant Burse",
])


def index(request):
    return render(request, 'Homepage.html')


def aboutus(request):
    return render(request, 'Aboutus.html')


def home(request, template_name="home.html"):
    return render(request, template_name)


@csrf_exempt
def get_response(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data = unquote(data)
        data = data[4:]
        if data.find('+') > -1:
            data = data.replace("+", " ")
        try:
            if data.find('news-') == 0 or data.find('News-') == 0:
                simplefilter(action='ignore', category=FutureWarning)
                filename = BASE_DI + '\\home\\word_to_vec.sav'
                model = joblib.load(filename)
                vocab = list(model.wv.key_to_index)
                global stopWords
                stopWords = ['be', 'which', 'y', 'myself', 'our', 'doing', 'isn', 'ma', 'o', 'yourself', 's', 'itself',
                             'ourselves',
                             'does', 'has', 'my', 'll', 'he', 'own', 'or', 'having', 'mustn', 'at', 'too', 'herself',
                             'other',
                             'themselves', 'very', 'don', 'me', 'these', 'with', "she's", 'can', 'is', 'off', 'in',
                             'to',
                             'shan',
                             'those', 'most', 'himself', 'them', 'there', 'ain', 'hasn', 'their', 'nor', 've', 'she',
                             'was',
                             'hadn',
                             'being', 'both', "it's", 'just', 'up', 'as', 'wouldn', 'aren', 'some', 'his', 'we', 'same',
                             'and',
                             'more',
                             'ours', 'because', 'mightn', 'of', 'will', 'do', 'on', 'are', 'no', 'if', "you're", 't',
                             'about',
                             'so',
                             'after', 'few', 'had', 'yourselves', 'while', 'd', 'over', 'this', 'any', 'its', 'once',
                             'that',
                             'a',
                             'again', 'how', 'it', 'who', 'than', "you'd", 'but', 'until', 'each', 'why', "you'll",
                             'you',
                             'from',
                             'further', 'an', 'through', 'yours', 'have', 'into', 'your', 'should', "mightn't", 'all',
                             'were',
                             'by',
                             're', 'been', 'hers', 'haven', 'him', "that'll", 'during', 'down', 'they', 'out',
                             "should've",
                             'theirs',
                             'm', 'the', 'whom', 'when', 'what', 'did', 'her', 'here', 'where', "you've", 'am',
                             "shan't",
                             'only',
                             'such', "mustn't", 'then', 'needn', "hadn't", 'weren', 'under', 'i', 'for']

                def extract(statement):
                    text = str(statement)
                    global bodys
                    safe_text = text

                    list_news_sources = [' inshorts', ' the hindu', ' india today',
                                         ' times of india', ' free press', ' livemint', ' hindustan times']
                    list_news_links = ["https://inshorts.com/en/news/",
                                       "https://www.thehindu.com/",
                                       "https://www.indiatoday.in/",
                                       "https://timesofindia.indiatimes.com/",
                                       "https://www.freepressjournal.in/",
                                       "https://www.livemint.com/",
                                       "hindustantimes.com/",
                                       ]

                    bodys = []

                    pages_links = []

                    for k in range(0, len(list_news_sources)):
                        text = safe_text
                        text = text + list_news_sources[int(k)]
                        time_to_sleep1 = random.randint(3, 5)
                        time.sleep(time_to_sleep1)

                        A = (
                            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 "
                            "Safari/537.36",
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/41.0.2227.1 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/41.0.2227.0 "
                            "Safari/537.36",
                            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/33.0.1750.517 Safari/537.36",
                        )
                        Agent = A[random.randrange(len(A))]

                        v = ("--window-size=1100,1000", "--window-size=2200,2000", "--window-size=880,700",
                             "--window-size=900,1100",
                             "--window-size=770,600")
                        vp = v[random.randrange(len(v))]

                        headers = {'user-agent': Agent}
                        options = webdriver.ChromeOptions()
                        options.add_argument("headless")
                        options.add_argument('--ignore-certificate-errors')
                        options.add_argument('--incognito')
                        options.add_argument("user-agent=" + str(Agent))
                        options.add_argument(vp)
                        options.add_experimental_option("excludeSwitches", ["enable-automation"])
                        options.add_experimental_option('useAutomationExtension', False)
                        driver = webdriver.Chrome(executable_path=BASE_DI + "\\home\\chromedriver", options=options)
                        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": Agent})

                        list_se_links = ["https://www.google.com/"]
                        se = list_se_links[random.randrange(len(list_se_links))]
                        driver.get(se)
                        search_box = driver.find_element_by_xpath('//input[@name="q"]')
                        search_box.send_keys(text)
                        search_box.send_keys(Keys.ENTER)

                        second_check = None
                        rotation = None
                        i = 0

                        while True:
                            page_no = driver.find_elements_by_xpath("//table[@class='AaVjTc']/tbody/tr/td/a")
                            try:
                                if i != 0:
                                    page_no[i].click()
                                    time_to_sleep2 = random.randint(2, 4)
                                    time.sleep(time_to_sleep2)
                                else:
                                    pass
                            except IndexError:
                                break
                            else:
                                pass

                                first_check = 0
                                value = driver.find_elements_by_xpath("//a[@href]")
                                for each_val in value:
                                    link = each_val.get_attribute('href')
                                    if list_news_links[k] in link:
                                        print(link)
                                        if '&ved=' in link:
                                            split_string = link.split("&ved=", 1)
                                            link = split_string[0]
                                        if '&url=' in link:
                                            split_string1 = link.split("&url=", 1)
                                            link = split_string1[1]
                                        pages_links.append(link)
                                        print("Link: ", link)
                                        try:
                                            r = requests.get(link, headers=headers)
                                            time_to_sleep3 = random.randint(2, 4)
                                            time.sleep(time_to_sleep3)
                                            doc = Document(r.text)
                                            headlines = doc.short_title()
                                        except:
                                            pass
                                        else:
                                            bodys.append(headlines)
                                        first_check += 1

                                if first_check == 0:
                                    if second_check is None:
                                        second_check = 1
                                        rotation = i
                                    elif second_check == 1 and i == rotation + 1:
                                        second_check = 2
                                        break
                                    elif second_check == 1:
                                        second_check = 1
                                        rotation = i
                                    else:
                                        second_check = None

                                i += 1
                        text = safe_text
                        driver.quit()

                    print("Complete links \n", "\n".join(pages_links))
                    print("Complete headlines \n", "\n".join(bodys))

                def remove_stopwords(data):
                    words_filtered = []
                    global stopWords
                    words = word_tokenize(data)
                    for w in words:
                        w = w.lower()
                        global stopWords
                        if w not in stopWords:
                            words_filtered.append(w)
                    table = str.maketrans('', '', string.punctuation)
                    for i in range(len(words_filtered)):
                        words_filtered[i] = words_filtered[i].translate(table)
                    ans = ""
                    for i in range(len(words_filtered)):
                        ans = ans + " " + words_filtered[i]
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

                def max_min_func(headline):
                    global bodys
                    head = remove_stopwords(headline)
                    print(head)
                    try:
                        count = 0
                        max_res = 0
                        min_res = 2.0
                        for body in bodys:
                            statement = remove_stopwords(body)
                            s1_afv = avg_feature_vector(head, model=model, num_features=100, vocab=vocab)
                            s2_afv = avg_feature_vector(statement, model=model, num_features=100, vocab=vocab)
                            s1_afv_is_all_zero = np.all((s1_afv == 0))
                            s2_afv_is_all_zero = np.all((s2_afv == 0))
                            if s1_afv_is_all_zero or s2_afv_is_all_zero:
                                cos = 1
                            else:
                                cos = spatial.distance.cosine(s1_afv, s2_afv)
                            sim = 1 - cos
                            print("\nSimilarity: ", sim)

                            if not math.isnan(sim):
                                if sim > max_res:
                                    max_res = sim
                                if sim < min_res:
                                    min_res = sim
                            count = count + 1
                            if count == 5:
                                break
                        return [max_res, min_res]
                    except:
                        return []

                filename1 = BASE_DI + '\\home\\SVM_model.sav'
                model_svm = joblib.load(filename1)

                filename2 = BASE_DI + '\\home\\LR_model.sav'
                model_lr = joblib.load(filename2)

                pro1 = 0
                pro2 = 0
                input_data = data[5:]
                print("Input Data: ", input_data)
                statement = input_data
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
                print("\nUsing SVM model, statement is true by " + str(pro1 * 100) + " %")
                print("\nUsing LR model, Statement is true by " + str(pro2 * 100) + " %")
                print("\nUsing combined model, Statement is true by " + str(((pro1 + pro2) / 2) * 100) + " %")
                stt = "Using combined model, Statement is true by " + str(round(((pro1 + pro2) / 2) * 100,2)) + " %"
                print("\n")
                chat_response = stt
            else:
                chat_response = chatbot.get_response(data).text
        except Exception as e:
            print(e)
            chat_response = "No Response."

    return HttpResponse(str(chat_response))
