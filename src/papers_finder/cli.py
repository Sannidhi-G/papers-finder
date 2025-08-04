from typer import Typer, Option
from typing import Optional
from papers_finder.api import fetch_pubmed_ids, fetch_paper_details
from papers_finder.clean_filters import filter_non_academic_authors

from papers_finder.csv_writer import write_papers_to_csv

app = Typer(help="Fetch PubMed papers with non-academic authors.")

@app.command()
def main(
    query: str,
    file: Optional[str] = Option(None, "--file", "-f", help="Output CSV filename"),
    debug: bool = Option(False, "--debug", "-d", help="Enable debug output")
):
    if debug:
        print(f"[DEBUG] Query received: {query}")

    print(f"Searching PubMed for: {query}")

    # 1:Fetch PubMed IDs
    ids = fetch_pubmed_ids(query)
    if debug:
        print(f"[DEBUG] Found {len(ids)} paper IDs")

    #  2: Fetch paper details
    papers = fetch_paper_details(ids)
    print(f"Fetched {len(papers)} papers from PubMed.\n")

    # 3: Add filtered authors to each paper
    for paper in papers:
        non_academic = filter_non_academic_authors(paper["authors"])
        paper["non_academic_authors"] = non_academic
        paper["corresponding_email"] = extract_corresponding_email(paper["authors"])

        print(f"📄 {paper['title']}")
        print(f"   Date: {paper['pub_date']}")
        if non_academic:
            print("   🧪 Non-academic Author(s):")
            for author in non_academic:
                print(f"     - {author['name']} ({author['affiliation']})")
        else:
            print("   ⚠️ No non-academic authors found.")
        print()

    # 4: Write to CSV if requested
    if file:
        write_papers_to_csv(papers, file)
        print(f"\n✅ Results saved to {file}")
    
