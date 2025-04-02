import pyglet

class GameOverScene:
    def __init__(self, window):
        self.window = window
        self.message = "Game Over! Press R to Restart or Q to Quit."
    
    def draw(self):
        self.window.clear()
        self.window.draw_text(self.message, x=100, y=100, color=(255, 0, 0, 255), font_size=24)
    
    def update(self, dt):
        pass
    
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.R:
            self.restart_game()
        elif symbol == pyglet.window.key.Q:
            self.quit_game()
    
    def restart_game(self):
        # Logic to restart the game
        pass
    
    def quit_game(self):
        self.window.close()