# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.

"""
Taranis Errors
"""


class TaranisError(Exception):
    """
    Super class for all Taranis errors
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class TaranisNotFoundError(TaranisError):
    """
    When the resource has not been found
    """


class TaranisAlreadyExistsError(TaranisError):
    """
    When the resource already exists
    """


class TaranisNotImplementedError(TaranisError):
    """
    When the action has not been implemented yet
    """
