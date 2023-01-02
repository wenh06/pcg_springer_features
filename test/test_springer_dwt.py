"""
"""

from pathlib import Path

import numpy as np
import scipy.io.wavfile as siw
from easydict import EasyDict as ED

try:
    from pcg_springer_features.springer_dwt import (
        get_dwt_features,
        get_full_dwt_features,
    )
except ModuleNotFoundError:
    import sys

    sys.path.insert(0, str(Path(__file__).parents[1].resolve()))

    from pcg_springer_features.springer_dwt import (
        get_dwt_features,
        get_full_dwt_features,
    )


def _to_dtype(data: np.ndarray, dtype: np.dtype = np.float32) -> np.ndarray:
    """ """
    if data.dtype == dtype:
        return data
    if data.dtype in (np.int8, np.uint8, np.int16, np.int32, np.int64):
        data = data.astype(dtype) / (np.iinfo(data.dtype).max + 1)
    return data


def test_get_dwt_features():
    """ """
    fs, data = siw.read(Path(__file__).parents[1] / "sample_data" / "13918_AV.wav")
    data = _to_dtype(data, np.float32)
    dwt_features = get_dwt_features(data, fs)
    assert dwt_features.shape == data.shape


def test_get_full_dwt_features():
    """ """
    fs, data = siw.read(Path(__file__).parents[1] / "sample_data" / "13918_AV.wav")
    data = _to_dtype(data, np.float32)

    config = ED(
        wavelet_level=3,
        wavelet_name="db7",
    )
    dwt_features = get_full_dwt_features(data, fs, config)
    assert dwt_features.shape == (config.wavelet_level, data.shape[0])

    config = ED(
        wavelet_level=4,
        wavelet_name="db3",
    )
    dwt_features = get_full_dwt_features(data, fs, config)
    assert dwt_features.shape == (config.wavelet_level, data.shape[0])


if __name__ == "__main__":
    test_get_dwt_features()
    print("test_get_dwt_features passed")
    test_get_full_dwt_features()
    print("test_get_full_dwt_features passed")
