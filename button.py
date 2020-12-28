import pygame
import misc

class Button:
    def __init__(self, screen, text, bg_color, fg_color, callback, font, position):
        self.screen = screen
        self.callback = callback

        self.normal_bg_color = bg_color
        self.normal_fg_color = fg_color
        self.hover_fg_color = (255, 255, 0)
        self.hover_bg_color = bg_color
        self.bg_color = bg_color
        self.fg_color = fg_color

        self.font = font
        self.position = position
        self.padding = 4
        self.normal_padding = 4
        self.hover_padding = 8

        self.text = text
        self.change_text(self.text)

        self.mouse_pressed = False
        self.mouse_is_on = False

    
    def change_text(self, new_text):
        self.img = self.font.render(self.text, True, self.fg_color)
        width, height = self.img.get_size()
        x, y = self.position
        self.x=x-width//2
        self.y=y-height//2
        self.rect = (
            self.x-self.padding,
            self.y-self.padding,
            width+2*self.padding,
            height+2*self.padding
        )

    
    def pygame_update(self):
        if misc.is_in_rect(self.rect, pygame.mouse.get_pos()):
            self.mouse_is_on = True
            self.fg_color = self.hover_fg_color
            self.padding = self.hover_padding
            self.change_text(self.text)
        else:
            self.mouse_is_on = False
            self.fg_color = self.normal_fg_color
            self.padding = self.normal_padding
            self.change_text(self.text)

        if pygame.mouse.get_pressed()[0]:
            if not self.mouse_pressed:
                self.mouse_pressed = True
                if self.mouse_is_on:
                    self.callback()
        else:
            self.mouse_pressed = False
        self.draw()


    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        self.screen.blit(self.img, (self.x, self.y))