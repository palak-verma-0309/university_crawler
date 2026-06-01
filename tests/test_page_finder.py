from page_finder import PageFinder
def test_find_admissions_page():
    urls = [
        "https://abc.edu/about",
        "https://abc.edu/admissions",
        "https://abc.edu/contact"
    ]
    finder = PageFinder()
    result = finder.find_admissions_page(urls)
    assert result == "https://abc.edu/admissions"
def test_find_tuition_page():
    urls = [
        "https://abc.edu/about",
        "https://abc.edu/tuition-fees",
        "https://abc.edu/contact"
    ]
    finder = PageFinder()
    result = finder.find_tuition_page(urls)
    assert result == "https://abc.edu/tuition-fees"