import lookup

print("TimBot active!")

def timResponse(message, llm_client, sender):
    message = message.lstrip().lower()
    print("Received phrase: ", message)

    # First, I will check for basic responses to standard questions/greetings.
    # "hello", "hey", "yo", "hi", etc.
    greetings = ['hello', 'yo', 'hi', 'hey', 'greetings', 'sup']
    query = ['who are you?', 'who are you', 'what can i ask?', 'what can i ask', 'you dumb', 'what do you know?', 'what do you know']
    for word in message.split():
        if word in greetings:
            res = "Hello! Hope you are well."
            return res
    
    if message in query:
        res = "I am TimBot; a Discord bot developed by your boy <@_yaboitim>. I am still in beta though, so my responses may not be always accurate. \nBut I do have an IQ of -1/12."
        return res

    res = lookup.getAnswers(message, llm_client) 

    return res