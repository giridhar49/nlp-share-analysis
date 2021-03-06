__author__ = 'jojofabe'

from nltk.corpus import stopwords
from nltk import FreqDist
import json
import nltk

from nltk import word_tokenize,sent_tokenize

nltk.download('punkt')
'''
    setting up topics, description and title
'''
topics_table = {}

#may need to tweak this a little
with open('comp/100_comp.json') as data_file:
    data = json.load(data_file)

results = data['results']

def setUpTopicsToDictionary():
    #loading the topics into the dictionary
    for data_point in results:
        for s in data_point['subjects']:
            if '-' in s:
                subject = s
                topic = subject[subject.index('-')+2: len(subject)]
                if topic not in topics_table:
                    if data_point['publisher']["name"] != '':
                        topics_table[topic] = [{"title":data_point['title'],
                                           "publisher":data_point['publisher']["name"],
                                           "summary":data_point['description'],
                                            }]
                    else:
                        topics_table[topic] = [{"title":data_point['title'],
                                           "summary":data_point['description'],
                                            }]
                else:
                     topics_table[topic].append({'title':data_point['title'],
                                           'publisher':data_point['publisher'],
                                           'summary':data_point["description"],
                                            })



topics_table_title = {}
topics_table_description = {}

built_topic_stop_words = {}
built_topic_context = {} #we take the most contextual nouns of each description
#and put tags on the context

topics_table_noun_only_title = {}
topics_table_noun_only_description = {}

#setting up the nouns from the corpus, we make this assumption
#good research papers are not opinionated, they are technical, use specified
#words to ensure their message and findings are published successfully. This is a
#an observation based on me <jouella>'s observation with research. As thus
#we only care about nouns.
def setUpNounsTopicTable():
    all_description = ''
    all_topics = ''
    for topic in topics_table:
        for elem in topics_table[topic]:
            if(len(elem["description"]) > 3):
                all_description += str(elem["description"])

            if(len(elem["topics"]) > 3):
                all_topics += str(elem["topics"])

        current_description_tag = nltk.pos_tag(all_description.split())
        topics_table_noun_only_description[topic] = [noun for noun, pos in current_description_tag if pos == 'NNP']
        current_topic_tag = nltk.pos_tag(all_topics.split())
        topics_table_noun_only_title[topic] = [noun for noun, pos in current_topic_tag if pos == 'NNP']

    #Start print statement
    for key in topics_table_noun_only_description:
        print key, topics_table_noun_only_description[key], '\n'
    #end print statement

    # this needs more more work in setting up.

'''
We want to improve data quality here by removing words that appear the most
frequent, the sole being is that we want to improve the sub-categorization of
the data point
'''
# essentially we are finding the most common nouns in each topic, reason being is
# to only count the ones that actually say something meaningful
# Was this effective? Setting up own stop words,
# The down-ward setbacks would be the missed words that actually are important,
# how do we find that they are important?
# How much is enough words to remove?
# Will this improve anything? Definitely questions that needs answered
def setUpOwnSubjectStopWords():
    for topic in topics_table_noun_only_title:
        #only limiting it to a specified length

        #might want to look into the numeric part
        all_description = [ds for ds in topics_table_noun_only_description[topic] if len(ds) > 5].join()
        all_topics = [topics for topics in topics_table_noun_only_title[topic] if len(ds) > 5].join()


        fdist_description = FreqDist(all_description)
        fidst_topics = FreqDist(all_topics)

        ten_most_common_descr = fdist_description.most_common(10)
        ten_most_common_topic = fdist_description.most_common(10)
        built_topic_stop_words[topic] = [word for word,freq in ten_most_common_descr ]
        built_topic_stop_words[topic].append([word for word, freq in ten_most_common_topic])

        #here we set up the top 5-10 words (we need to look into the data more to find
        #the hard margin of the good numerical value to stop, but for simplicity sake, we
        #pick 5 for now, let's see how our accuracy changes when change the most frequent words


    for topic in built_topic_stop_words:
        print built_topic_stop_words[topic]
        print "\n"


# this is a cool way to find the features of the data set and how they aggregate with one another
# might be cool to visualize, perhaps certain names appear more often - might want to look into
# data integrity of a particular data set - gives you some statistical analysis of how data is
# flawed
def setUpClusteringOnWords():
    x = {}

# set up a model in which the neighboring words are taken into consideration, this is simply
# annotating each words to come up with the best way of adding tags, might give more
# pertinent information on the relativeness of a particular data-set
def setUpContextTitleDescriptionTable():
    x = {}

#these are better object holders for storing the topics and description, for now,
#readability wise, it's much better
def setUpStopWordsTopicDescription():
    stop_words = stopwords.words("english")
    temp_descriptor = []
    temp_descriptor = []
    #remove words in topics_table if they appear in stop_words
    for topic in topics_table:
        topics_table_title[topic] = []
        for element in topic:
            for w in topic[element]:
                temp_descriptor.append(word for word in w["description"].text() if word not in stop_words)

                topics_table_title[topic].append(temp_descriptor)

            temp_title = [w for w in element["title"].text() if w not in stop_words]
            topics_table_description[topic].append(temp_title) #just add the title for now

'''
This is the second iteration of filtering through and getting the important
and relevant words

This is the experimental part in which we try to see which words would
yield the most pertinent information
'''
topics_table_nouns = {}
for topic in topics_table:
    topics_table_nouns[topic] = []
    for element in topic:
        #this extracts the noun
        topics_table_nouns[topic].append('');




'''
methods to call to set up everything
'''
setUpTopicsToDictionary()
setUpStopWordsTopicDescription()



