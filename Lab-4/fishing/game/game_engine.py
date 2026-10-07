"""
GameEngine: owns the hook and the fish, and runs one frame's worth of
game logic.

Starter version: the hook casts and retracts automatically in a
continuous loop - there's no player control over casting yet (that's
Task 3), only one fish type exists (Task 2 adds more), and there's no
round timer (Task 4). Catch detection also has a known bug (see
game/catch.py) that Task 1 asks you to fix.
"""

import pygame
from game.hook import Hook, IDLE
from game.fish import Fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y


class GameEngine:
    def __init__(self):
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.fish_list = [
            Fish(x=100, y=180, fish_type="slow"),
            Fish(x=400, y=280, fish_type="fast"),
            Fish(x=250, y=380, fish_type="slow"),
        ]
        self.hooked_fish = None
        self.score = 0
        self.round_timer = 30  # 30-second round timer
        self.game_over = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and not self.game_over:
            if event.key == pygame.K_SPACE and self.hook.state == IDLE:
                self.hook.start_cast()
        if event.type == pygame.KEYDOWN and self.game_over:
            if event.key == pygame.K_r:
                self.reset_round()

    def update(self):
        if self.game_over:
            return

        if self.hook.state == IDLE:
            pass  # casting is player-controlled, not auto-started

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y
            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish = None
        else:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

        # decrement round timer
        self.round_timer -= 1 / 60  # approximate, based on 60fps
        if self.round_timer <= 0:
            self.round_timer = 0
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Time: {int(self.round_timer)}", (10, 40))
        if self.game_over:
            font_large = pygame.font.SysFont("consolas", 44)
            renderer.draw_banner(surface, font_large, f"Game Over! Final Score: {self.score}")

    def reset_round(self):
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.fish_list = [
            Fish(x=100, y=180, fish_type="slow"),
            Fish(x=400, y=280, fish_type="fast"),
            Fish(x=250, y=380, fish_type="slow"),
        ]
        self.hooked_fish = None
        self.score = 0
        self.round_timer = 30
        self.game_over = False
