def left(i, width, height):
    if i % width != 0:
        # Not in col 1
        return i-1

def right(i, width, height):
    if (i+1) % width != 0:
        # Not in last col
        return i+1

def above(i, width, height):
    if i-width >= 0:
        # not top row
        return i-width

def below(i, width, height):
    if i+width < width*height:
        # not bottom row
        return i+width

def top_left(i, width, height):
    top = above(i, width, height)
    if top is not None:
        return left(top, width, height)

def top_right(i, width, height):
    top = above(i, width, height)
    if top is not None:
        return right(top, width, height)

def bottom_left(i, width, height):
    bottom = below(i, width, height)
    if bottom is not None:
        return left(bottom, width, height)

def bottom_right(i, width, height):
    bottom = below(i, width, height)
    if bottom is not None:
        return right(bottom, width, height)

