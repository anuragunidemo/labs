# GitHub Copilot Chat Lab for Engineering Faculty (India)

Works with GitHub Copilot Chat free trial in VS Code, using these workspace files:
- 2_langchainlab.py
- 4_raglab.py
- 1_llmapiexample.py

---

## Step 1: Learn and Use Common / Commands First

Purpose:
Start with slash commands so faculty can use GHCP features quickly before doing file-level tasks.

How to begin:
1. In chat, type `/` and review available commands.
2. Run `/help` to confirm the active command set in your VS Code build.
3. Open 2_langchainlab.py and select one function.
4. Run `/explain` on the selection.
5. Run `/doc` on the same selection to create concise docstrings/comments.

If you have a runtime issue available:
6. Run the script and use `/fix` on the failing block.
7. Use `/tests` to generate quick checks for the updated function.

Expected outcome:
- Faculty can discover and use GHCP slash commands confidently.
- Team has a repeatable command-first workflow before deeper edits.

How this reduces manual effort:
- Manual feature discovery and trial/error: 15 to 25 min
- With command-first GHCP flow: 5 to 10 min
- Typical saving: 10 to 15 min at session start

---

## Step 2: Setup
1. Open this workspace in VS Code.
2. Ensure GitHub Copilot Chat extension is installed and signed in.
3. Open GHCP chat panel.
4. Keep these files visible in editor tabs:
  - 2_langchainlab.py
  - 4_raglab.py
   - ../README.md

Expected outcome:
- Chat is active and can see current file/workspace context.

Manual time saved:
- Not a time-saving step; this enables later savings.

---

## Step 3: Understand Existing Teaching Workflow from Code

Purpose:
Use GHCP to read your actual script and explain the teaching pipeline, instead of manually tracing code.

Prompt to try:
```text
Analyze 2_langchainlab.py in this workspace and explain:
1) the full flow of data from input topic to final outputs,
2) where lecture plan, quiz/rubric, and remediation are produced,
3) what I should modify to adapt this for 2nd-year ECE students in India.
Return your answer as:
- Code flow summary
- Exact sections/functions to edit
- Risks if I only change prompt text
```

Revision prompt:
```text
Now rewrite that as a faculty action checklist with only practical edits I should make today.
Limit to 8 bullet points.
```

Expected output:
- Clear file-aware explanation tied to code structure
- specific edit points (not generic advice)
- concise action checklist

How this reduces manual effort:
- Manual code walkthrough: 20 to 30 min
- With GHCP workspace explanation: 5 to 8 min
- Typical saving: 15 to 22 min per script onboarding

---

## Step 4: Ask GHCP to Perform a Targeted Code Upgrade

Purpose:
Perform a real improvement in your existing teaching script, not just content generation.

Prompt to try:
```text
In 2_langchainlab.py, add a new optional parameter called class_profile
that captures student background (for example: mixed English/Hindi medium,
weak Python basics, strong exam orientation).

Apply this profile in all three tasks:
- lecture plan
- quiz and rubric
- remediation plan

Then show the exact code changes and explain why each change is needed.
```

Revision prompt:
```text
Revise the change so class_profile defaults to a practical Indian engineering class profile,
and add one short validation check so empty profile values are handled gracefully.
```

Expected output:
- concrete code edits in the real file
- consistent propagation of new parameter across pipeline
- explanation of impact on prompt quality and output relevance

How this reduces manual effort:
- Manual cross-function refactor: 30 to 45 min
- With GHCP guided edit: 10 to 15 min
- Typical saving: 20 to 30 min

---

## Step 6: Prompt-Driven Artifact Generation

Purpose:
Faculty learn to write a single precise prompt that produces a complete teaching
artifact — coding exercise scaffold, rubric, or test file — without manual authoring.
This is the highest-leverage GHCP skill: one prompt replaces hours of preparation.

---

### 6.1 – Understand what makes a prompt produce a usable artifact

Every artifact-generation prompt has **five essential parts**:

| Part | What to include | Example |
|---|---|---|
| ROLE | Who GHCP acts as | "You are a Python faculty at Anurag University" |
| CONTEXT | Subject, semester, student profile | "CSE Sem 1, 60 students, exam-oriented" |
| ARTIFACT | Exactly what to produce | "a Python lab file with 4 TODOs" |
| CONSTRAINTS | Format, tools, Bloom's level | "No external libs, Python 3.10+" |
| OUTPUT FORM | Structure of the response | "One Python file, no prose outside" |

