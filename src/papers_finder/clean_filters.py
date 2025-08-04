from typing import List, Dict

ACADEMIC_KEYWORDS = [
    "university", "institute", "college", "school", "hospital", "center", "dept", "faculty"
]

COMPANY_KEYWORDS = [
    "inc", "corp", "ltd", "llc", "gmbh", "pharma", "biotech", "therapeutics", "diagnostics"
]

def is_non_academic_affiliation(affiliation: str) -> bool:
    aff_lower = affiliation.lower()
    if any(keyword in aff_lower for keyword in ACADEMIC_KEYWORDS):
        return False
    if any(keyword in aff_lower for keyword in COMPANY_KEYWORDS):
        return True
    return False

def filter_non_academic_authors(authors: List[Dict]) -> List[Dict]:
    return [
        author for author in authors
        if author["affiliation"] and is_non_academic_affiliation(author["affiliation"])
    ]
