from extractor import DataExtractor
def main():
    admissions_url = (
        "https://www.bucknell.edu/admissions-aid/apply-bucknell"
    )
    extractor = DataExtractor()
    html = extractor.fetch_page(admissions_url)
    text = extractor.extract_text(html)
    print("\nEMAIL:")
    print(extractor.extract_email(text))
    print("\nPHONE:")
    print(extractor.extract_phone(text))
    print("\nDEADLINE:")
    print(extractor.extract_deadline(text))

if __name__ == "__main__":
    main()