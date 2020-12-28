def is_in_rect(rect, pos):
    x, y = pos
    rx, ry, width, height = rect
    return x < rx + width and x > rx and y < ry + height and y > ry