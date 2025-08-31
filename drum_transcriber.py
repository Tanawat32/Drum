import argparse
import numpy as np
import librosa
import mido


def classify_hit(y_segment, sr):
    """Classify drum hit as kick or snare based on spectral centroid."""
    centroid = librosa.feature.spectral_centroid(y=y_segment, sr=sr)
    mean_centroid = centroid.mean()
    # Rough heuristic: low centroid -> kick, high -> snare/hat
    return 36 if mean_centroid < 1500 else 38  # MIDI notes: 36 Kick, 38 Snare


def transcribe(audio_path, midi_path):
    y, sr = librosa.load(audio_path, sr=None)
    # Use HPSS to isolate percussive elements
    _, y_perc = librosa.effects.hpss(y)
    onset_times = librosa.onset.onset_detect(y=y_perc, sr=sr, units="time")

    mid = mido.MidiFile(ticks_per_beat=480)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    tempo = mido.bpm2tempo(120)  # default tempo
    last_time = 0.0
    for onset in onset_times:
        # classify hit
        start = max(int((onset - 0.03) * sr), 0)
        end = min(int((onset + 0.03) * sr), len(y_perc))
        segment = y_perc[start:end]
        note = classify_hit(segment, sr)

        delta_time = onset - last_time
        ticks = mido.second2tick(delta_time, mid.ticks_per_beat, tempo)
        track.append(mido.Message("note_on", note=note, velocity=100, time=int(ticks)))
        off_ticks = mido.second2tick(0.1, mid.ticks_per_beat, tempo)
        track.append(mido.Message("note_off", note=note, velocity=0, time=int(off_ticks)))
        last_time = onset + 0.1

    mid.save(midi_path)


def main():
    parser = argparse.ArgumentParser(description="Extract drum hits and create MIDI for MuseScore")
    parser.add_argument("input", help="Path to the input audio file")
    parser.add_argument("output", help="Path to the output MIDI file")
    args = parser.parse_args()
    transcribe(args.input, args.output)


if __name__ == "__main__":
    main()
