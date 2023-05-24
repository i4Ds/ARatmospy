from typing import Union

import numpy as np
from numpy.typing import NDArray

IntLike = Union[bool, int]
FloatLike = Union[int, float]
FloatBoolLike = Union[FloatLike, bool]
ComplexLike = Union[FloatLike, complex]

NPIntLike = Union[IntLike, np.int_, np.bool_]
NPFloatLike = Union[FloatLike, np.int_, np.float_]
NPComplexLike = Union[ComplexLike, NPFloatLike, np.complex_]

NDArrayIntLike = Union[NDArray[np.bool_], NDArray[np.int_]]
NDArrayFloatLike = Union[NDArray[np.int_], NDArray[np.float_]]
NPArrayFloatBoolLike = Union[NDArrayFloatLike, NDArray[np.bool_]]
NDArrayComplexLike = Union[NDArrayFloatLike, NDArray[np.complex_]]
