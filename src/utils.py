# src/utils.py
from typing import List, Dict
from langchain.tools import tool

class VectorStore:  # Mock vector store - REPLACE THIS with your actual implementation
    def similarity_search(self, query: str) -> List[Dict[str, str]]:
        # Placeholder - Replace with your actual vector store logic
        return [{"page_content": f"Information about '{query}' in Grimoria (Mock Result)"}]

vectorstore = VectorStore()

@tool
def search_grimoria(query: str, location: str = "Grimoria", perspective: str = "Guardian") -> str:
    """Searches for information in Grimoria."""
    docs = vectorstore.similarity_search(query)
    if docs:
        return docs[0]["page_content"]
    else:
        return f"I couldn't find any information about '{query}' in {location} from the {perspective} perspective."

tools = [search_grimoria]

def choose_perspective() -> str:
    """Lets the user choose a perspective."""
    perspectives = ["Guardian", "Matriarch", "Curious Guardian", "Observer"]
    print("Choose your perspective:")
    for i, persp in enumerate(perspectives, 1):
        print(f"{i}. {persp}")

    while True:
        choice = input("Enter the number of your chosen perspective: ")
        if choice.isdigit() and 1 <= int(choice) <= len(perspectives):
            return perspectives[int(choice) - 1]
        print("Invalid choice. Please enter a number from the list.")

def introduction() -> str:
    """Provides an introduction to the game."""
    return """
    Welcome to the interactive 'Grimoria Chronicles' Chapter I experience!
    You find yourself in... (your introduction text)
    """

def display_help():
    """Displays help information."""
    print("""
    Available commands:
    - observe: Describe the current scene
    - communicate with [being]: Interact with other beings
    - ... (rest of your help text)
    """)
