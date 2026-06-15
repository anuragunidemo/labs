# OpenAPI + Faculty Labs

This workspace contains:
- OpenAPI client examples
- a LangChain-based faculty workflow
- a PDF/RAG-based faculty workflow
- one GHCP-focused step-by-step lab guide
- one M365 Copilot Chat faculty lab guide (trial-friendly)
- one Microsoft Agent Framework terminal chatbot lab guide

## GHCP Step-by-Step Lab
Use this guide:
- lab guides/GHCP_FACULTY_LAB.md

Before starting, complete prerequisites:
- lab guides/LAB_PREREQUISITES.md

This guide is focused on GitHub Copilot Chat usage inside VS Code with real workspace files.

## M365 Copilot Faculty Lab (Trial-Friendly)
Use this guide:
- lab guides/M365_COPILOT_FACULTY_LAB_TRIAL.md

This guide is focused on Microsoft 365 Copilot Chat scenarios for faculty day-to-day work,
with sample inputs in `m365_lab_assets/` and workflows that still work on common trial setups.

## Microsoft Agent Framework Terminal Chatbot Lab
Use this guide:
- lab guides/FINAL_LAB.md

This guide is focused on a terminal-based faculty chatbot built with Microsoft Agent Framework,
including function calling, session-backed memory, and step-by-step copy-paste instructions.

## Prerequisites Summary
Use the full checklist here first:
- lab guides/LAB_PREREQUISITES.md

Minimum prerequisites before running any lab:
- VS Code installed
- Python 3.10+ with pip
- GitHub account access
- Microsoft account, Azure Free account, and access to Azure Portal + Microsoft Foundry

## Run
1. Complete prerequisites first:
   - lab guides/LAB_PREREQUISITES.md
2. Clone the repository locally and open the lab root folder:
   - git clone https://github.com/anuragunidemo/labs.git
   - cd labs
3. Run the startup script in the current terminal (creates `.venv`, activates it, upgrades pip, installs from `requirements.txt`):
   . .\startup_lab.ps1
   
   **Important:** The first run will take **5–10 minutes** to resolve and download all dependencies. This is normal and a one-time cost. Subsequent runs will be much faster using pip's cache.
   
   Watch the terminal output for progress. When you see `[Done] Lab environment is ready.`, setup is complete.
4. If needed, activate virtual environment manually in a new terminal:
   .\.venv\Scripts\Activate.ps1
5. Create or update your .env file:
   - OPENAPI_BASE_URL
   - OPENAPI_API_KEY
   - OPENAPI_MODEL
6. Run basic client example:
   python 1_llmapiexample.py
7. Run LangChain faculty lab:
   python 2_langchainlab.py
8. Run LangGraph faculty lab (same workflow, graph-based orchestration):
   python 3_langgraphlab.py
9. Run PDF-based RAG lab:
   python 4_raglab.py
10. Run Microsoft Agent Framework chatbot lab:
   python 5_final_lab.py

## Files
- 1_llmapiexample.py
- 2_langchainlab.py
- 3_langgraphlab.py
- 4_raglab.py
- 5_final_lab.py
- startup_lab.ps1
- lab guides/GHCP_FACULTY_LAB.md
- lab guides/LAB_PREREQUISITES.md
- lab guides/M365_COPILOT_FACULTY_LAB_TRIAL.md
- lab guides/FINAL_LAB.md
- requirements.txt
- pdfs/
- m365_lab_assets/
