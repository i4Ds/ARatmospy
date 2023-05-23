import numpy as np
from numpy.typing import NDArray
from typing import Tuple

from ._types import NPFloatLike, NPIntLike


def generate_grids(
    n: NPIntLike,
    scalefac: NPFloatLike = 1.0,
    whole: bool = False,
    freqshift: bool = False,
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Returns nxn-element x- and y- index grids
    """
    xgrid = np.zeros((n, n))
    # Check if frequency scale flag is set
    if freqshift:
        for j in np.arange(n):
            xgrid[:, j] = j - (j > n / 2) * n
    else:
        for j in np.arange(n):
            xgrid[:, j] = j
        if n % 2:
            if whole:
                offset = (n - 1) / 2.0
            else:
                offset = 0.0
        else:
            if whole:
                offset = n / 2.0
            else:
                offset = (n - 1) / 2.0
        xgrid = xgrid - offset

    xgrid = xgrid * scalefac
    ygrid = xgrid.transpose()
    return xgrid, ygrid
