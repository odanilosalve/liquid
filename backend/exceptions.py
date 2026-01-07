class ValidationError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class DatabaseError(Exception):
    pass


class ExternalAPIError(Exception):
    pass


class ConfigurationError(Exception):
    pass


class RequestParsingError(Exception):
    pass

