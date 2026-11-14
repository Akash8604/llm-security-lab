# LLM Security Lab

**Reproducible AI Security Research | Prompt Injection Testing | LLM Application Security**

A hands-on, locally controlled security research project exploring vulnerabilities, trust boundaries, and reliability failures in applications powered by large language models.

The project combines a FastAPI-based document retrieval application, local Ollama models, controlled adversarial experiments, automated testing, and timestamped JSON evidence.

**Research status:** Active  
**Documented experiments:** PI-002 through PI-011, plus an initial PI-001 observation  
**Automated tests:** 38 passed  
**Environment:** Local and synthetic

---

## 1. Project Overview

LLM-powered applications frequently process external documents, user messages, retrieved information, and other potentially untrusted inputs.

This project investigates how those inputs may influence model behavior and whether application-level security controls adequately enforce trust boundaries.

The research covers:

- Direct and indirect prompt injection
- System prompt extraction
- Guardrail and confidentiality testing
- Tool and function-call abuse
- RAG access-control failures
- Agent privilege escalation
- Synthetic application-memory extraction
- Multimodal prompt injection
- Nested, encoded, and repeated instruction injection

Each experiment is designed to produce reproducible evidence rather than rely solely on theoretical examples.

Research findings distinguish between observed security failures, unsuccessful attacks, reliability issues, and intentionally vulnerable test fixtures.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.11 |
| API framework | FastAPI |
| Local model runtime | Ollama |
| Primary language model | Llama 3.1 8B |
| Multimodal model | LLaVA 7B |
| HTTP client | httpx |
| Image processing | Pillow |
| Automated testing | pytest |
| Evidence storage | Timestamped JSON |
| Version control | Git and GitHub |

All model experiments run locally without requiring a paid cloud-model API.

## 3. Application Architecture

The project includes a lightweight FastAPI application for document ingestion, retrieval, and LLM-based question answering.

### Application capabilities

- Document ingestion and storage
- Keyword-based document retrieval
- Local LLM integration through Ollama
- Untrusted document labeling
- API input validation
- Automated application tests
- Independent security experiment scripts
- Structured JSON evidence collection

### API endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Application information |
| `/health` | GET | Health check |
| `/documents` | POST | Ingest documents |
| `/documents` | GET | List documents |
| `/search` | POST | Search stored documents |
| `/chat` | POST | Ask questions using local LLM integration |

The document retrieval implementation is intentionally lightweight and keyword-based. It is not a production vector database or enterprise RAG platform.

## 4. Security Research Portfolio

The following experiments were performed using local models, synthetic data, and controlled fixtures.

| ID | Research Area | Key Observation | Report |
|---|---|---|---|
| PI-002 | Indirect Prompt Injection | No confirmed instruction takeover; injected content was sometimes quoted or rejected | [Report](research/PI-002.md) |
| PI-003 | Direct Prompt Injection | No exact target-marker disclosure in two tested attacks | [Report](research/PI-003.md) |
| PI-004 | System Prompt Extraction | Synthetic confidential system marker disclosed in repeated direct extraction tests | [Report](research/PI-004.md) |
| PI-005 | Guardrail Bypass | No secret disclosures; some deviations from exact refusal formatting | [Report](research/PI-005.md) |
| PI-006 | Tool / Function-Call Abuse | No unauthorized transfer calls or executions in the simulated tool environment | [Report](research/PI-006.md) |
| PI-007 | RAG Access Control | Restricted content entered model context in an intentionally insecure fixture; secure filtering prevented retrieval | [Report](research/PI-007.md) |
| PI-008 | Agent Privilege Escalation | No unauthorized privilege grants; unverified approval claim appeared in model output | [Report](research/PI-008.md) |
| PI-009 | Application Memory Extraction | Synthetic cross-user memory disclosure in an intentionally insecure fixture; secure filtering prevented access | [Report](research/PI-009.md) |
| PI-010 | Multimodal Prompt Injection | One intermittent synthetic marker disclosure across controlled image evaluations | [Report](research/PI-010.md) |
| PI-011 | Nested and Repeated Instruction Injection | Task-completion degradation observed; harmless repetition also triggered refusal | [Report](research/PI-011.md) |

