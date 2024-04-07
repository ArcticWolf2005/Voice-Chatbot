from logging.config import listen
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

#speech engine initialisation
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)#0=male, 1=female
activationWord='Nova'#single word

#Configure browser
#Set the path
chrome_path=r"C:/Program Files/Google/Chrome/Application/chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

def speak(text, rate=150):
    engine.setProperty('rate',rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener=sr.Recognizer()
    print('Listening for a command')

    with sr.Microphone() as source:
        listener.pause_threshold=2
        input_speech=listener.listen(source)

    try:
        print('Recognising speech...')
        query=listener.recognize_google(input_speech, language='en_gb')
        print('The input speech was: '(query))
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'

    return query

def search_wikipedia(query=''):
    searchResults=wikipedia.search(query)
    if not searchResults:
        print('No results found')
        return 'Result not found'
    try:
        wikiPage=wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
            wikiPage=wikipedia.page(error.option[0])
    print(wikiPage.title)
    wikiSummary=str(wikiPage.summary)
    return wikiSummary

if __name__== '__main__':
    speak('All systems nominal.')

    while True:
        #Parse as a list
        query=parseCommand().lower().split()

        if query[0]==activationWord:
            query.pop(0)

            #List commands
            if query[0]=='say':
                if 'hello' in query:
                    speak('Greetings, all.')
                else:
                    query.pop(0)
                    speech=''.join(query)
                    speak(speech)

            #Navigation
            if query[0]=='go'and query[1]=='to':
                speak('Opening....')
                query=' '.join(query[2:])
                webbrowser.get('chrome').open_new_tab(query)

            #Wikipedia
            if query[0]=='find':
                query=' '.join(query[1:])
                speak('Please wait a moment.')
                result=search_wikipedia(query)
                speak(result)

            if query[0]=='exit':
                speak('Goodbye')
                break
