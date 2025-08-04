import requests
from typing import List, Dict
import xml.etree.ElementTree as ET

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def fetch_pubmed_ids(query: str, retmax: int = 10) -> List[str]:
    """Use esearch to get a list of PubMed IDs based on the query"""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    response = requests.get(f"{BASE_URL}/esearch.fcgi", params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    """Use efetch to get paper metadata for given PubMed IDs"""
    if not pubmed_ids:
        return []

    ids = ",".join(pubmed_ids)
    params = {
        "db": "pubmed",
        "id": ids,
        "retmode": "xml"
    }
    response = requests.get(f"{BASE_URL}/efetch.fcgi", params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", default="N/A")
        pub_date_elem = article.find(".//PubDate")
        pub_date = "N/A"
        if pub_date_elem is not None:
            year = pub_date_elem.findtext("Year", "")
            month = pub_date_elem.findtext("Month", "")
            day = pub_date_elem.findtext("Day", "")
            pub_date = f"{year}-{month}-{day}"

        authors = []
        for author in article.findall(".//Author"):
            lastname = author.findtext("LastName", default="")
            forename = author.findtext("ForeName", default="")
            fullname = f"{forename} {lastname}".strip()
            affiliation = author.findtext(".//AffiliationInfo/Affiliation", default="")
            authors.append({
                "name": fullname,
                "affiliation": affiliation
            })

        papers.append({
            "title": title,
            "pub_date": pub_date,
            "authors": authors
        })

    return papers
