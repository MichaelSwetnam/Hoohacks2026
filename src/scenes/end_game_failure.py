from scene import Scene
from pygame import draw
from pygame import Vector2

class EndGame(Scene):
    def draw(self, scene, events):
        draw.circle(scene, "green", Vector2(100, 100), 50)
    
    def next_scene(self):
        return None