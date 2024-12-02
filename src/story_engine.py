# Needs prompt customization and LLM confirmation. 
# Make sure to replace the placeholder prompt with your actual prompt design, and ensure that your MistralLLM class 
# (or whichever LLM you are using) is correctly implemented and imported. 
# The logic now assumes the user_action is also used as the query for the retrieval step. You can refine this as needed.


# src/story_engine.py
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from typing import List, Dict, Any
import os

from src.story_progress import StoryProgress
from src.quest import Quest, QuestSystem
# Assuming your MistralLLM class is here (adjust if needed).
from src.mistral_llm import MistralLLM  # Make sure this path is correct

# Constants
FILE_PATH = '/content/drive/MyDrive/AI/PROJECT_G/dark_grimoria.md'  # Replace with your file path
EMBEDDINGS_PATH = '/content/drive/MyDrive/AI/PROJECT_G/grimoria_embed.faiss' # Replace with your embeddings path

def load_or_create_embeddings():
    """Loads existing embeddings or creates new ones."""
    embeddings = HuggingFaceEmbeddings()
    if os.path.exists(EMBEDDINGS_PATH):
        print("Loading existing embeddings...")
        return FAISS.load_local(EMBEDDINGS_PATH, embeddings, allow_dangerous_deserialization=True)

    print("Creating new embeddings...")
    from langchain_community.document_loaders import UnstructuredMarkdownLoader # Move import here
    loader = UnstructuredMarkdownLoader(FILE_PATH)
    documents = loader.load()
    from langchain.text_splitter import CharacterTextSplitter # Move import here
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(EMBEDDINGS_PATH)
    print(f"Embeddings saved to {EMBEDDINGS_PATH}")
    return vectorstore

class StoryEngine:
    """Manages the overall story progression and user interaction."""

    def __init__(self, api_key: str):

        self.model = MistralLLM(api_key=api_key)  # Instantiate MistralLLM
        self.story = StoryProgress(self.model)
        self.story_chain = self._setup_retrieval_qa(api_key)
        self.story_history = []
        self.quest_system = QuestSystem()
        self.perspective = "Guardian"
        self.world_balance = 100

    def add_quest(self, name: str, description: str):
        quest = Quest(name, description)
        self.quest_system.add_quest(quest)

    def complete_quest(self, quest_name: str):
        self.quest_system.complete_quest(quest_name)

    def get_active_quests(self) -> List[str]:
        return [quest.name for quest in self.quest_system.get_active_quests()]

    def _setup_retrieval_qa(self, api_key: str):
        """Sets up the RetrievalQA chain."""

        vectorstore = load_or_create_embeddings()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        mistral_llm = MistralLLM(api_key=api_key) # Make sure this is your actual LLM
        # Placeholder prompt - REPLACE THIS with your actual prompt.
        prompt_template = """You are narrating the story of 'The Dark World of Grimoria Chronicles' Chapter 1 from the perspective of a {perspective}.
        Use the following context to continue the interactive story, incorporating the user's actions and the current scene.

        Context:
        {context}

        The Guardians are... (Guardian description)

        Current Scene: {current_scene}
        Perspective: {perspective}
        User Action: {user_action}

        Query: {query}

        Continue the story... (Instructions for continuation)
        """
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=[
                "context", "perspective", "current_scene", "user_action", "query"
            ]
        )
        return RetrievalQA.from_chain_type(
            llm=mistral_llm,
            chain_type="map_reduce",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

    def set_perspective(self, perspective: str):
        if perspective in ["Guardian", "Matriarch"]:
            self.perspective = perspective
            self.story.set_character_perspective(perspective)
        else:
            raise ValueError("Invalid perspective. Choose either 'Guardian' or 'Matriarch'.")

    def interact(self, user_action: str) -> Dict[str, Any]:
        """Handles user interaction and generates story continuation."""
        user_action = user_action.lower().strip()

        if user_action == "inventory":
            inventory_items = self.story.inventory.list_items()
            return {
               "story_output": f"You have: {inventory_items}" if inventory_items != "Empty" else "Your inventory is empty.", 
               "world_balance": self._get_world_balance_description(), 
               "guardian_history": "\n".join(self.story_history[-10:]) 
           }



        context = {
            "context": self.story.current_scene.description, # Use scene description here
            "current_scene": self.story.current_scene.name,
            "perspective": self.perspective,
            "user_action": user_action,
            "query": user_action  # Use user_action as query for now
        }

        result = self.story_chain.invoke(context) # Correct invoke call

        story_continuation = result['result']
        self.story_history.append(f"User: {user_action}")
        self.story_history.append(f"Story: {story_continuation}")

        self._update_world_balance(user_action, story_continuation)

        return {
            "story_output": story_continuation,
            "world_balance": self._get_world_balance_description(),
            "guardian_history": "\n".join(self.story_history[-10:])
        }

    def _update_world_balance(self, user_action: str, story_continuation: str):
        if "destroy" in user_action or "kill" in user_action:
            self.world_balance -= 5
        elif "protect" in user_action or "nurture" in user_action:
            self.world_balance += 5
        self.world_balance = max(0, min(100, self.world_balance)) # Ensure it stays within bounds

    def _get_world_balance_description(self) -> str:
        if self.world_balance > 80:
            return "The world is in perfect harmony."
        elif self.world_balance > 60:
            return "The balance is stable, but slight disturbances can be felt."
        elif self.world_balance > 40:
            return "The world's balance is wavering, caution is needed."
        elif self.world_balance > 20:
            return "The balance is severely threatened, immediate action is required."
        else:
            return "The world is on the brink of chaos, the balance must be restored!"
