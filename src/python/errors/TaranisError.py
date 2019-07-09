# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.

class TaranisError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class TaranisNotFoundError(TaranisError):
    def __init__(self, message):
        super().__init__(message)


class TaranisAlreadyExistsError(TaranisError):
    def __init__(self, message):
        super().__init__(message)


class TaranisNotImplementedError(TaranisError):
    def __init__(self, message):
        super().__init__(message)
