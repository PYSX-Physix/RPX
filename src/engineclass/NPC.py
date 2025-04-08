import pyglet
import json
import random

class NPC:
    def __init__(self, name, image_path, x, y, dialogue_file=None):
        self.load_animation(image_path, x, y)
        self.name = name
        self.dialogue_chain = []
        self.dialogue_index = 0
        self.active = True
        self.load_dialogue(dialogue_file)

    def load_animation(self, image_path, x: int = 0, y: int = 0):
        """
        Load the image as either a static image or an animation (GIF).
        """
        if image_path:
            try:
                # Try to load the image as an animation (GIF)
                image = pyglet.image.load_animation(image_path)
                print(f"Log: Loaded animation: {image_path}")
            except Exception:
                # If it fails, load it as a static image
                image = pyglet.image.load(image_path)
                print(f"Log: Loaded static image: {image_path}")

            # Create a sprite for the image or animation
            self.sprite = pyglet.sprite.Sprite(image, x=x, y=y)
            self.sprite.scale = 1.0
        else:
            print("Log: No image provided for NPC.")
            self.sprite = None

    def load_dialogue(self, dialogue_file):
        """
        Load dialogue from a JSON file.
        """
        if dialogue_file:
            try:
                with open(dialogue_file, 'r') as f:
                    dialogue_data = json.load(f)
                    for dialogue in dialogue_data:
                        prompt = dialogue["prompt"]
                        options = dialogue["options"]
                        self.add_dialogue(prompt, options)
                    print(f"Log: Loaded {len(dialogue_data)} dialogue sets.")
            except Exception as e:
                print(f"Error loading dialogue: {str(e)}")
        else:
            print("No dialogue file provided.")

    def add_dialogue(self, prompt, options):
        """
        Adds dialogue options to the dialogue chain.
        """
        formatted_options = []
        for opt in options:
            formatted_options.append({
                "text": opt["text"],
                "response": f"{self.name}: {opt['response']}",
                "condition": opt.get("condition", lambda: True)  # Default condition always true
            })
        self.dialogue_chain.append((f"{self.name}: {prompt}", formatted_options))

    def condition_checker(self, condition):
        """
        Simulate checking conditions. This can be expanded for inventory, quest flags, etc.
        """
        conditions = {
            "has_item_potion": True,  # Simulating the player having a potion
            "has_item_sword": False,   # Simulating the player not having a sword
            # Add more conditions based on your game logic
        }
        return conditions.get(condition, False)

    def get_dialogue(self):
        """
        Get the current dialogue and available options based on conditions.
        """
        if self.dialogue_index >= len(self.dialogue_chain):
            return None
        prompt, options = self.dialogue_chain[self.dialogue_index]
        available_options = [opt for opt in options if self.condition_checker(opt["condition"]())]
        return prompt, available_options

    def advance_dialogue(self):
        """
        Move to the next dialogue in the chain.
        """
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.dialogue_chain):
            self.active = False

    def draw(self):
        """
        Draw the NPC sprite.
        """
        if self.sprite:
            self.sprite.draw()

