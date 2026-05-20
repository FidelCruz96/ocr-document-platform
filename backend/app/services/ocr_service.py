from abc import ABC, abstractmethod


class OCRProvider(ABC):
    @abstractmethod
    def extract_text(self, file_bytes: bytes, content_type: str) -> str:
        raise NotImplementedError


class MockOCRProvider(OCRProvider):
    def extract_text(self, file_bytes: bytes, content_type: str) -> str:
        if not file_bytes:
            raise ValueError("Uploaded file is empty")
        return "Mock OCR result: extracted text from uploaded document."


def get_ocr_provider() -> OCRProvider:
    return MockOCRProvider()


def extract_text(file_bytes: bytes, content_type: str) -> str:
    return get_ocr_provider().extract_text(file_bytes, content_type)
