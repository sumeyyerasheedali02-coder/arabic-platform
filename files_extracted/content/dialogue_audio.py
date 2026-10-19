"""Published dialogue recordings, keyed by course unit and dialogue numbers.

Keep media in object storage, not the database or this repository. Only add a
recording here after uploading and checking it against the corresponding text.
The keys are content numbers; database row IDs can differ between installations.
"""

_BASE_URL = "https://qyr8ctlxytrsnmot.public.blob.vercel-storage.com"

DIALOGUE_AUDIO: dict[tuple[int, int], str] = {
    (1, 1): f"{_BASE_URL}/unit-01-dialogue-01-1256cef1857a.mp3",
    (1, 2): f"{_BASE_URL}/unit-01-dialogue-02-68d347cdffed.mp3",
    (1, 3): f"{_BASE_URL}/unit-01-dialogue-03-f6ef89dc87bf.mp3",
    (1, 4): f"{_BASE_URL}/unit-01-dialogue-04-4d83343981ff.mp3",
    (1, 5): f"{_BASE_URL}/unit-01-dialogue-05-40c08ef2bb05.mp3",
    (1, 6): f"{_BASE_URL}/unit-01-dialogue-06-4467a6046b12.mp3",
}
