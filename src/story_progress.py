# Needs Improvement: The Langgraph implementation has been simplified to just the LLM call for now. 
# You'll need to re-integrate your tool usage logic here once you've clarified how you want the tools to interact with the story flow. 
# The placeholder YourLLM class needs to be replaced with your actual LLM implementation. 
# A basic example is provided, but you'll have to adapt it to your LLM's API.

# src/story_progress.py
from langchain_core.messages import HumanMessage, AIMessage # Import AIMessage
from langgraph.graph import StateGraph, MessagesState
from langgraph.checkpoint import MemorySaver
from typing import Literal
from src.scene import Scene
from src.inventory import Inventory

# Placeholder for your LLM class (replace with your actual implementation)
class YourLLM:  # Replace with your actual LLM class
    def invoke(self, prompt):
        # Replace with your LLM's call method
        return AIMessage(content=f"LLM Response to: {prompt}")

class StoryProgress:
    """Manages the progress of the interactive story using Graph."""

    def __init__(self, model):
        self.current_scene = Scene(
            "World Creation",
            "The light from the sky... (scene description)",
            "The Primordial Chaos"
        )
        self.scenes = {self.current_scene.name: self.current_scene}
        self.completed_tasks = set()
        self.inventory = Inventory()
        self.character_perspective = "Narrator"
        self.checkpointer = MemorySaver()
        self.model = model or YourLLM()  # Use provided model or default
        self.scene_graph = self._create_graph()

    def _create_graph(self):
        workflow = StateGraph(MessagesState)

        def call_model(state):
            messages = state['messages']
            prompt = f"""You are narrating the story of 'The Dark World of Grimoria Chronicles' Chapter 1
            from the perspective of {self.character_perspective}.
            Current Scene: {self.current_scene.name}
            User Action: {messages[-1].content}

            Continue the story from {self.character_perspective}'s point of view:"""
            response = self.model.invoke(prompt)
            return {"messages": messages + [response]}

        def should_continue(state) -> Literal["END"]: # Simplified for now
            return "END" # Always end after LLM call



        workflow.add_node("agent", call_model) # Main LLM node

        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", should_continue)
        return workflow.compile(checkpointer=self.checkpointer)

    def update_scene(self, new_scene_name):

        if new_scene_name in self.scenes:
            self.current_scene = self.scenes[new_scene_name]
        else:
            new_scene = Scene(
                new_scene_name, f"A new area in the story: {new_scene_name}", "Unknown Location"
            )
            self.scenes[new_scene_name] = new_scene
            self.current_scene = new_scene

    def complete_task(self, task):
        self.completed_tasks.add(task)

    def add_to_inventory(self, item):
        self.inventory.add_item(item)

    def set_character_perspective(self, character):
        self.character_perspective = character

    def __str__(self):
        return (
            f"Current Scene: {self.current_scene.name}\n"
            f"Character Perspective: {self.character_perspective}\n"
            f"Completed Tasks: {', '.join(self.completed_tasks)}\n"
            f"Inventory: {self.inventory.list_items()}"
        )
