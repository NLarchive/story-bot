# src/main.py
import gradio as gr
from google.colab import userdata  # For Colab environments

# Replace with your actual API key management.
MISTRAL_API_KEY = userdata.get('MISTRAL_API_KEY') # Example for Colab

from src.story_engine import StoryEngine #, interactive_grimoria
from src.utils import introduction, choose_perspective

story_engine = None

def interactive_grimoria(user_action: str, perspective: str):
    """Handles user interaction within the Gradio interface."""
    global story_engine

    return story_engine.interact(user_action)  # Now using the interact method directly



def main_gradio():
    """Runs the main Gradio interface."""
    global story_engine

    story_engine = StoryEngine(MISTRAL_API_KEY)  # Initialize AFTER API key is set.

    perspective_options = ["Guardian", "Matriarch"]

    with gr.Blocks() as demo:
        gr.Markdown("# Interactive Grimoria Chronicles")
        gr.Markdown("Choose your perspective and enter actions to explore the world of Grimoria.")

        with gr.Row():
            perspective = gr.Radio(choices=perspective_options, label="Choose your perspective", value="Guardian")

        user_action = gr.Textbox(label="Enter your action", placeholder="e.g., observe the landscape")
        story_output = gr.Textbox(label="Story Output", interactive=False)
        world_balance = gr.Textbox(label="World Balance", interactive=False)
        guardian_history = gr.Textbox(label="Guardian History", interactive=False)

        user_action.submit(
            interactive_grimoria,
            inputs=[user_action, perspective],
            outputs=[story_output, world_balance, guardian_history]
        )

    demo.launch(debug=True)




if __name__ == "__main__":
    main_gradio()
