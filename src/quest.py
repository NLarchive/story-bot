# src/quest.py
from typing import List

class Quest:
    """Represents a quest in the story."""

    def __init__(self, name: str, description: str, location=None):
        self.name = name
        self.description = description
        self.location = location
        self.completed = False

    def complete(self):
        self.completed = True

class QuestSystem:
    """Manages quests in the story."""

    def __init__(self):
        self.quests = {}

    def add_quest(self, quest):
        self.quests[quest.name] = quest

    def complete_quest(self, quest_name):
        if quest_name in self.quests:
            self.quests[quest_name].complete()

    def get_active_quests(self):
        return [quest for quest in self.quests.values() if not quest.completed]
