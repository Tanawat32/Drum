# Drum

A simple script to extract drum hits from an audio file and create a MIDI file that can be opened in MuseScore for viewing as sheet music.

## Requirements

Install dependencies:

```bash
pip install librosa mido numpy
```

## Usage

```bash
python drum_transcriber.py input_song.wav output.mid
```

Open `output.mid` in [MuseScore](https://musescore.org) to view the transcribed drum hits.
