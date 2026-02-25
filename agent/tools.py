import requests
from langchain.tools import tool

@tool
def search_pubmed(query: str) -> str:
    """Search PubMed for medical research articles related to a query."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 3,
        "retmode": "json"
    }
    response = requests.get(url, params=params).json()
    ids = response["esearchresult"]["idlist"]

    if not ids:
        return "No articles found."

    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "rettype": "abstract",
        "retmode": "text"
    }
    abstracts = requests.get(fetch_url, params=fetch_params).text
    return abstracts[:2000]


@tool
def check_drug_info(drug_name: str) -> str:
    """Look up drug information and adverse effects from OpenFDA."""
    url = "https://api.fda.gov/drug/label.json"
    params = {"search": f"openfda.brand_name:{drug_name}", "limit": 1}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return f"No information found for {drug_name}."

    data = response.json()
    result = data["results"][0]
    warnings = result.get("warnings", ["No warnings found"])[0][:500]
    indications = result.get("indications_and_usage", ["Not found"])[0][:500]

    return f"Indications: {indications}\nWarnings: {warnings}"


@tool
def assess_urgency(symptoms: str) -> str:
    """Assess the urgency level of symptoms based on keywords."""
    high_urgency = ["chest pain", "difficulty breathing", "unconscious",
                    "severe bleeding", "stroke", "heart attack", "seizure"]
    medium_urgency = ["high fever", "vomiting", "severe pain", "infection", "fracture"]

    symptoms_lower = symptoms.lower()

    if any(keyword in symptoms_lower for keyword in high_urgency):
        return "URGENCY: HIGH — Immediate medical attention required."
    elif any(keyword in symptoms_lower for keyword in medium_urgency):
        return "URGENCY: MEDIUM — Should be seen within a few hours."
    else:
        return "URGENCY: LOW — Can be scheduled for routine care."