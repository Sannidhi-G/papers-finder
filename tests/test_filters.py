# tests/test_filters.py

from papers_finder.clean_filters import filter_non_academic_authors

def test_filter_non_academic_authors():
    authors = [
        {"name": "John Doe", "affiliation": "University of Oxford"},
        {"name": "Jane Smith", "affiliation": "Pfizer Inc"},
        {"name": "Tom Brown", "affiliation": "Biotech Corp"},
        {"name": "Alice White", "affiliation": ""},
    ]

    filtered = filter_non_academic_authors(authors)
    assert len(filtered) == 2
    assert filtered[0]["name"] == "Jane Smith"
    assert filtered[1]["name"] == "Tom Brown"
