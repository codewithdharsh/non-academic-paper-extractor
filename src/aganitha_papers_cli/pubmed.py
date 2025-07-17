from typing import List, Dict, Optional
from Bio import Entrez
import logging
import csv
import re

# Set your email to use the Entrez API
Entrez.email = "your_email@example.com"

# Keywords to identify academic affiliations
ACADEMIC_KEYWORDS: List[str] = [
    "university", "institute", "college", "school",
    "department", "faculty", "hospital", "centre", "center"
]

def is_academic_affiliation(affiliation: str) -> bool:
    """
    Check if an affiliation is academic based on predefined keywords.
    """
    affil = affiliation.lower()
    return any(keyword in affil for keyword in ACADEMIC_KEYWORDS)

def fetch_pubmed_ids(query: str, max_results: int = 20) -> List[str]:
    """
    Fetch a list of PubMed IDs for a given query.
    """
    logging.debug(f"Searching PubMed for query: {query}")
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record.get("IdList", [])

def extract_email(text: str) -> Optional[str]:
    """
    Extract an email address from a string using regex.
    """
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None

def format_pub_date(date_dict: Dict[str, str]) -> str:
    """
    Convert PubMed date dictionary to a human-readable date string.
    """
    year = date_dict.get("Year", "")
    month = date_dict.get("Month", "")
    day = date_dict.get("Day", "")
    return f"{year}-{month}-{day}".strip("-")

def fetch_paper_details(pmid: str) -> Optional[Dict[str, str]]:
    """
    Fetch details for a single paper and filter for non-academic authors.
    """
    try:
        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="xml")
        records = Entrez.read(handle)
        handle.close()

        article = records["PubmedArticle"][0]
        article_info = article["MedlineCitation"]["Article"]
        pub_date = article_info.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
        title = article_info.get("ArticleTitle", "")
        authors = article_info.get("AuthorList", [])

        non_academic_authors: List[str] = []
        company_affiliations: List[str] = []
        corresponding_email: Optional[str] = None

        for author in authors:
            if "AffiliationInfo" in author:
                for aff in author["AffiliationInfo"]:
                    aff_text = aff.get("Affiliation", "")
                    if not is_academic_affiliation(aff_text):
                        fullname = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()
                        non_academic_authors.append(fullname)
                        company_affiliations.append(aff_text)
                        if "@" in aff_text and not corresponding_email:
                            corresponding_email = extract_email(aff_text)

        if non_academic_authors:
            return {
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": format_pub_date(pub_date),
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email or "N/A"
            }

    except Exception as e:
        logging.warning(f"Error parsing paper {pmid}: {e}")

    return None

def process_query(query: str, max_results: int = 20) -> List[Dict[str, str]]:
    """
    Process a query by fetching PubMed IDs and filtering relevant paper details.
    """
    pmids = fetch_pubmed_ids(query, max_results)
    logging.info(f"Found {len(pmids)} results")

    papers: List[Dict[str, str]] = []
    for pmid in pmids:
        paper = fetch_paper_details(pmid)
        if paper:
            papers.append(paper)

    return papers

def save_to_csv(papers: List[Dict[str, str]], filename: str) -> None:
    """
    Save a list of paper metadata to a CSV file.
    """
    if not papers:
        logging.info("No non-academic papers found.")
        return

    fieldnames = [
        "PubmedID", "Title", "Publication Date",
        "Non-academic Author(s)", "Company Affiliation(s)",
        "Corresponding Author Email"
    ]
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)

    logging.info(f"Saved {len(papers)} papers to {filename}")
