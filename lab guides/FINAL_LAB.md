# Final Lab Guide: Faculty Chatbot (5_final_lab.py)

## Prerequisites

1. Python 3.10 or newer.
2. Open this workspace in VS Code.
3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Configure a `.env` file with:
- `OPENAPI_BASE_URL`
- `OPENAPI_API_KEY`
- `OPENAPI_MODEL`

5. Use this lab file:
- `5_final_lab.py`

## Lab Completion Criteria

Complete all four TODOs in `5_final_lab.py`.

## TODO 1: Agent Instructions

Location:
- `build_agent()`

Action:
1. Uncomment the instruction lines under TODO 1.

Expected outcome:
- The agent gets richer DBMS-specific behavior guidance.

## TODO 2: Tooling

Locations:
- Commented tool function blocks near the top of the file.
- `tools=[...]` line inside `build_agent()`.

Action:
1. Uncomment both tool functions:
- `save_faculty_context`
- `suggest_classroom_activity`
2. Uncomment the agent tool-registration line:
- `tools=[save_faculty_context, suggest_classroom_activity],`
3. Remove or replace the temporary fallback:
- `tools=[]`

Expected outcome:
- Tool calling is enabled and available to the agent.

## TODO 3: Memory Save Block

Location:
- `run_chatbot()` memory block under TODO 3.

Action:
1. Uncomment the full `await agent.run(...)` block that sends:
- `Save faculty context with subject=... class_level=...`

Expected outcome:
- Faculty context is saved into session memory through tool usage.

## TODO 4: Evaluators

Locations:
- Evaluator block in `run_evaluation_demo()`.
- Evaluator call lines in `run_chatbot()`.

Action:
1. Uncomment the evaluator logic block in `run_evaluation_demo()`.
2. Uncomment the two lines in `run_chatbot()` that invoke evaluation.

Expected outcome:
- Built-in evaluators run after the single bot response:
- `keyword_check`
- `tool_called_check`

## Validation Commands

Run after completing all TODOs:

```bash
python -m py_compile 5_final_lab.py
python 5_final_lab.py
```

## Suggested One-Prompt Test

1. Topic focus: `joins`
2. Class level: `second-year CSE`
3. User prompt: `Explain inner join with one example.`

Lab is complete when all TODO blocks are uncommented correctly and the script runs without errors.