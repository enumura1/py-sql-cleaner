class PySqlCleanerError(Exception):
    """Base error for py-sql-cleaner."""


class FormatterError(PySqlCleanerError):
    """Raised when a formatter backend cannot format a SQL block."""
