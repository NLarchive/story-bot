# src/character.py
from src.inventory import Inventory

class Character:
    """Represents a character in the story."""

    def __init__(self, name: str, description: str, location=None):
        self.name = name
        self.description = description
        self.inventory = Inventory()
        self.location = location

    def move_to(self, scene):
        if self.location:
            try:
                self.location.characters.remove(self)
            except ValueError:
                pass  # Character wasn't in the scene's list
        self.location = scene
        scene.add_character(self)

    def describe(self) -> str:
        character_description = f"Character: {self.name}\nDescription: {self.description}\n\n"
        character_description += f"Inventory:\n{self.inventory.list_items()}\n" if self.inventory.items else "Inventory: Empty\n"
        character_description += f"\nCurrent Location: {self.location.name}\n" if self.location else ""
        return character_description
