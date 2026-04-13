import pytest
from pathlib import Path
from tabulate import tabulate

from series_intro_recognizer.config import Config
from series_intro_recognizer.processors.audio_files import recognise_from_audio_files_with_offsets


@pytest.mark.skip(reason="test is a manual test")
def test_recognise_from_audio_files() -> None:
    """
    Copy 8 6-minute audio files to assets/audio_files/ directory and run the test.
    :return:
    """
    cfg = Config()
    files = [(f'{__file__}/../audio_files/{i}.wav', None, None) for i in range(1, 8)]
    recognised = list(recognise_from_audio_files_with_offsets(iter(files), cfg))

    rows: list[tuple[str, float, float, float]] = []
    for (file_path, _, _), interval in zip(files, recognised):
        duration = interval.end - interval.start
        rows.append((Path(file_path).name, interval.start, interval.end, duration))

    print()
    print(
        tabulate(
            rows,
            headers=['audio', 'start', 'end', 'duration'],
            floatfmt='.3f',
            tablefmt='github',
        )
    )

    for _, start, end, duration in rows:
        assert start >= 0
        assert end >= 0
        assert duration > 0
        assert 90 - duration <= 1
