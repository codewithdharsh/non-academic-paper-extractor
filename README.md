 PubMed Research Paper Filter CLI
A command-line Python tool that fetches research papers from PubMed using a search query and filters papers with at least one non-academic author (e.g., authors affiliated with pharmaceutical or biotech companies). The results are output as a CSV file.

✅ Features
🔍 Accepts any valid PubMed search query

🧪 Filters for non-academic affiliations using smart heuristics

📤 Outputs results to a CSV file with:

PubmedID
Title
Publication Date
Non-academic Author(s)
Company Affiliation(s)
Corresponding Author Email

🧵 Fully typed Python with static type hints

🛠️ Structured into reusable module and CLI

🧪 Poetry-based setup with optional CLI entrypoint


🚀 Installation
Clone this repository and install dependencies using Poetry:

git clone https://github.com/codewithdharsh/non-academic-paper-extractor
cd aganitha-pubmed-cli
poetry install
✅ Make sure you are using Python 3.8 or higher.


⚙️ Usage
poetry run get-papers-list "cancer therapy AND 2023"
Optional Flags
-f, --file <filename>: Output CSV file (default: results.csv)

--max-results <number>: Maximum number of papers to fetch (default: 20)

--debug: Enable debug logs

-h, --help: Show CLI usage


Example
poetry run get-papers-list "gene therapy 2023" -f biotech_results.csv --max-results 30 --debug



📂 Project Structure

aganitha-pubmed-cli/
├── src/
│   └── aganitha_papers_cli/
│       ├── __init__.py
│       ├── pubmed.py         # Main logic
│       └── cli.py            # Command-line interface
├── pyproject.toml            # Poetry config
└── README.md


🧪 LLM & Tools Used
BioPython – to access PubMed via Entrez

Poetry – for dependency and packaging

ChatGPT – used for partial generation and review of boilerplate code

All code has been reviewed and validated by the developer.