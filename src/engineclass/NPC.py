import pyglet
import json
import random

class NPC:
    def __init__(self, name, image_path, x, y, dialogue_file=None):
        self.name = name
        self.dialogue_chain = []
        self.dialogue_index = 0
        self.active = True
        self.sprite = None

        self.load_animation(image_path, x, y)
        self.load_dialogue(dialogue_file)

    def start_dialog(self, npc):
        if npc.dialogue_chain:
            prompt, options = npc.get_dialogue()
            self.current_dialog_npc = npc
            print(f"Current dialogue npc: {self.current_dialog_npc.name}")
            self.dialog_ui_visible = True
            self.dialog_prompt = pyglet.text.Label(
                prompt,
                x=50, y=100,
                width=1180,
                multiline=True,
                font_size=16,
                color=(255, 255, 255, 255))

            self.dialog_options = []
            for i, option in enumerate(options):
                label = pyglet.text.Label(
                    f"{i+1}. {option['text']}",
                    x=50, y=70 - i * 30,
                    font_size=14,
                    color=(200, 200, 200, 255))
                self.dialog_options.append(label)
        else:
            print("No dialogue available for this NPC.")



    def load_animation(self, image_path, x=0, y=0):
        try:
            image = pyglet.image.load_animation(image_path)
            print(f"Log: Loaded animation: {image_path}")
        except Exception:
            image = pyglet.image.load(image_path)
            print(f"Log: Loaded static image: {image_path}")

        self.sprite = pyglet.sprite.Sprite(image, x=x, y=y)
        self.sprite.scale = 1.0

    def load_dialogue(self, dialogue_file):
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
        formatted_options = []
        for opt in options:
            formatted_options.append({
                "text": opt["text"],
                "response": opt["response"],
                "condition": opt.get("condition", None)  # Expecting string like "has_item_potion"
            })
        self.dialogue_chain.append((prompt, formatted_options))

    def condition_checker(self, condition_key):
        if not condition_key:
            return True
        conditions = {
            "has_item_potion": True,
            "has_item_sword": False,
        }
        return conditions.get(condition_key, False)

    def get_dialogue(self):
        if self.dialogue_index >= len(self.dialogue_chain):
            return None
        prompt, options = self.dialogue_chain[self.dialogue_index]
        available_options = [
            {
                "text": opt["text"],
                "response": f"{self.name}: {opt['response']}"
            }
            for opt in options if self.condition_checker(opt.get("condition"))
        ]
        return f"{self.name}: {prompt}", available_options

    def advance_dialogue(self):
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.dialogue_chain):
            self.active = False

    def draw(self):
        if self.sprite:
            self.sprite.draw()