An earlier PI-001 experiment explored explicit instruction override through retrieved document content.

### 4.1 Selected Research Findings

**PI-004 — System Prompt Extraction**

A local Llama 3.1 8B model was configured with a synthetic confidential system-level marker.

Direct extraction requests disclosed the marker in four repeated evaluations.

This demonstrated a confidentiality-instruction failure in the controlled setup, not unauthorized extraction from an external system.

**PI-007 — RAG Access-Control Testing**

A deliberately insecure retrieval fixture allowed a restricted document to enter the model's context.

A secure filtering configuration prevented the same unauthorized retrieval.

The experiment demonstrates the importance of enforcing authorization before retrieved content reaches the language model.

**PI-009 — Synthetic Cross-User Memory Extraction**

An intentionally insecure application-memory fixture allowed a simulated user to retrieve another simulated user's private memory.

The model disclosed a synthetic marker from that memory.

A secure configuration prevented the unauthorized access.

This was an application-memory isolation experiment, not extraction of the model's training data.

**PI-010 — Multimodal Prompt Injection**

Real PNG images containing support-ticket content and adversarial instructions were submitted to a locally hosted LLaVA 7B model.

Across 18 image evaluations, one exact synthetic confidential-marker disclosure was observed.

The disclosure was intermittent and was not reproduced in the additional controlled comparisons.

The evidence does not establish that visual authority spoofing was the unique cause of the disclosure.

**PI-011 — Nested, Encoded, and Repeated Instructions**

The experiment evaluated nested fake system messages, repeated authority claims, Base64-encoded instructions, and instruction saturation.

Across 24 evaluations:

- No exact confidential-marker disclosures were detected.
- No exact output-hijack markers were detected.
- All 12 adversarial evaluations resulted in legitimate task refusal.
- Harmless repeated text also triggered refusal in all three control trials.

The primary finding was repeatable task-completion degradation with a repetition-related confounding factor.

The term *recursive token shadowing* is used as an operational experimental label, not as a universally standardized vulnerability classification.

## 5. Project Structure

```text
llm-security-lab/
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── experiments/
│   ├── run_pi002.py
│   ├── ...
│   ├── run_pi010.py
│   ├── run_pi010_control.py
│   ├── run_pi011.py
│   └── run_pi011_control.py
│
├── tests/
│   ├── test_api.py
│   ├── test_prompt_injection.py
│   ├── test_multimodal.py
│   ├── test_shadowing.py
│   └── ...
│
└── research/
    ├── PI-002.md
    ├── ...
    ├── PI-011.md
    │
    ├── assets/
    │   └── pi010/
    │       ├── baseline.png
    │       ├── visual_direct_injection.png
    │       ├── visual_authority_spoofing.png
    │       └── visual_output_hijack.png
    │
    └── results/
        ├── pi002_*.json
        ├── ...
        └── pi011_*.json
```

The directory listing is abbreviated to highlight the primary components. Experiment-specific files and evidence are available in the repository.

## 6. Local Setup

### Prerequisites

- Python 3.11
- Git
- Ollama
- Sufficient memory to run the selected local models

### Clone the repository

```powershell
git clone https://github.com/Akash8604/llm-security-lab.git
cd llm-security-lab
```

### Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install Python dependencies

```powershell
python -m pip install -r requirements.txt
```

### Install local models

Install Ollama from its official website.

Pull the primary language model:

```powershell
ollama pull llama3.1:8b
```

For multimodal experiments:

```powershell
ollama pull llava:7b
```

If `ollama` is not recognized in PowerShell, use the full executable path or configure the Ollama installation directory in PATH.

Ensure that the Ollama service is running before executing model-dependent experiments.

## 7. Running the Application

Start the FastAPI application:

