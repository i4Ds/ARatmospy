# ;; Developed by Lisa A. Poyneer 2001-2008
# ;; No warranty is expressed or implied.
# ;; --------------------------------------------------------
#
# ;; use this to make phasecube for our simulation!

from typing import List, Optional, cast

import numpy as np
from numpy.typing import NDArray, _ArrayLikeFloat_co

from ._types import FloatLike, NPFloatLike
from .get_phase_streamlined import get_phase_streamlined


def get_x_size(
    xsize0: NPFloatLike,
    max_size: NPFloatLike,
    ok_sizes: NDArray[np.float_],
    dir: str = "X",
) -> np.float_:
    if xsize0 < max_size:
        locs = np.where(xsize0 < ok_sizes)
        cnt = len(locs[0])
        if cnt > 0:
            return ok_sizes[locs[0][0]]
    raise RuntimeError(
        "create_multilayer_phasecube: %s size too big %s" % (dir, xsize0)
    )


def create_multilayer_phasecube(
    n: int,
    m: int,
    pscale: int,
    time: FloatLike,
    paramcube: NDArray[np.float_],
    random: Optional[_ArrayLikeFloat_co] = None,
    sizeflag: Optional[FloatLike] = None,
) -> NDArray[np.float64]:
    bign = n * m
    n_layers = len(paramcube)

    r0s = paramcube[:, 0]
    vels = paramcube[:, 1]
    directions = paramcube[:, 2]

    # figure out how big each screen needs to be
    vels_x = vels * np.cos(directions * np.pi / 180.0)
    vels_y = vels * np.sin(directions * np.pi / 180.0)

    distances_x = vels_x * time
    distances_y = vels_y * time

    pixels_x = distances_x / pscale
    pixels_y = distances_y / pscale

    xsize0 = np.floor(max(np.abs(pixels_x) + bign) + 1) * 1.0
    ysize0 = np.floor(max(np.abs(pixels_y) + bign) + 1) * 1.0

    # these are nice sizes, given FFTW
    powers_of_2 = (
        np.array([64, 128, 256, 512, 1024, 2048, 4096], dtype=np.float64) * 1.0
    )
    an_extra_3 = 3.0 * np.array([32, 64, 128, 256, 512, 1024, 2048], dtype=np.float64)
    two_extra_3s = 9.0 * np.array([16, 32, 64, 128, 256, 512], dtype=np.float64)

    ok_sizes0 = np.concatenate([powers_of_2, an_extra_3, two_extra_3s])
    ok_sizes = np.sort(ok_sizes0)
    max_size = max(ok_sizes)

    xsize = get_x_size(xsize0, max_size, ok_sizes)
    ysize = get_x_size(xsize0, max_size, ok_sizes, dir="Y")

    mysize = cast(float, max([xsize, ysize]))
    required_minimum_size = bign * 4.0
    if mysize < required_minimum_size:
        mysize = required_minimum_size

    if sizeflag is not None:
        mysize = max(mysize, sizeflag)

    print("********** ", xsize0, ysize0, xsize, ysize, mysize, " ************")
    effectiven = int(mysize / m)  # changed from orig-code to not get dtype exception

    # now make the phase screens!

    if random is None:
        random = 104812094812

    phasecube: List[NDArray[np.float64]] = []
    for j in range(n_layers):
        phasecube.append(get_phase_streamlined(effectiven, m, pscale, r0s[j], random))
    # Match expected array format in original IDL code:
    # phasecube = make_array(mysize, mysize, n_layers, double=dflag)
    # for j=0, n_layers-1 do begin
    #    phasecube[*,*,j] = get_phase_streamlined(effectiven, m, $
    #                                             pscale, r0s[j], rflag, double=dflag, nofftw=nofftwflag)
    # endfor

    phasecube_ = np.array(phasecube).transpose()

    return phasecube_


if __name__ == "__main__":
    import astropy.io.fits as pyfits

    n = 10
    m = 100
    pscale = 1
    time = 1
    paramcube = np.array([(0.85, 23.2, 259, 7600), (1.08, 5.7, 320, 16000)])
    random = 13409801
    phasecube = create_multilayer_phasecube(
        n, m, pscale, time, paramcube, random=random
    )

    output = pyfits.HDUList()
    output.append(pyfits.PrimaryHDU(data=phasecube.transpose()))
    output.writeto("phasecube.fits", overwrite=True)
