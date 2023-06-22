from types import TracebackType
from typing import Literal, Optional

import numpy as np

ErrKind = Literal["ignore", "warn", "raise", "call", "print", "log"]


class NumpyHandleError:
    def __init__(
        self,
        all: Optional[ErrKind] = None,
        divide: Optional[ErrKind] = None,
        over: Optional[ErrKind] = None,
        under: Optional[ErrKind] = None,
        invalid: Optional[ErrKind] = None,
    ) -> None:
        self.all = all
        self.divide = divide
        self.over = over
        self.under = under
        self.invalid = invalid

    def __enter__(self) -> None:
        self.old_settings = np.seterr(
            all=self.all,
            divide=self.divide,
            over=self.over,
            under=self.under,
            invalid=self.invalid,
        )

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        np.seterr(**self.old_settings)