```powershell
python -m uvicorn main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

Check the application health endpoint:

http://127.0.0.1:8000/health

The API provides a local environment for exploring document ingestion, retrieval, and LLM-assisted responses.

## 8. Reproducing Security Experiments

Run an individual experiment from the repository root.

### Direct prompt injection

```powershell
python -m experiments.run_pi003
```

### System prompt extraction

```powershell
python -m experiments.run_pi004
```

### Multimodal prompt injection

```powershell
python -m experiments.run_pi010
```

### Multimodal controlled comparison

```powershell
python -m experiments.run_pi010_control
```

### Nested and repeated instruction injection

```powershell
python -m experiments.run_pi011
```

### Harmless formatting controls

```powershell
python -m experiments.run_pi011_control
```

These commands require the corresponding experiment scripts and locally installed models.

Experiment outputs are stored under:

`research/results/`

Each execution generates timestamped JSON evidence containing the tested scenario, model response, and recorded evaluation metrics.

## 9. Automated Testing

Run the complete test suite:

```powershell
python -m pytest -q
```

Latest recorded local test result:

```text
38 passed, 1 warning in 1.45s
```

The warning is a dependency deprecation warning associated with Starlette's test-client integration and does not indicate a failed test.

### Test coverage includes

- FastAPI endpoint behavior
- Document ingestion and retrieval
- Input validation
- Security experiment fixtures
- Simulated tool and access-control logic
- Multimodal experiment asset validation
- Nested-instruction scenario validation
- Saved JSON evidence consistency

Automated tests validate defined behaviors and experiment artifacts. They do not prove that the model or application is universally resistant to prompt injection.

## 10. Research Methodology

The experiments generally follow a structured process:

1. Define a legitimate application task and expected behavior.
2. Establish the trust boundary being evaluated.
3. Construct a synthetic adversarial payload.
4. Execute the payload against a locally controlled model or application fixture.
5. Capture the model's actual response and relevant execution metadata.
6. Compare the response against defined success and failure indicators.
7. Repeat selected tests to assess consistency.
8. Introduce benign controls when necessary to investigate alternative explanations.
9. Document observations, limitations, and potential mitigations.
10. Preserve scripts, evidence, and research reports in version control.

### Evidence principles

The project distinguishes among:

- **Observed disclosure:** A synthetic marker or protected value appears in an actual response.
- **Instruction takeover:** Evidence indicates that the model followed an unauthorized instruction.
- **Answer contamination:** The model produces unsupported or attacker-influenced content.
- **Task-completion failure:** The model fails to perform the legitimate task.
- **Secure boundary behavior:** The tested application or model prevents the specific unauthorized action.
- **Inconclusive result:** The available evidence does not support a definitive causal conclusion.

An attack is not classified as successful solely because malicious text appears in a response.

## 11. Limitations

This repository is a controlled research environment rather than a production security assessment.

Important limitations include:

- Local models and synthetic data.
- A limited number of models and adversarial scenarios.
- Keyword-based retrieval in the primary application.
- Simulated tools, agents, access controls, and application memory in selected experiments.
- No production vector database or external enterprise environment.
- Limited repeatability testing for some experiments.
- Exact-marker checks that may miss more subtle behavioral failures.
- Results that may vary with model version, hardware, configuration, and generation settings.
- No general security guarantees for the evaluated models.

Findings from intentionally insecure fixtures demonstrate the behavior of those fixtures, not vulnerabilities in third-party products.

## 12. Responsible Research

All experiments are conducted against locally controlled models, synthetic documents, or intentionally constructed test environments.

The project does not involve unauthorized access to external systems, real customer information, or third-party production applications.

The purpose is to understand AI application security boundaries, evaluate defensive behavior, and develop reproducible testing methods.

## 13. Future Research

Potential future directions include:

- Stronger retrieval authorization and document isolation
- Prompt injection detection and filtering comparisons
- Cross-model robustness testing
- Structured tool-call authorization enforcement
- Agent workflow security testing
- More extensive multimodal evaluations
- Regression testing for previously observed failures
- Evaluation metrics beyond exact-string matching

## 14. Project Status

**Active independent AI security research project.**

Current documented portfolio:

- 10 experiments from PI-002 through PI-011.
- One earlier PI-001 observation.
- 24 evaluations in PI-011.
- 18 image evaluations in PI-010.
- 38 passing automated tests in the latest recorded run.
- Research reports, experiment scripts, and timestamped JSON evidence maintained in GitHub.

The project is intended to demonstrate practical experimentation, security reasoning, evidence-based reporting, and reproducible AI application security testing.

---

**Repository:** https://github.com/Akash8604/llm-security-lab