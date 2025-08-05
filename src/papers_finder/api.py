# src/papers_finder/api.py

import requests
from typing import List, Dict

# PubMed E-utilities base URL
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_pubmed_ids(query: str, retmax: int = 5) -> List[str]:
   
    url = BASE_URL + "esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    ids = data.get("esearchresult", {}).get("idlist", [])
    return ids

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    """
    Fetch detailed paper info for a list of PubMed IDs.
    Returns list of dicts: title, pub_date, authors (name + affiliation).
    """
    if not pubmed_ids:
        return []

    url = BASE_URL + "esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "json"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    result = data.get("result", {})
    papers = []

    for pid in pubmed_ids:
        paper_data = result.get(pid)
        if not paper_data:
            continue

        title = paper_data.get("title", "No title")
        pub_date = paper_data.get("pubdate", "No date")
        authors_list = paper_data.get("authors", [])

        authors = []
        for author in authors_list:
            name = author.get("name", "No name")
            affiliation = author.get("affiliation", "No affiliation")
            authors.append({
                "name": name,
                "affiliation": affiliation
            })

        papers.append({
            "title": title,
            "pub_date": pub_date,
            "authors": authors
        })

    return papers


def extract_corresponding_email(authors: List[Dict]) -> str:
   
 for author in authors:
    if "email" in author and author["email"]:
        return author["email"]
    if "affiliation" in author and "@" in author["affiliation"]:
            # Try to extract email from affiliation string
        parts = author["affiliation"].split()
        for part in parts:
            if "@" in part:
                return part.strip("().,;")
    return "N/A"