**Without all five parts** the output is generic and requires heavy revision.  
**With all five parts** the output is ready to use as-is.

---

### 6.2 – CARD 1: Generate a coding exercise scaffold

**Prompt goal:** produce a Python lab file with 4 TODOs and hints in one shot.

#### Paste this into GHCP Chat:

```
ROLE:
You are a Python programming faculty at Anurag University, Hyderabad,
teaching B.Tech CSE Semester 1.

CONTEXT:
Topic from the Anurag University CSE curriculum: Functions and Recursion in Python.
Students have completed basic control flow and lists.
Class size: 60 students, mixed English/Telugu medium, exam-oriented.

ARTIFACT:
Create a Python lab exercise file (lab_functions_recursion.py) that students
complete by writing code themselves during a 90-minute lab session.

CONSTRAINTS:
- Include exactly 4 TODOs, each with a short, non-obvious hint comment
- TODO 1: a pure function (factorial, iterative)
- TODO 2: the same function rewritten as recursion
- TODO 3: a second recursive problem (Fibonacci with memoization)
- TODO 4: a helper that pretty-prints a comparison table of both approaches
- Add sample input/output as assert statements at the bottom
- No external libraries, Python 3.10+ only
- Map each TODO to a Bloom's taxonomy level in a comment
- Hints should guide direction but not reveal full logic or full code structure

OUTPUT FORM:
Return a single Python file, no prose outside the file.
Include a module-level docstring with learning outcomes and Bloom's mapping.
```

#### Then paste this follow-up revision:

```
Revise the file so:
1. Replace any direct solution hints with subtler clue-style hints (no step-by-step)
2. The assert block prints PASS/FAIL per assertion, not just raises
3. Add a STRETCH TODO at the end: implement Tower of Hanoi recursively
```

**What to look for:**
- Each TODO has a non-obvious hint but does not give away the solution
- Bloom's levels are listed (e.g., Understand L2, Apply L3, Analyze L4)
- assert statements let students self-check their work

---

### 6.3 – CARD 2: Generate a rubric

**Prompt goal:** produce a TA-ready grading rubric for a linked list assignment.

#### Paste this into GHCP Chat:

```
ROLE:
You are a senior CSE faculty at Anurag University preparing assessment material.

CONTEXT:
Course: Data Structures Using Python | B.Tech CSE Semester 3
Assignment: Implement a singly linked list with insert, delete, search, and reverse.
Students submit a Python .py file and a brief PDF explanation.
TAs grade 120 submissions.

ARTIFACT:
Create a detailed grading rubric for this assignment.

CONSTRAINTS:
- 5 criteria: Correctness, Code Quality, Edge Cases, Documentation, Complexity Analysis
- 4 levels per criterion: Excellent (4), Good (3), Average (2), Poor (1)
- Total score out of 100 with per-criterion weights
- Include one concrete example of what each level looks like for Correctness
- Add a TA quick-reference checklist (10 checkboxes, yes/no)
- Bloom's level for each criterion in parentheses

OUTPUT FORM:
Markdown tables only. No prose paragraphs.
End with a one-line formula: Final_score = weighted sum.
```

#### Then paste this follow-up revision:

```
Revise the rubric so:
1. Add a Plagiarism / AI-misuse row (weight 0, but flags submission for review)
2. Convert the TA checklist into a two-column table: Check | Evidence to look for
3. Add a Grade band: 90-100 = O, 80-89 = A+, etc. using Anurag University scale
```

**What to look for:**
- Rubric is in Markdown table format, easy to copy into LMS
- Each criterion has 4 clear levels with point values
- TA checklist is concrete (not vague)

---

### 6.4 – CARD 3: Generate a pytest auto-grader

**Prompt goal:** produce test_linked_list.py that TAs can run on 120 student submissions.

#### Paste this into GHCP Chat:

