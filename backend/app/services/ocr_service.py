def extract_text(file_bytes: bytes, content_type: str) -> str:
    if not file_bytes:
        raise ValueError("Uploaded file is empty")
    return "Mock OCR result: extracted text from uploaded document."
