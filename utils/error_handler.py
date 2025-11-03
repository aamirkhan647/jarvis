"""Centralized error types and helpers."""


class JobTailorError(Exception):
    """Base application error."""


class ParsingError(JobTailorError):
    pass


class ExternalServiceError(JobTailorError):
    pass
