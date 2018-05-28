

def text_to_screen(pg, screen, text, x, y, size=9,
                   color=(200, 000, 000),
                   font_type='data/font/8-BIT-WONDER.TTF'):
    try:
        text = str(text)
        font = pg.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
    except Exception as e:
        raise e
