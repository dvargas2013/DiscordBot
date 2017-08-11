#!/usr/bin/env python3
from pickle import dumps, load
from os.path import exists

def translate(s): return ''.join(i for i in s if i.isalnum() or i in ' ')

class Reactions():
    def __init__(self):
        self.triggers = dict() # trigger -> set([emoji])
        self.emojis = dict() # emoji -> set([trigger])
        self.dirty = 0
    def add(self,trigger,emoji):
        trigger = translate(trigger.lower())
        if not trigger: return
        self.dirty = 1
        self.triggers[trigger] = self.triggers.get(trigger,set())
        self.triggers[trigger].add(emoji)
        self.emojis[emoji] = self.emojis.get(emoji,set())
        self.emojis[emoji].add(trigger)
    def removeTrigger(self,trigger):
        trigger = translate(trigger.lower())
        if not trigger: return
        self.dirty = 1
        for emoji in self.triggers.pop(trigger,set()):
            self.emojis.get(emoji,set()).discard(trigger)
    def removeEmoji(self,emoji):
        self.dirty = 1
        for trigger in self.emojis.pop(emoji,set()):
            self.triggers.get(trigger,set()).discard(emoji)
    def removePair(self,trigger,emoji):
        trigger = translate(trigger.lower())
        if not trigger: return
        self.dirty = 1
        self.triggers[trigger] = self.triggers.get(trigger,set())
        self.triggers[trigger].discard(emoji)
        self.emojis[emoji] = self.emojis.get(emoji,set())
        self.emojis[emoji].discard(trigger)
    def getTrigger(self,trigger):
        trigger = translate(trigger.lower())
        return list(self.triggers.get(trigger,[]))
    def getEmoji(self,emoji): return list(self.emojis.get(emoji,[]))
    def getTriggersFromMessage(self,message):
        message = translate(message.lower()).split()
        for w in message:
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