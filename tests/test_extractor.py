from extractor import DataExtractor
def test_extract_email():
    text = """Contact us at admissions@university.edu"""
    extractor = DataExtractor()
    assert (extractor.extract_email(text)== "admissions@university.edu")
def test_extract_phone():
    text = """Call us at 570-577-3000"""
    extractor = DataExtractor()
    assert (extractor.extract_phone(text)== "570-577-3000")