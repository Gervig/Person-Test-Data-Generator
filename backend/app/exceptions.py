class DatabaseError(Exception):
    """Raised when the database driver cannot complete an operation."""


class PostalCodeUnavailableError(Exception):
    """Raised when no postal codes are available."""
