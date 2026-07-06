class UploadError(Exception):
    def __init__(self, status_code: int, error_code: str, message: str):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        super().__init__(message)


class MissingFileError(UploadError):
    def __init__(self):
        super().__init__(400, "missing_file", "No file was uploaded.")


class UnsupportedFileTypeError(UploadError):
    def __init__(self):
        super().__init__(415, "unsupported_file_type", "Only PDF files are supported.")


class CorruptPdfError(UploadError):
    def __init__(self):
        super().__init__(422, "corrupt_pdf", "The uploaded file is not a valid PDF.")


class UnexpectedProcessingError(UploadError):
    def __init__(self):
        super().__init__(500, "unexpected_error", "An unexpected error occurred while processing the file.")