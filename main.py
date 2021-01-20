"""
This is the main source code for Bob, a bot made in Python similar to Alexa.
It can get information about people, places, things, or events from Wikipedia, play videos,
get words from Jesus, and get the time. It can also tell jokes.
"""


#######################
##      Imports      ##
#######################
import speech_recognition as sr
import pyaudio
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from jesuswordsttest import fulllist

"""
1. Add already answered questions to a dataset
    a. Make Jesus topics individual files in a folder
2. Add something like "Should I save this?"
3. Query a database using the 5 W's and how
4. When no one is around, be asleep, when someone is around, be awake
5. Eventually make it a robot (hopefully)

Other things

Let the computer remove history from over 2 years ago automatically.
"""

"""
Notes:
Format for text file:

question: who is jesus' questionend

answer: Jesus (c. 4 BC –  AD 30 / 33), also referred to as Jesus of Nazareth or Jesus Christ, was a first-century Jewish preacher and religious leader.' answerend

question: what was the 1993 storm of the century' questionend

answer: The 1993 Storm of the Century (also known as the 93 Superstorm, The No Name Storm, or the Great Blizzard of '93/1993) was a large cyclonic storm that formed over the Gulf of Mexico on March 12, 1993.' answerend

Will split the questions and answers into dictionaries like this:

aqdict = {"who is jesus'": "Jesus (c. 4 BC –  AD 30 / 33), also referred to as Jesus of Nazareth or Jesus Christ, was a first-century Jewish preacher and religious leader.'"...}
So that it can be accessed by the program.
keylist = list(aqdict.list()))
if question in keylist:
    talk(aqdict[question]) # or something like that
else:
    pass # will get it from the internet
"""

listener = sr.Recognizer()
engine = pyttsx3.init()
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)
######################
##    Functions     ##
######################
def talk(text):
    engine.say(text)
    engine.runAndWait()
    
def take_command(bobneeded = True):
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if bobneeded:
                if 'bob' in command:
                    command = command.replace('bob', '')
                    print(command)
                    return command
                else:
                    talk("Would you like me to answer that?")
                    yn = take_command(False)
                    if "yes" in yn.lower():
                        print(command)
                        return command
                    else:
                        talk("Ok.")
                        take_command(False)
            else:
                command = command.replace('bob', '')
                print(command)
                return command
    except:
        pass

def getansweredquestions(question):
    pass

