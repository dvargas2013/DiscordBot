#!/usr/bin/env python3
from pickle import dumps, load
from os.path import exists

# TODO make this sqlite
from threading import Thread

def translate(s): return ''.join(i for i in s if i.isalnum() or i in ' ')
# TODO event logger to the changes of the data
# self.dirty could be a string[] of changes and gets appended to a file

class Reactions():
    def __init__(self):
        self.triggers = dict() # trigger -> set([emoji])
        self.emojis = dict() # emoji -> set([trigger])
        self.customs = []
    def add(self,trigger,emoji):
        trigger = translate(trigger.lower())
        if not trigger: return
        self.triggers[trigger] = self.triggers.get(trigger,set())
        self.triggers[trigger].add(emoji)
        self.emojis[emoji] = self.emojis.get(emoji,set())
        self.emojis[emoji].add(trigger)
    def removeTrigger(self,trigger):
        trigger = translate(trigger.lower())
        if not trigger: return
        for emoji in self.triggers.pop(trigger,set()): self.emojis.get(emoji,set()).discard(trigger)
    def removeEmoji(self,emoji):
        for trigger in self.emojis.pop(emoji,set()): self.triggers.get(trigger,set()).discard(emoji)
    def getTriggers(self): return set(list(self.triggers.keys())+[translate(e.name.lower()) for e in self.customs])
    def getEmojis(self): return set(list(self.emojis.keys())+self.customs)
    def getEmojisFromTrigger(self,trigger):
        trigger = translate(trigger.lower())
        return list(self.triggers.get(trigger,[]))+[e for e in self.customs if translate(e.name.lower()) == trigger]
    def getTriggersFromEmoji(self,emoji): return list(self.emojis.get(emoji,[]))+[translate(e.name.lower()) for e in self.customs if e == emoji]
    def getEmojisFromTriggersInMessage(self,message):
        message = set(translate(message.lower()).split())
        for e in self.customs:
            if e.name in message: yield e
        for w in message:
            if w in self.triggers: yield from self.triggers.get(w,[])
    def setCustoms(self,customs): self.customs = customs
    def _write(self,f="reactions.data"):
        with open(f,'wb') as fi: fi.write(dumps(self))
        print("Saved "+f)
    def write(self): Thread(target = self._write).start()
    def read(f="reactions.data"):
        if not exists(f):
            print("No Reaction Data")
            return Reactions()
        else:
            print("Reactions Data Loaded")
            with open(f,'rb') as fi: return load(fi)
    def overwrite(self):
        r = Reactions()
        r.triggers = self.triggers
        r.emojis = self.emojis
        r.write()