

def load_song(pg, song):
    SONG_END = pg.USEREVENT + 1
    pg.mixer.music.set_endevent(SONG_END)
    pg.mixer.music.load(song)
    pg.mixer.music.play()
    return SONG_END
