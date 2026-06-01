# University ETL Pipeline

## Overview

This project implements a simple ETL (Extract, Transform, Load) pipeline that automatically discovers and extracts university admissions and tuition-related information starting from a university domain.

The pipeline crawls the university website, identifies relevant Admissions and Tuition/Cost pages, extracts structured information, validates the extracted data using Pydantic schemas, and outputs normalized JSON data.

The solution is designed to work without hardcoded destination URLs and follows the requirements specified in the assignment.

---

## Features

* Automatic website crawling with configurable crawl depth
* Automatic discovery of Admissions pages
* Automatic discovery of Tuition/Cost pages
* Contact information extraction (email and phone)
* Admission deadline extraction
* Tuition extraction
* University overview extraction
* Pydantic-based schema validation
* Optional metadata collection for source pages
* LLM-assisted location extraction using Gemini
* Retry mechanism for failed requests
* Structured logging and execution summaries
* Data quality checks
* Support for processing multiple university domains in a single run
* Basic automated tests for key components

---

## Project Structure

```text
.
├── crawler.py
├── page_finder.py
├── extractor.py
├── llm_extractor.py
├── schemas.py
├── main.py
├── requirements.txt
├── tests/
│   ├── test_page_finder.py
│   └── test_extractor.py
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd university_etl
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Running the Pipeline

### Single University

```bash
python main.py https://www.bucknell.edu
```

### Multiple Universities

```bash
python main.py https://www.bucknell.edu https://www.salisbury.edu https://www.udc.edu
```

---

## Overall Approach

### 1. Crawl

The crawler performs a breadth-first search (BFS) traversal of the university website.

Key characteristics:

* Maximum crawl depth of 2
* Same-domain URLs only
* PDF links ignored
* Retry logic for failed requests

### 2. Page Discovery

All discovered URLs are scored using keyword-based heuristics.

Admissions keywords:

```text
admission
admissions
apply
```

Tuition keywords:

```text
tuition
fees
cost
financial-aid
```

The highest-scoring URLs are selected as the Admissions and Tuition pages.

### 3. Data Extraction

Information is extracted from the selected pages using rule-based extraction:

* University name
* Email address
* Phone number
* Admission deadline
* Tuition information
* Page metadata

### 4. LLM-Assisted Enrichment

Google Gemini is used as an optional enrichment layer to extract university location information when available.

The extraction process remains functional even if the LLM is unavailable.

### 5. Validation

All extracted data is validated against the provided Pydantic schema before being returned.

---

## Key Design Decisions

### BFS Crawling

Breadth-first search was chosen because important admissions and tuition pages are usually located close to the homepage.

### Heuristic Page Discovery

A lightweight keyword scoring system was selected instead of a fully LLM-based approach because it is:

* Faster
* Deterministic
* Easier to debug
* Less expensive

### Hybrid Extraction

Rule-based extraction is used as the primary extraction mechanism.

LLM-based extraction is used only for enrichment tasks to improve reliability and reduce dependence on external AI services.

### Graceful Failure Handling

The pipeline continues processing even if:

* Some pages fail to load
* LLM requests fail
* Certain fields cannot be extracted

Missing values are returned as `null`.

---

## Data Quality Checks

The pipeline performs several quality checks:

* Missing overview detection
* Missing university name detection
* Missing admission deadline detection
* Missing tuition information detection
* Suspicious tuition value detection

Quality issues are reported during execution but do not stop processing.

---

## Logging

Structured logging is used throughout the pipeline.

Execution summaries include:

* Number of URLs crawled
* Selected Admissions page
* Selected Tuition page
* University name
* Data quality issues

---

## Automated Tests

Basic automated tests are included for:

* Admissions page discovery
* Tuition page discovery
* Email extraction
* Phone extraction

Run tests using:

```bash
pytest
```

---

## Assumptions

* Important admissions and tuition pages are reachable within two levels from the homepage.
* Tuition information appears in textual content accessible through standard HTML.
* Contact information is publicly available on admissions-related pages.
* Websites do not require authentication to access the relevant pages.

---

## Limitations

* JavaScript-heavy websites may not be fully supported.
* Tuition extraction currently relies on rule-based patterns and may not always identify the most accurate tuition value.
* Multiple admission deadlines are not fully categorized into admission types.
* Location extraction depends on LLM availability.
* Dynamic content loaded after page rendering may not be captured.
* Some universities may use unconventional page structures that reduce extraction accuracy.

---

## AI / LLM Usage

Google Gemini is used as an optional enrichment component.

Current use cases:

* University location extraction
* Structured information enrichment

The pipeline does not depend entirely on the LLM and continues functioning if the LLM service is unavailable.

---

## Sample Universities Tested

* Bucknell University
* Salisbury University
* University of the District of Columbia (UDC)

The pipeline successfully discovers Admissions and Tuition/Cost pages for these universities and generates structured output conforming to the provided schema.

---

## Future Improvements

* Improved tuition extraction accuracy
* Deadline classification by admission type
* Better duplicate detection
* Confidence scoring for extracted fields
* Additional data quality validations
* Support for JavaScript-rendered websites
* Parallel crawling for improved performance
