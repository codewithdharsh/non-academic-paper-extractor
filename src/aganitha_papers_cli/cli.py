import argparse
import logging
from aganitha_papers_cli.pubmed import process_query, save_to_csv

def main() -> None:
    """
    Command-line interface to fetch papers from PubMed and save to CSV.
    """
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("--max-results", type=int, default=20, help="Maximum number of results to fetch.")
    parser.add_argument("-f", "--file", type=str, default="results.csv", help="Output CSV filename.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    logging.info(f"Running query: {args.query}")
    papers = process_query(args.query, args.max_results)
    save_to_csv(papers, args.file)

if __name__ == "__main__":
    main()
