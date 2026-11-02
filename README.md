# Follow-the-rhythm
# Follow the Rhythm 🎵

## About the Game

**Follow the Rhythm** is a rhythm game made using Python, Pygame, and NumPy. The goal is to hit the correct notes at the correct time as they fall down the screen.

The game includes multiple songs, different difficulties, generated musical sounds, scoring, and timing feedback.

You can also create your own songs by editing the song data in the Python code!

---

## How to Play

### 1. Starting the Game

- Click the **Start** button on the main screen.
- You will be taken to the level selection screen.

### 2. Selecting a Song

- Use the left and right arrows to switch between songs.
- Each song has its own high score and last score.
- Click **Start** to begin playing the selected song.
- Use the back arrow to return to the previous screen.

### 3. Playing

There are four colored lanes, each representing a different musical note.

| Lane | Keyboard Key | Color |
|---|---|---|
| 1 | 1 | Red |
| 2 | 2 | Green |
| 3 | 3 | Yellow |
| 4 | 4 | Blue |

As notes fall down the screen, press the matching number key when the note reaches the bottom target.

You can also click the colored circles at the bottom of the screen.

**Timing matters!** Try to hit each note as close to the target line as possible.

### 4. Understanding Your Results

After finishing a song, you will see your score and statistics.

- **Perfect:** You hit the note very close to the target.
- **Early:** You hit the note before it reached the target.
- **Late:** You hit the note after it passed the target.
- **Miss:** You hit too far away from the target or didn't hit the note.

You can also see your high score and last score.

Click the check box to return to song selection.

---

## How Scoring Works

Your score changes depending on your timing.

| Result | Points |
|---|---:|
| Perfect | +2 |
| Early | +1 |
| Late | +1 |
| Miss | -1 |

A note counts as:

- **Perfect:** Within 50 pixels of the target.
- **Early or Late:** Within 125 pixels of the target, but outside the perfect range.
- **Miss:** Outside the early/late range but within 300 pixels.
- **Automatic miss:** If a note passes the screen without being hit.

The game also tracks how many perfect, early, late, and missed notes you get.

---

## How the Game Works

The game is built using three main Python libraries.

### Pygame

Pygame handles:
- Displaying the game window.
- Drawing the notes and lanes.
- Loading images and backgrounds.
- Detecting mouse and keyboard inputs.
- Playing generated sounds.
- Managing the game loop.

### NumPy

NumPy is used to generate the audio waveforms for each musical note.

### Asyncio

Asyncio allows the game loop to run asynchronously. This is especially useful when running the game in a browser using Pygbag.

### Falling Notes

Each note has:
1. A lane number.
2. A beat position.
3. A musical note number.

The game calculates the vertical position of each note using:

`y = -note_spacing * beat_position + time`

As time increases, the notes move down the screen.

When a note reaches the target area, its sound plays. The player must press the corresponding lane at the right time.

### Sound Generation

The game doesn't need a separate audio file for every note!

Instead, it generates sounds using sine waves.

Each musical note has a frequency measured in Hertz (Hz).

The code converts a musical note number into a frequency and uses NumPy to create a sine wave. Pygame then turns that waveform into a playable sound.

This means you can create new melodies without needing to download or record audio files.

---

# Making Your Own Songs 🎼

One of the most important parts of the game is the `songs_notes` list.

This is where all the songs are stored.

Each song contains three matching lists:

```python
songs_notes = [
    [
        [1, 2, 3, 4],  # Lanes
        [1, 2, 3, 4],  # Beat positions
        [1, 

For Test Run
```python -m pytest test_main.py```


![Follow the Rhythm gameplay](StartScreen)

