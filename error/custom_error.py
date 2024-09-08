class APIError(Exception):
    """General Error in API Service"""
    def __init__(self, errCode, errMsg, status_code=None):
        super().__init__(errCode, errMsg)
        self.errCode = errCode
        self.errMsg = errMsg
        self.status_code = status_code if status_code is not None else 500

class BadRequestError(APIError):
    """HTTP status 400 error"""
    def __init__(self, errCode, errMsg='Bad request'):
        super().__init__(errCode=errCode, errMsg=errMsg, status_code=400)

class NotFoundError(APIError):
    """Exception raised when a resource is not found (HTTP 404)."""
    def __init__(self, errCode, errMsg='The resource not found'):
        super().__init__(errCode=errCode, errMsg=errMsg, status_code=404)

class UnauthorizedError(APIError):
    """Exception raised for unauthorized access (HTTP 401)."""
    def __init__(self, errCode, errMsg='Unauthorized'):
        super().__init__(errCode=errCode, errMsg=errMsg, status_code=401)

class AccessDeniedError(APIError):
    """Exception raised for Access denied (HTTP 403)."""
    def __init__(self, errCode, errMsg='Access Denied'):
        super().__init__(errCode=errCode, errMsg=errMsg, status_code=403)