#!/usr/bin/env python3
from pickle import dumps, load
from os.path import exists

# TODO make this sqlite
from threading import Thread

def translate(s): return ''.join(i for i in s if i.isalnum() or i in ' ')
# TODO event logger to the changes of the data
# self.dirty could be a string[] of changes and gets appended to a file
import itertools
class Reactions():
    def __init__(self):
        self.triggers = dict() # trigger -> set([emoji])
        self.emojis = dict() # emoji -> set([trigger])
        self.customs = dict()
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
    def getTriggers(self): return set(list(self.triggers.keys())+list(self.customs.keys()))
    def getEmojis(self): return set(list(self.emojis.keys())+list(itertools.chain(*self.customs.values())))
    def getEmojisFromTrigger(self,trigger):
        trigger = translate(trigger.lower())
        return list(self.triggers.get(trigger,[]))+list(self.customs.get(trigger,[]))
    def getTriggersFromEmoji(self,emoji): return list(self.emojis.get(emoji,[]))
    def getEmojisFromTriggersInMessage(self,message):
        message = translate(message.lower()).split()
        for w in message:
            if w in self.customs: yield from self.customs.get(w,[])
            if w in self.triggers: yield from self.triggers.get(w,[])
    def setCustoms(self,customs):
        self.customs = dict()
        for e in customs:
            n = translate(e.name.lower())
            self.customs[e.name] = self.customs.get(e.name,[])
            self.customs[e.name].append(e)
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