#!/usr/bin/env python3
from pickle import dumps, load
from os.path import exists

from string import punctuation
puncRemover = str.maketrans('','',punctuation)

class Reactions():
    def __init__(self):
        self.triggers = dict() # trigger -> set([emoji])
        self.emojis = dict() # emoji -> set([trigger])
        self.dirty = 0
    def add(self,trigger,emoji):
        self.dirty = 1
        trigger = trigger.lower().translate(puncRemover)
        self.triggers[trigger] = self.triggers.get(trigger,set())
        self.triggers[trigger].add(emoji)
        self.emojis[emoji] = self.emojis.get(emoji,set())
        self.emojis[emoji].add(trigger)
    def removeTrigger(self,trigger):
        self.dirty = 1
        trigger = trigger.lower().translate(puncRemover)
        for emoji in self.triggers.pop(trigger,set()):
            self.emojis.get(emoji,set()).discard(trigger)
    def removeEmoji(self,emoji):
        self.dirty = 1
        for trigger in self.emojis.pop(emoji,set()):
            self.triggers.get(trigger,set()).discard(emoji)
    def removePair(self,trigger,emoji):
        self.dirty = 1
        trigger = trigger.lower().translate(puncRemover)
        self.triggers[trigger] = self.triggers.get(trigger,set())
        self.triggers[trigger].discard(emoji)
        self.emojis[emoji] = self.emojis.get(emoji,set())
        self.emojis[emoji].discard(trigger)
    def getTrigger(self,trigger):
        trigger = trigger.lower().translate(puncRemover)
        return list(self.triggers.get(trigger,[]))
    def getEmoji(self,emoji): return list(self.emojis.get(emoji,[]))
    def getTriggersFromMessage(self,message):
        message = message.lower().translate(puncRemover)
        for w in message.split():
            if w in self.triggers: yield w
    def test(self):
        for t,E in self.triggers.values():
            for e in E: assert t in self.emojis[e]
        for e,T in self.emojis.values():
            for t in T: assert e in self.triggers[t]
    def write(self,f="reactions.data"):
        if self.dirty:
            self.dirty = 0
            with open(f,'wb') as fi: fi.write(dumps(self))
            print("Saved "+f)
    def read(f="reactions.data"):
        if not exists(f):
            print("No Reaction Data")
            return Reactions()
        else:
            print("Reactions Data Loaded")
            with open(f,'rb') as fi: return load(fi)