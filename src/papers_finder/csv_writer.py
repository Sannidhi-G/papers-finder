import csv
from typing import List, Dict

def write_papers_to_csv(papers: List[Dict], filename: str) -> None:
    """Writes filtered paper data to a CSV file."""

    headers = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email"
    ]

    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for paper in papers:
            non_academic_authors = paper.get("non_academic_authors", [])
            author_names = [a["name"] for a in non_academic_authors]
            affiliations = [a["affiliation"] for a in non_academic_authors]

            writer.writerow({
                "PubmedID": paper.get("id", "N/A"),
                "Title": paper.get("title", "N/A"),
                "Publication Date": paper.get("pub_date", "N/A"),
                "Non-academic Author(s)": ", ".join(author_names),
                "Company Affiliation(s)": ", ".join(affiliations),
                "Corresponding Author Email": paper.get("corresponding_email", "N/A")  # placeholder
            })
