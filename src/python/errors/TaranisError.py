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
