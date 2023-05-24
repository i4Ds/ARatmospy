# ;; IDL written 19 Nov 2003 by Lisa Poyneer
#
# ;; this is our primary phase screen generator code

import numpy as np
import numpy.random as ra
import scipy.fftpack as sf
from numpy.typing import NDArray, _ArrayLikeFloat_co

from . import generate_grids as gg
from ._types import NPFloatLike


def get_phase_streamlined(
    nsub: int,
    m: int,
    dx: int,
    r0: NPFloatLike,
    rseed: _ArrayLikeFloat_co,
) -> NDArray[np.float64]:
    ra.seed(rseed)
    n = m * nsub
    d = dx * m
    sampfac = 1.0

    screensize_meters = n * dx
    delf = 1.0 / screensize_meters
    # generate_grids, /freqsh, newfx, newfy, n, scale=delf, double=doubleflag
    newfx, newfy = gg.generate_grids(n, scalefac=delf, freqshift=True)

    powerlaw = (
        2
        * np.pi
        / screensize_meters
        * np.sqrt(0.00058)
        * (r0 ** (-5.0 / 6.0))
        * (newfx**2 + newfy**2)
        * (-11.0 / 12.0)
        * n
        * np.sqrt(np.sqrt(2.0))
    )

    powerlaw[0][0] = 0.0

    noise = ra.normal(size=(n, n))

    phaseFT = sf.fft2(noise)

    phaseFT = phaseFT * powerlaw
    powerlaw = 0.0

    phase = np.real(sf.fft2(phaseFT))

    return phase


if __name__ == "__main__":
    pass
#    phase = get_phase_streamlined(
