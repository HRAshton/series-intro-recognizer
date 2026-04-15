import cupy as cp  # type: ignore

from series_intro_recognizer.config import Config
from series_intro_recognizer.services.offsets_calculator import find_offsets


def test__same_values__not_enough_correlation() -> None:
    cfg = Config()
    corr_values = cp.array([10000, 10000, 10000, 10000, 10000])

    find_offsets_result = find_offsets(corr_values, cfg)

    assert find_offsets_result is None


def test__plateau__correct_offsets() -> None:
    cfg = Config()
    low1 = cp.zeros(cfg.offset_searcher_sequential_intervals * 3)
    high = cp.ones(cfg.offset_searcher_sequential_intervals * 4) * 12
    low2 = cp.zeros(cfg.offset_searcher_sequential_intervals * 4)
    corr_values = cp.concatenate([low1, high, low2], dtype=cp.float32)
    corr_values += cp.random.rand(corr_values.shape[0]) * 0.1

    find_offsets_result = find_offsets(corr_values, cfg)

    assert find_offsets_result == (3 * cfg.offset_searcher_sequential_intervals,
                                   (3 + 4) * cfg.offset_searcher_sequential_intervals)


def test__plateau_with_gaps__correct_offsets() -> None:
    cfg = Config()
    low1 = cp.zeros(cfg.offset_searcher_sequential_intervals * 3)
    high1 = cp.ones(cfg.offset_searcher_sequential_intervals * 4) * 12
    low2 = cp.ones(cfg.offset_searcher_sequential_intervals)  # short gap
    high2 = cp.ones(cfg.offset_searcher_sequential_intervals * 3) * 12
    low3 = cp.zeros(cfg.offset_searcher_sequential_intervals + 1)  # long gap
    high3 = cp.ones(cfg.offset_searcher_sequential_intervals * 4) * 12
    low4 = cp.zeros(cfg.offset_searcher_sequential_intervals * 10)
    corr_values = cp.concatenate([low1, high1, low2, high2, low3, high3, low4], dtype=cp.float32)
    corr_values += cp.random.rand(corr_values.shape[0]) * 0.1

    find_offsets_result = find_offsets(corr_values, cfg)

    assert find_offsets_result == (3 * cfg.offset_searcher_sequential_intervals,
                                   (3 + 4 + 1 + 3) * cfg.offset_searcher_sequential_intervals)


def test__plateau_with_extreme_high_peaks__correct_offsets() -> None:
    cfg = Config()
    low1 = cp.zeros(cfg.offset_searcher_sequential_intervals * 3)
    high = cp.ones(cfg.offset_searcher_sequential_intervals * 4) * 12
    low2 = cp.zeros(cfg.offset_searcher_sequential_intervals * 4)
    corr_values = cp.concatenate([low1, high, low2], dtype=cp.float32)
    corr_values += cp.random.rand(corr_values.shape[0]) * 0.1

    # Add extreme high peaks
    start = int(3.1 * cfg.offset_searcher_sequential_intervals)
    end = int(3.7 * cfg.offset_searcher_sequential_intervals)
    corr_values[start:end] = 10000

    find_offsets_result = find_offsets(corr_values, cfg)

    assert find_offsets_result == (3 * cfg.offset_searcher_sequential_intervals,
                                   (3 + 4) * cfg.offset_searcher_sequential_intervals)


def test__empty_array__returns_none() -> None:
    cfg = Config()
    corr_values = cp.array([], dtype=cp.float32)

    result = find_offsets(corr_values, cfg)

    assert result is None


def test__no_clear_plateau__returns_none() -> None:
    """Linearly-spaced values: mean ≈ median, so _get_threshold returns None."""
    cfg = Config()
    # linspace gives a symmetric distribution where mean(filtered) < median(filtered)*2
    corr_values = cp.linspace(1.0, 2.0, 1000, dtype=cp.float32)

    result = find_offsets(corr_values, cfg)

    assert result is None


def test__plateau_at_start__correct_offsets() -> None:
    """High values at the very beginning of the array (start index = 0)."""
    cfg = Config()
    n = cfg.offset_searcher_sequential_intervals
    high = cp.ones(n * 4, dtype=cp.float32) * 12
    low = cp.zeros(n * 8, dtype=cp.float32)
    corr_values = cp.concatenate([high, low])
    corr_values += cp.random.rand(corr_values.shape[0]) * 0.1

    result = find_offsets(corr_values, cfg)

    assert result == (0, 4 * n)


def test__two_plateaus_second_longer__returns_second() -> None:
    """Two plateaus separated by a gap larger than max_gap; the longer second one wins."""
    cfg = Config()
    n = cfg.offset_searcher_sequential_intervals
    # layout:  [low1 | high1 | gap>n | high2 | low3]
    #  indices: [0,2n) [2n,4n) [4n,6n) [6n,10n) [10n,14n)
    low1  = cp.zeros(n * 2, dtype=cp.float32)
    high1 = cp.ones(n * 2, dtype=cp.float32) * 12   # length 2n
    low2  = cp.zeros(n * 2, dtype=cp.float32)        # gap (2n > n) → splits sequences
    high2 = cp.ones(n * 4, dtype=cp.float32) * 12   # length 4n — strictly longer
    low3  = cp.zeros(n * 4, dtype=cp.float32)
    corr_values = cp.concatenate([low1, high1, low2, high2, low3])
    corr_values += cp.random.rand(corr_values.shape[0]) * 0.1

    result = find_offsets(corr_values, cfg)

    assert result == (6 * n, 10 * n)


def test__plateau_on_edge__correct_offsets() -> None:
    cfg = Config()
    low1 = cp.zeros(cfg.offset_searcher_sequential_intervals * 8)
    high = cp.ones(cfg.offset_searcher_sequential_intervals * 3) * 12
    corr_values = cp.concatenate([low1, high], dtype=cp.float32)
    corr_values += cp.random.rand(corr_values.shape[0]) * 0.1

    find_offsets_result = find_offsets(corr_values, cfg)

    assert find_offsets_result == (8 * cfg.offset_searcher_sequential_intervals,
                                   (8 + 3) * cfg.offset_searcher_sequential_intervals)