```
ROLE:
You are a CSE lab coordinator at Anurag University.

CONTEXT:
Students submit lab_linked_list.py which must define a class LinkedList with:
  insert(value)   – insert at head
  delete(value)   – delete first occurrence
  search(value)   – return True/False
  reverse()       – reverse in place
  to_list()       – return Python list of current values

ARTIFACT:
Create a pytest test file test_linked_list.py that auto-grades the submission.

CONSTRAINTS:
- At least 12 test functions, grouped by method
- Cover: empty list, single element, duplicates, non-existent value
- Use descriptive test names (test_insert_into_empty_list, etc.)
- Add a module docstring explaining how to run: pytest test_linked_list.py -v
- No mocking, no fixtures — just direct LinkedList usage
- Final test: test_combined_sequence that inserts 10 items, deletes 3, reverses, checks to_list()

OUTPUT FORM:
One Python file. Pure pytest, no unittest. No prose outside the file.
```

#### Then paste this follow-up revision:

```
Revise the test file:
1. Add a @pytest.mark.parametrize test for insert covering 5 different input sequences
2. Add a test that imports the student file and catches ImportError gracefully,
   printing "LinkedList class not found – check filename and class name"
3. Add a score comment at the top: each test = N marks, total = 50
```

**What to look for:**
- Test names are descriptive (not just test_1, test_2)
- Edge cases are covered (empty list, single element, duplicates)
- pytest parametrize reduces redundant test code

---

### 6.5 – CARD 4: Full lab from one sentence

**Prompt goal:** generate scaffold + rubric + test + session plan all at once.

#### Paste this into GHCP Chat:

```
Pick a topic from the curriculum for CSE at Anurag University and build a lab
that faculty can use to create a coding exercise.

The output must include:
1. A Python scaffold file with 4 TODOs and subtle hints embedded as comments
2. A grading rubric as a Markdown table
3. A pytest test file for auto-grading student submissions
4. A 10-line faculty session plan (what to say/do each 5 minutes)

Constraints:
- Topic must be from Semester 1–3 CSE curriculum
- Suitable for 90-minute lab slot
- Free-trial GHCP compatible (no API keys or plugins required)
- All three files must be self-contained, no shared imports
```

#### Then paste this follow-up revision:

```
Revise the output:
1. Change the topic to String Methods and Regular Expressions in Python
2. Make the scaffold file work specifically with Anurag University student roll number
   format (e.g., 22CSE101) — add a validation function as TODO 1
3. Add a 5th TODO that uses the re module to parse a CSV of student data
```

**What to look for:**
- GHCP returns THREE separate files (scaffold, rubric, test)
- PLUS a brief session plan that tells you what to say each 5 minutes
- One prompt replaced what would take a full afternoon to write manually

---

### 6.6 – Free card: write your own

Use this blank template to create an artifact for your own subject:

```
ROLE:
You are a [SUBJECT] faculty at Anurag University teaching [COURSE] Semester [N].

CONTEXT:
Topic: [pick from your syllabus]
Students have already covered: [prerequisites]
Class profile: [size, medium, exam-focus level]

ARTIFACT:
Create [lab file / rubric / test file / lecture plan / all of the above]

CONSTRAINTS:
- [list specific requirements, e.g. "4 TODOs", "Bloom's levels", "no third-party libs"]
- [add format constraints]

OUTPUT FORM:
[describe exact format — table / code block / numbered list / markdown headings]
```

Fill in your own details, paste into GHCP Chat, and compare the output quality to CARD 4.

**Discussion prompt for faculty:**  
> "Which part of the five-part anatomy was hardest to write for your subject?"

---

### What this step demonstrates

| Prompt card | Artifact produced | Time manual | Time with GHCP |
|---|---|---|---|
| CARD 1 | Coding exercise .py with TODOs + prompts | 90–120 min | 5 min |
| CARD 2 | TA rubric with weights + checklist | 45–60 min | 4 min |
| CARD 3 | 12-function pytest auto-grader | 60–90 min | 4 min |
| CARD 4 | All three above + session plan | 3–5 hours | 8 min |

**Total saving from Step 6 alone: 3 to 5 hours per new lab topic.**

---

## End-of-Lab Deliverables
By the end of this lab, faculty should have:
1. one improved code workflow in 2_langchainlab.py
2. one revised, class-profile-aware teaching artifact
3. at least one complete teaching artifact (lab file, rubric, or test) generated from a single structured prompt

This is the practical advantage of GHCP inside VS Code: faster outcomes anchored to your actual codebase, not generic standalone answers.
