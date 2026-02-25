# Medical Triage Agent

I built this because I kept reading about how much time doctors and nurses waste on admin work — reviewing records, looking up drug info, figuring out how urgent a case is. It felt like exactly the kind of repetitive, research-heavy task that AI should be handling. So I built an agent that does it.

You describe a patient case. The agent figures out what it needs to know, searches real medical databases, checks drug warnings, and gives you a triage report. No hardcoded steps — it reasons its way through each case on its own.

**Live demo:** https://medicaltriageagent.streamlit.app

---

## What it does

- Reads a patient case (typed or uploaded as a PDF)
- Decides the urgency — HIGH, MEDIUM, or LOW
- Searches PubMed for relevant research on the condition
- Looks up drug warnings from the FDA database if a medication is mentioned
- Shows you exactly which tools it used and why

---

## How it works

The agent runs on a ReAct loop — it reasons, acts, checks the result, then reasons again. It's not a pipeline where steps are fixed. It decides what to do based on what the patient case actually says.

```
Patient case
     │
     ▼
ReAct Agent (LangGraph)
     │
     ├── assess_urgency      → keyword-based urgency classifier
     ├── search_pubmed       → NCBI PubMed API
     └── check_drug_info     → OpenFDA API
     │
     ▼
Triage Report
```

---

## Stack

- **LLM** — Llama 3.3 70B on Groq (free)
- **Agent** — LangGraph ReAct
- **Tools** — PubMed NCBI API, OpenFDA API
- **PDF parsing** — pdfplumber
- **UI** — Streamlit

Everything is free to run. No paid APIs needed.

---

## Running it locally

You'll need Python 3.10+ and a free Groq API key from [console.groq.com](https://console.groq.com).

```bash
git clone https://github.com/ashvathhh/medical-triage-agent.git
cd medical-triage-agent

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install langchain langchain-groq langgraph streamlit pdfplumber requests python-dotenv langchainhub
```

Create a `.env` file:

```
GROQ_API_KEY=your_key_here
```

Then run:

```bash
streamlit run app.py
```

---

## Try these cases

```
A 58 year old male has chest pain and shortness of breath. He is on metformin. What is the urgency?
```

```
A 45 year old female has type 2 diabetes, is overweight, and has high blood pressure. What does research say about treatment?
```

```
A 70 year old with seizure history is on ibuprofen and has severe headaches. What should we do?
```

---

## Project structure

```
medical-triage-agent/
├── agent/
│   ├── agent.py       # LangGraph ReAct agent
│   └── tools.py       # PubMed, OpenFDA, urgency tools
├── app.py             # Streamlit UI
├── .env               # API keys (not committed)
└── README.md
```

---

## What's next

- Add a second agent that reviews and validates triage decisions
- Persistent history across sessions
- Deploy publicly on Streamlit Cloud

---

Built by [Ashvath Cheppalli](https://www.linkedin.com/in/ashvath-cheppalli-0ab28a249)