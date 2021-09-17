import musicbot

class Queue():
    def __init__(self):
        self.q = []
    
    def enqueue(self, url):
        self.q.append(url)
    
    def dequeue(self):
        url = q.pop(0)
        return url
    
    def isEmpty(self):
        return len(q)==0