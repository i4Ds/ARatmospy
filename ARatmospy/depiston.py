import numpy as np
from numpy.typing import NDArray

from ._types import NPArrayFloatBoolLike


def depiston(
    phase: NDArray[np.float_],
    aperture: NPArrayFloatBoolLike = np.zeros(1),
) -> NDArray[np.float_]:
    """
    ;  depiston - remove piston over an aperture
    ;
    ;  USAGE:
    ;    phdp = depiston(ph,ap)
    ;
    ;  INPUTS:
    ;    ph - 2D numpy array of phase [n,m]
    ;    ap - numpy array defining aperture[n,m] - optional
    ;
    ;  OUTPUTS:
    ;    phdp - phase with piston removed
    """

    if len(aperture) == 1:
        aperture = np.ones(phase.shape)

    piston = np.sum(phase * aperture) / aperture.sum()
    phdp = aperture * (phase - piston)

    return phdp
