import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import PyPDF2
from gtts import gTTS
import os
import subprocess
import pywhatkit as kit
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow
import pickle
import random
import json
from tensorflow.python.framework import ops

engine = pyttsx3.init('sapi5')
voices  = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
print(voices)

def speak(audio):
 engine.say(audio)
 engine.runAndWait()
 
 

def wishMe():
    
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
         speak('good morning!')
         speak('hello i am friday and how may i help you sir?')

    elif hour>=12 and hour<18:
         speak('good afternoon')
         speak('hello i am friday and how may i help you sir?')
    else:
         speak('good evening')
         speak('hello i am friday and how may i help you sir?')


if __name__ == "__main__":
    wishMe()

with open("machine learning\intents.json") as file:
    data= json.load(file) 
try:
    x
    with open("data.pickle","rb") as f:
        words,labels,training,output = pickle.load(f)
except:
    words=[]
    labels=[]
    docs_x= []
    docs_y=[]
    for intents in data["intents"]:
        for  pattern in intents["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intents["tag"])

        if intents["tag"] not in labels:
            labels.append(intents["tag"]) 

    words = [stemmer.stem(w.lower())for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels) 

    training =[]
    output =[]
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag =[]
        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)     
        output.append(output_row)   
    training =numpy.array(training) 
    output = numpy.array(output)

    with open("data.pickle","wb") as f:
       pickle.dump(( words,labels,training,output), f)

    ops.reset_default_graph()

    net = tflearn.input_data(shape=[None , len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation ="softmax")
    net =tflearn.regression(net)

    model = tflearn.DNN(net)

    try:
        model.load("model.tflearn")
    except:    
        model.fit(training,output,n_epoch=1000,batch_size=8,show_metric=True)
        model.save("model.tflearn")

def bag_of_words(s , words):
    bag =[0 for _ in range(len(words))]

    s_words =nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):
            if w== se:
                bag[i] = 1
                 
    return numpy.array(bag) 


def chat():
    print("start talking with bot")
    while True:
         def takeCommand():
             r=sr.Recognizer()
             with sr.Microphone() as source:
                 print("listening...")
                 r.pause_threshold = 1
                 audio = r.listen(source)  

             try:
                 print("Recognizing...")
                 query = r.recognize_google(audio,language='en-in')
                 print(f"You said:{query}\n")   
                
             except Exception as e:
                # print(e) 
                print("say that again sir...") 
                return "None"  
             return query
        
         query= takeCommand().lower()
         if query=="ok bye":
            speak("ok have a great time")
            break
         elif 'wikipedia' in query:
             speak("searching the internet...")
             query= query.replace("wikipedia","")
             results = wikipedia.summary(query,sentences=2)
             speak("according to the internet")
             speak(results)
         elif 'open youtube'in query:
                  speak("opening youtube")
                  speak("what should i search for?")
                  channel=takeCommand()
                  url=('https://www.youtube.com/results?search_query= '+ channel)
                  speak('here it is i found for'+ channel )
                  webbrowser.get().open(url) 
         elif 'search' in query:
             speak('what you want to search?')
             search= takeCommand()
             url =('https://google.com//search?q='+ search)
             webbrowser.get().open(url)        
             speak('here it is i found for'+ search )
             
           
         elif  'the time'  in query:
                timet= datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"sir your clock is showing{timet}")
         elif 'read' in query:
              speak( text)
        
         elif query=='stop'or query=='ok bye':
             speak("ok have a nice day sir")
             exit()

         elif "open notepad" in query:
             speak("opening notepad")
             path ="C:\\Windows\\system32\\notepad.exe"
             os.startfile(path)
         elif "close notepad" in query:
             speak("closing notepad")
             os.system(' TASKKILL /F /IM notepad.exe' )      
              
         elif "friday" in query:
             speak("im listening sir")

         elif "open photoshop" in query:
             speak("opening photoshop")
             path ="C:\\Program Files\\Adobe\\Adobe Photoshop CC 2019\\Photoshop.exe"
             os.startfile(path)   
         elif "close photoshop" in query:
             speak("closing photoshop")
             os.system(' TASKKILL /F /IM photoshop.exe') 
         elif "play song" in query:
             speak("what song should i play sir?")
             song = takeCommand().lower()
             kit.playonyt(song)


         results = model.predict([bag_of_words(query,words)])
         results_index = numpy.argmax(results)
         tag = labels[results_index]
         
        
         for tg in data["intents"]:
            if tg['tag'] == tag:
             responses = tg["responses"]

         answer=random.choice(responses)
         print("Friday:"+random.choice(responses))
         speak(answer)    
             
chat()


