# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser # Universal feed parser to parse Atom and RSS feeds in Python
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    ''' String '''
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_subject(self):
        return self.subject
    def get_summary(self):
        return self.summary
    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
    '''Subclass of Trigger. Takes a string word as an argument'''
    
    def __init__(self, word):
        '''Initialize WordTrigger as a subclass of Trigger'''
        self.word = word
        
    def is_word_in(self, text):
        word = self.word.lower()
        text = text.lower()
        
        '''If word is present in text, True, otherwise false. Case insensitive.'''
        # First, parse text by punctuation in string.punctuation
        for punc in string.punctuation:
            if punc in text:
                text = text.replace(punc, ' ')
        # Second, check to see if word is in parsed text.
        wordlist = text.split(' ')
        return word in wordlist     #Quicker way than if/else loop to return True/False
        
# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    '''Subclass of the class WordTrigger'''
    def __init__(self, word):
        '''Initialize WordTrigger as a subclass of Trigger, taking into the argument of the instance whatever word is passed in when instantiating the class'''
        WordTrigger.__init__(self, word)
    def evaluate(self, story):
        '''Evaluates to True if the title section of the NewsStory object contains the word in question'''
        # Return True if target word is in title of the NewsStory
        return self.is_word_in(story.get_title())
        # self. is referenced because this is a subclass
        # story.get_title() produces the title of the NewsStory class

# TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):
    '''Subclass of the class WordTrigger'''
    def __init__(self, word):
        '''Initialize WordTrigger as a subclass of Trigger, taking into the argument of the instance whatever word is passed in when instantiating the class'''
        WordTrigger.__init__(self, word)
    def evaluate(self, story):
        '''Evaluates to True if the subject section of the NewsStory object contains the word in question'''
        # Return True if target word is in subject of the NewsStory
        return self.is_word_in(story.get_subject())

# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    '''Subclass of the class WordTrigger'''
    def __init__(self, word):
        '''Initialize WordTrigger as a subclass of Trigger, taking into the argument of the instance whatever word is passed in when instantiating the class'''
        WordTrigger.__init__(self, word)
    def evaluate(self, story):
        '''Evaluates to True if the subject section of the NewsStory object contains the word in question'''
        # Return True if target word is in summary of the NewsStory
        return self.is_word_in(story.get_summary())

# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
    '''A subclass of trigger that produces the inverse output of another trigger'''
    def __init__(self, trigger):
        self.trigger = trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story) #Quicker than if/else loop

# TODO: AndTrigger
class AndTrigger(Trigger):
    '''A subclass of trigger that takes two triggers as arguments to its constructor and fires on a news story only if both of the inputted triggers would fire on that item'''
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        '''Evaluates to True iff BOTH input triggers fire on the item'''
        # print 'Evaluating the following triggers:'
        # print 'Trigger1 type: ',type(self.trigger1)
        # print 'Trigger2 type: ',type(self.trigger2)
        # print 'Trigger1: ',self.trigger1, self.trigger1.get_title(), self.trigger1.get_subject(), self.trigger1.get_summary()
        # print 'Trigger2: ',self.trigger2, self.trigger2.get_title(), self.trigger2.get_subject(), self.trigger2.get_summary()
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# TODO: OrTrigger
class OrTrigger(Trigger):
    '''A subclass of trigger that takes two triggers as arguments to its constructor and fires on a news story if either of the inputted triggers would fire on that item'''
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        '''Evaluates to True if either input triggers fire on the item'''
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    '''A subclass of Trigger (NOT of word trigger, as it has important differences) that fires when a given phrase is in any of the news story's subject, title, or summary'''
    def __init__(self, phrase):
        self.phrase = phrase
    def evaluate(self, story):
        return self.phrase in story.get_subject() or self.phrase in story.get_title() or self.phrase in story.get_summary()

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    Returns stories as a list
    """
    # TODO: Problem 10
    storylist = []
    
    # print 'beginning loop in filter_stories'
    for story in stories:
        # print 'story is: ',story
        # print 'story title, summary, and subject are: ', story.get_title(), story.get_summary(), story.get_subject()
        for trigger in triggerlist:
            # print 'trigger is: ',trigger
            if trigger.evaluate(story): # Second error. type(trigger) returns trigger classes
                # print 'trigger.evaluate(story) is: ',trigger.evaluate(story)
                storylist.append(story)
                break
    return storylist

#======================
# Part 4
# User-Specified Triggers
#======================

# Create a helper function for parsing trigger config file
def makeTrigger(trigger_map, trigger_type, params, name):
    """
    Takes in a mapping of names to trigger instance, the type of trigger to make,
    and the list of parameters to the constructor, and returns a new
    trigger instance. This can then be used to parse read trigger config function.

    trigger_map: dictionary with names as keys (strings) and triggers as values
    trigger_type: string indicating the type of trigger to make (ex: "TITLE", "AND")
    params: list of strings with the inputs to the trigger constructor (ex: ["world"], ["t2", "t3"])
    name: a string representing the name of the new trigger (ex: "t1", "t2")

    Returns a new instance of a trigger (ex: TitleTrigger, AndTrigger).
    Adds to/modifies trigger_map, adding a new key-value pair for this trigger.  Key = triggername, value = instance.
    """
    
    # Loop depending on the type of trigger
    if trigger_type == "TITLE":
        trigger = TitleTrigger(params[0])

    elif trigger_type == "SUBJECT":
        trigger = SubjectTrigger(params[0])

    elif trigger_type == "SUMMARY":
        trigger = SummaryTrigger(params[0])

    elif trigger_type == "NOT":
        trigger = NotTrigger(trigger_map[params[0]])

    elif trigger_type == "AND":
        trigger = AndTrigger(trigger_map[params[0]], trigger_map[params[1]])

    elif trigger_type == "OR":
        trigger = OrTrigger(trigger_map[params[0]], trigger_map[params[1]])

    elif trigger_type == "PHRASE":
        trigger = PhraseTrigger(" ".join(params))

    else:
        return None

    trigger_map[name] = trigger
    
# Read the trigger config file
def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Read in the file and eliminate blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    
    # Loop through lines and use the makeTrigger function to make a trigger 
    trigger_set = []
    trigger_map = {}
    
    for line in lines:
        splitline = line.split(' ')
        if splitline[0] != 'ADD':
            # makeTrigger(trigger_map, trigger_type, params, name)
            trigger = makeTrigger(trigger_map, splitline[1], splitline[2:], splitline[0])
        
        if splitline[0] == 'ADD':
            for i in splitline[1:]:
                trigger_set.append(trigger_map[i])
                
    return trigger_set
    
import thread

def main_thread(p):
    # # A sample trigger list - you'll replace
    # # this with something more configurable in Problem 11
    # t1 = SubjectTrigger("Obama")
    # t2 = SummaryTrigger("MIT")
    # t3 = PhraseTrigger("Supreme Court")
    # t4 = OrTrigger(t2, t3)
    # triggerlist = [t1, t4]
    
    # TODO: Problem 11
    triggerlist = readTriggerConfig("triggers.txt")
    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))
        
        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

