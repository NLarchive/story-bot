# src/scene.py
class Scene:
    """Represents a scene in the story."""

    def __init__(self, name: str, description: str, location: str):
        self.name = name
        self.description = description
        self.location = location
        self.characters = []
        self.objects = []

    def add_character(self, character):
        self.characters.append(character)

    def add_object(self, object_name):
        self.objects.append(object_name)

    def describe(self) -> str:
        scene_description = f"Scene: {self.name}\nDescription: {self.description}\nLocation: {self.location}\n\n"
        if self.characters:
            scene_description += "Characters in the scene:\n"
            scene_description += "\n".join(f" - {character.name}" for character in self.characters)
        else:
            scene_description += "No characters are in the scene.\n"

        if self.objects:
            scene_description += "\n\nObjects in the scene:\n"
            scene_description += "\n".join(f" - {obj}" for obj in self.objects)
        else:
            scene_description += "\nNo objects are in the scene.\n"
        return scene_description
