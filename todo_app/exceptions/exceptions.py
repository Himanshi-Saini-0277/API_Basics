class AppException(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(AppException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)

class UnauthorizedException(AppException):
    def __init__(self, message="Invalid Credentials"):
        super().__init__(message, 401)

class ConflictException(AppException):
    def __init__(self, message="Resource already exists"):
        super().__init__(message, 409)

class BadRequestException(AppException):
    def __init__(self, message="All fields are required"):
        super().__init__(message, 400)

class DatabaseException(AppException):
    def __init__(self, message="Database error occurred"):
        super().__init__(message, 500)
