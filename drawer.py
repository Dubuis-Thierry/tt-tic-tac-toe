import pygame
import math

def draw_cross(screen, center_position, size, color, width):
    decal = int(size*math.cos(math.pi/4))

    c_x, c_y = center_position

    top_left = c_x - decal // 2, c_y - decal // 2

    top_right = c_x + decal // 2, c_y - decal // 2

    bottom_right = c_x + decal // 2, c_y + decal // 2

    bottom_left = c_x - decal // 2, c_y + decal // 2

    pygame.draw.line(screen, color, top_left, bottom_right, width)
    pygame.draw.line(screen, color, top_right, bottom_left, width)
