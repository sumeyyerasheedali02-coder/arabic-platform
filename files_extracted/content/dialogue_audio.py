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
    (2, 1): f"{_BASE_URL}/unit-02-dialogue-01-f8ad4a4a78b6.mp3",
    (2, 2): f"{_BASE_URL}/unit-02-dialogue-02-b8a708e97bc2.mp3",
    (2, 3): f"{_BASE_URL}/unit-02-dialogue-03-f94c819bf1e9.mp3",
    (3, 1): f"{_BASE_URL}/unit-03-dialogue-01-f898fe6de099.mp3",
    (3, 2): f"{_BASE_URL}/unit-03-dialogue-02-a7302eba0add.mp3",
    (3, 3): f"{_BASE_URL}/unit-03-dialogue-03-8cf3883f3616.mp3",
    (4, 1): f"{_BASE_URL}/unit-04-dialogue-01-4c0e5eaa178f.mp3",
    (4, 2): f"{_BASE_URL}/unit-04-dialogue-02-7b4dc8a6506b.mp3",
    (4, 3): f"{_BASE_URL}/unit-04-dialogue-03-5404872ead06.mp3",
    (5, 1): f"{_BASE_URL}/unit-05-dialogue-01-0ab29a3fcf34.mp3",
    (5, 2): f"{_BASE_URL}/unit-05-dialogue-02-477a5a6a0e8f.mp3",
    (5, 3): f"{_BASE_URL}/unit-05-dialogue-03-47608df0bf04.mp3",
    (6, 1): f"{_BASE_URL}/unit-06-dialogue-01-5399565eb1c2.mp3",
    (6, 2): f"{_BASE_URL}/unit-06-dialogue-02-87bc237fc7f2.mp3",
    (6, 3): f"{_BASE_URL}/unit-06-dialogue-03-664af9ecc6ea.mp3",
    (7, 1): f"{_BASE_URL}/unit-07-dialogue-01-c3921fa2a70b.mp3",
    (7, 2): f"{_BASE_URL}/unit-07-dialogue-02-09110da9d6ed.mp3",
    (7, 3): f"{_BASE_URL}/unit-07-dialogue-03-4d1b8844bd1e.mp3",
    (8, 1): f"{_BASE_URL}/unit-08-dialogue-01-62de159eaed9.mp3",
    (8, 2): f"{_BASE_URL}/unit-08-dialogue-02-9c9a709621d1.mp3",
    (8, 3): f"{_BASE_URL}/unit-08-dialogue-03-bc9f0a2105ea.mp3",
    (9, 1): f"{_BASE_URL}/unit-09-dialogue-01-a6d77cf1515a.mp3",
    (9, 2): f"{_BASE_URL}/unit-09-dialogue-02-e1bcc687a204.mp3",
    (9, 3): f"{_BASE_URL}/unit-09-dialogue-03-92251b124dea.mp3",
    (10, 1): f"{_BASE_URL}/unit-10-dialogue-01-f75535b73888.mp3",
    (10, 2): f"{_BASE_URL}/unit-10-dialogue-02-cc5887a7df7d.mp3",
    (10, 3): f"{_BASE_URL}/unit-10-dialogue-03-b08793de4609.mp3",
}

# This source ends at «وهذا عمه حمزة». The owner approved the available part.
PARTIAL_DIALOGUE_AUDIO: set[tuple[int, int]] = {(2, 2)}
