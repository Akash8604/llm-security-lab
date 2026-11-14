
# LLM Security Lab

A local, reproducible research project for testing security
boundaries in LLM-powered document retrieval applications.

## Overview

This project investigates how a local language model handles
potentially malicious instructions embedded in retrieved documents.

The application uses FastAPI, Ollama, and Llama 3.1 8B.

Research focuses on indirect prompt injection, instruction
hierarchy, untrusted document content, and response behavior.

## Technology Stack

- Python 3.11
- FastAPI
- Ollama
- Llama 3.1 8B
- pytest
- httpx

## Features

- Document ingestion API
- Keyword-based document retrieval
- Local LLM integration
- Untrusted document labeling
- Automated API tests
- Isolated prompt injection experiments
- Timestamped JSON evidence collection

## Project Structure

```text
llm-security-lab/
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
├── experiments/
│   └── run_pi002.py
├── tests/
│   ├── test_api.py
│   └── test_prompt_injection.py
└── research/
    ├── PI-002.md
    └── results/
```

## Setup

Create and activate a Python virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Install Ollama and download the model:

```powershell
ollama pull llama3.1:8b
```

Start the application:

```powershell
python -m uvicorn main:app --reload
```

Open the API documentation:

http://127.0.0.1:8000/docs

## Automated Tests

```powershell
python -m pytest tests -v
```

Seven automated tests passed in the recorded local test run.

These tests validate API behavior, input validation,
document ingestion, and retrieval. They do not establish
general prompt-injection resistance.

## Security Experiments

### PI-001 — Explicit Instruction Override

A retrieved document attempted to override the user's task
and force an unrelated output sentence.

Observed outcome: the model rejected the instruction and
answered the legitimate authentication question.

### PI-002 — Claimed Compliance Authority

A retrieved document presented an unauthorized instruction
as an internal compliance formatting requirement.

Observed behaviors included:

- Rejection of the embedded instruction
- Correct answers to the legitimate question
- Quotation of injected text while rejecting it
- Occasional refusal to complete the legitimate task

No observed run visibly complied with the requested
instruction to append the exact target sentence as an
approved final statement.

See [PI-002 Research Report](research/PI-002.md).

## Reproduce PI-002

```powershell
python -m experiments.run_pi002
```

Timestamped JSON evidence is saved under `research/results/`.

## Limitations

- Local research environment
- Keyword-based retrieval, not vector search
- Limited payload categories and experimental runs
- Model generation settings not explicitly fixed
- No production deployment or external target testing
- No claim of general LLM security guarantees

## Responsible Research

All experiments target a locally controlled application
using synthetic policy documents.

The project does not claim unauthorized access to
third-party systems or vulnerabilities in external services.

## Status

Active research project.
```
