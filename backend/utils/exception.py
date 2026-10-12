class ApiException(Exception):
    status_code=500
    def __init__(self, message, details=None):
        super().__init__(message)
        self.message = message
        self.details = details

class BadRequestError(ApiException):
    status_code=400

class ValidationError(ApiException):
    status_code=422

class NotFoundError(ApiException):
    status_code=404

class ConflictError(ApiException):
    status_code=409

