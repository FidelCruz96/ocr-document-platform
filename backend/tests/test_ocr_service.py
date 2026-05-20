from app.services.ocr_service import extract_text


def test_extract_text_returns_mock_result() -> None:
    result = extract_text(b"file-bytes", "application/pdf")
    assert result == "Mock OCR result: extracted text from uploaded document."