def run_alexa():
    possibleverses = {}
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        print('playing ' + song)
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk("Current time is " + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        if "jesus" in person.lower():
            info=wikipedia.summary(person, 2)
        else:
            info=wikipedia.summary(person, 1)
        with open("answeredquestions.txt", "a", encoding="utf-8") as aq:
            aq.write("question: ")
            aq.write(str(command.encode("utf-8"))) # str
            aq.write("\n\n")
            aq.write("answer: ")
            aq.write(str(info.encode("utf-8"))) # str
            aq.write("\n")
        with open("answeredquestions.txt", "r", encoding="utf-8") as aq1:
            wo_b1 = aq1.read()
            wo_b = str(wo_b1.replace("b'", ""))
            wo_b = str(wo_b.replace("\\xe2\\x80\\x93", "-"))
            lastchar = len(wo_b1) - 1
            wo_b1 = list(wo_b1)
            wo_b1[lastchar] = ""
            wo_b1 = "".join(wo_b1)
        with open("answeredquestions.txt", "w", encoding="utf-8") as aq2:
            aq2.write(wo_b)
        print(type(wo_b))
        print(info)
        talk(info)
    elif 'what is' in command:
        thing = command.replace('what is', '')
        info = wikipedia.summary(thing, 1)
        with open("answeredquestions.txt", "a", encoding="utf-8") as aq:
            aq.write(str(command.encode("utf-8")))
            aq.write(str(info.encode("utf-8")))
        print(info)
        talk(info)
    elif 'who was' in command:
        person = command.replace('who was', '')
        if "jesus" in person.lower():
            info=wikipedia.summary(person, 2)
        else:
            info = wikipedia.summary(person, 1)
        with open("answeredquestions.txt", "a", encoding="utf-8") as aq:
            aq.write(str(command.encode("utf-8")))
            aq.write(str(info.encode("utf-8")))
        print(info)
        talk(info)
    elif 'what was' in command:
        thing = command.replace('what was', '')
        info = wikipedia.summary(thing, 1)
        with open("answeredquestions.txt", "a", encoding="utf-8") as aq:
            aq.write(str(command.encode("utf-8")))
            aq.write(str(info.encode("utf-8")))
        print(info)
        talk(info)
    elif 'tell me about' in command:
        thing = command.replace('tell me about', '')
        info = wikipedia.summary(thing, 5)
        print(info)
        talk(info)
    elif 'tell me a lot about' in command:
        thing = command.replace('tell me a lot about', '')
        info = wikipedia.summary(thing, 10)
        print(info)
        talk(info)
    elif "tell me some information about" in command:
        talk("Would you like it in sections? Yes or no.")
        sectionsyn = take_command(False)
        if "yes" in sectionsyn.lower():
            def listsections():
                thing = command.replace('tell me some information about', '')
                talk("Sections are:")
                print(wikipedia.page(thing).sections)
                talk(wikipedia.page(thing).sections)
                talk("Which section would you like to read?")
                whichsection = take_command(False)
                if str(whichsection.strip()[0].upper() + whichsection[1:]) in wikipedia.page(thing).sections: # or simply .capitalize()
                    print(whichsection.strip()[0].upper() + whichsection[1:])
                    talk(wikipedia.page(thing).section(whichsection))
                else:
                    talk("I didn't get that statement, or it is not a part of the sections. Please say it again.")
                    listsections()
            listsections()
        else:
            talk('How much?')
            howmuch = take_command(False)
            try:
                print(wikipedia.summary(thing, int(howmuch)))
                talk(wikipedia.summary(thing, int(howmuch)))
            except:
                talk("I didn't hear that well. Please say the command again.")
                run_alexa()
    elif 'tell me a joke' in command:
        talk(pyjokes.get_joke())
    elif command == " good night":
        talk("Good night.")
        quit()
    elif command == " goodbye" or command == " bye" or command == "by" or command == " by":
        talk("bye")
        quit()
    elif 'what did jesus say about' in command:
        topicjesus = command.replace('what did jesus say about ', '')
        for i in range(0, len(fulllist) - 1):
            if topicjesus in fulllist[i]:
                possibleverses[fulllist[i]]=fulllist[i].lower().count(topicjesus.lower())
        allvals = list(possibleverses.values())
        allkeys = list(possibleverses.keys())
        """try:"""
        largestmention = max(allvals)
        print(allkeys[allvals.index(largestmention)])
        talk(allkeys[allvals.index(largestmention)])
        talk("Would you like me to continue?")
        yon=take_command(False)
        if "yes" in yon:
            newcontinue = allkeys[allvals.index(largestmention)]
            num=fulllist.index(newcontinue)
            print(num)
            howmanyverses=0
            for i in range(num, len(fulllist)-1):
                talk(fulllist[i])
                if howmanyverses==6:
                    talk("Would you like to continue? Yes or no.")
                    continueyn = take_command(False)
                    if "yes" in continueyn:
                        howmanyverses=0
                        continue
                    else:
                        talk("Ok.")
                        take_command()
                else:
                    howmanyverses+=1
            """print(allvals.index(largestmention-1))
            print(newcontinue)
            talk(newcontinue)"""
        elif "no" in yon:
            talk("Ok.")
            take_command()
        """except:
            talk("Jesus said nothing about " + topicjesus)"""
    elif 'what did jesus say about being' in command:
        topicjesus = command.replace('what did jesus say about being ', '')
        talk(topicjesus)
    elif "clear my history" in command:
        with open("answeredquestions.txt", "w", encoding="utf-8") as aq2:
            aq2.write("")
        talk("History cleared.")
    else:
        talk("Please say the command again, if I didn't hear well, or try a different one, if I can't respond to it.")
        run_alexa()

######################
##      Output      ##
######################


talk('I\'m Bob. What do you want from me?')

while True:
    run_alexa()
