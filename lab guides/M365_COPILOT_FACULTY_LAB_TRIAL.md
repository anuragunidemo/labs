# Microsoft 365 Copilot Lab for Teaching Faculty (Trial-Friendly)

Duration: 75 to 90 minutes
Audience: Teaching faculty, course coordinators, and TAs
Mode: Hands-on using Microsoft 365 Copilot Chat

This lab is designed to work even when you only have a trial setup, by prioritizing Copilot Chat workflows that do not depend on advanced in-app Copilot features.

## What Works on Trial (Baseline)

Primary mode used in this lab:
- Microsoft 365 Copilot Chat (web/chat experience)
- Prompting over uploaded files and pasted text
- Summarization, drafting, planning, rubric generation, and communication support

Optional mode (if your trial tenant enables it):
- In-app Copilot in Word/PowerPoint/Excel/Outlook/Teams

If in-app Copilot is unavailable, complete all tasks in Copilot Chat and copy the outputs into Office apps manually.

## Faculty Day-Job Scenarios Covered

1. Convert raw course notes into a faculty-ready weekly teaching plan
2. Build remediation plan from class performance data
3. Draft clear student and parent communications
4. Create a TA-consistent grading rubric and viva bank
5. Generate accreditation-friendly CO-PO evidence summary
6. Convert meeting notes into actions, owners, and deadlines

All scenario inputs are pre-created in this workspace under `../m365_lab_assets/`.

## Prerequisites (5 min)

1. Sign in with your institutional account to Microsoft 365 Copilot Chat.
2. Keep this workspace open for easy copy/paste and file upload.
3. Ensure you can upload files in Copilot Chat.
4. Open these files:
   - `../m365_lab_assets/course_outline_cs101.md`
   - `../m365_lab_assets/class_performance_sample.csv`
   - `../m365_lab_assets/faculty_meeting_notes_raw.txt`
   - `../m365_lab_assets/student_email_threads.txt`
   - `../m365_lab_assets/assignment_brief_raw.md`
   - `../m365_lab_assets/accreditation_mapping_template.md`

## Lab Flow

## Step 1 - Course Planning Assistant (12 min)

Goal:
Turn a draft syllabus into a practical 14-week delivery plan with remediation windows.

Input file:
- `../m365_lab_assets/course_outline_cs101.md`

Prompt:
```text
You are an experienced engineering faculty mentor.
Using the uploaded course outline, produce:
1) A 14-week teaching plan with week objective, class activity, and expected student outcome.
2) A remediation strategy for weak students (attendance or performance risk).
3) A TA support plan with weekly responsibilities.

Constraints:
- Target: B.Tech CSE Sem 1, mixed proficiency classroom.
- Keep language simple and implementation-focused.
- Include measurable outcomes each week.
Output as markdown tables.
```

Follow-up prompt:
```text
Revise for a 60-minute lab slot per week and add one low-cost classroom activity per week.
```

Expected output:
- Ready-to-use weekly teaching plan
- Structured remediation + TA workload guidance

## Step 2 - Data-Aware Remediation Plan (12 min)

Goal:
Use student marks + attendance data to identify support groups and interventions.

Input file:
- `../m365_lab_assets/class_performance_sample.csv`

Prompt:
```text
Analyze the uploaded CSV and segment students into:
- High risk
- Moderate risk
- On track

Define your own transparent rules using attendance and score indicators.
Then provide:
1) Segment-wise intervention plan
2) 2-week remediation micro-plan
3) Faculty message template for each segment

Keep recommendations realistic for one faculty + two TAs.
```

Follow-up prompt:
```text
Give the same output in a format I can paste into Excel: plain tables with short columns.
```

Expected output:
- Risk segmentation logic
- Immediate, operational remedial action plan

## Step 3 - Communication Drafting (10 min)

Goal:
Draft clear and professional responses for students, parents, and TA team.

Input file:
- `../m365_lab_assets/student_email_threads.txt`

Prompt:
```text
From the uploaded thread snippets, draft:
1) One student-facing response email
2) One parent-facing response email
3) One TA internal instruction message

Requirements:
- Tone: supportive, accountable, non-defensive.
- Include concrete next steps and timeline.
- Keep each message under 180 words.
```

Follow-up prompt:
```text
Now produce a bilingual-friendly version with simpler English and short bullet points suitable for first-year students.
```

Expected output:
- Fast communication pack for common faculty situations

## Step 4 - Assignment, Rubric, and Viva Pack (15 min)

Goal:
Convert an unstructured mini-project brief into classroom-ready assets.

Input file:
- `../m365_lab_assets/assignment_brief_raw.md`

Prompt:
```text
Using the uploaded mini-project brief, generate three artifacts:
1) Student-facing assignment brief (clear, concise, no ambiguity)
2) TA grading rubric out of 100 with criterion descriptions and performance levels
3) Viva question bank with 10 questions ordered from easy to challenging

Constraints:
- Python first-semester level
- Include plagiarism warning and acceptable collaboration policy
- Keep rubric usable by multiple TAs consistently
```

Follow-up prompt:
```text
Add a one-page grading sheet format that TAs can fill during demo day.
```

Expected output:
- A complete assessment pack that normally takes hours to draft manually

## Step 5 - Accreditation Evidence Support (12 min)

Goal:
Prepare CO-PO evidence narrative in audit-ready format.

Input file:
- `../m365_lab_assets/accreditation_mapping_template.md`

Prompt:
```text
Use the uploaded CO-PO template and produce:
1) A concise narrative justifying the CO-PO mapping
2) Evidence collection checklist with owners and frequency
3) Gaps/risk list before accreditation review

Constraints:
- Keep wording formal and audit-friendly.
- Avoid generic statements; refer to specific evidence items.
```

Follow-up prompt:
```text
Rewrite as a 5-minute speaking brief for HoD review meeting.
```

Expected output:
- Practical accreditation documentation starter

## Step 6 - Meeting Notes to Action Tracker (10 min)

Goal:
Convert raw meeting notes into structured work items.

Input file:
- `../m365_lab_assets/faculty_meeting_notes_raw.txt`

Prompt:
```text
Transform these faculty meeting notes into:
1) Action register with owner, due date, dependency, priority
2) Risks and mitigation table
3) Weekly status email template for HoD

Assume today is 2026-06-11.
Use realistic due dates over the next 3 weeks.
```

Follow-up prompt:
```text
Provide a compact version suitable for Teams channel posting.
```

Expected output:
- Execution-ready action tracker from messy notes

## Prompting Pattern to Reuse

Use this 5-part pattern for reliable output quality:

1. Role: who Copilot should act as
2. Context: class, semester, constraints
3. Artifact: exact deliverable format
4. Rules: constraints, tone, length
5. Revision: one focused follow-up to refine

Template:
```text
Role:
Context:
Artifact required:
Constraints:
Output format:
Then revise for:
```

## Trial-License Safe Fallbacks

If in-app Copilot is not available:
- Run every scenario in Copilot Chat.
- Copy generated outputs into Word, Excel, PowerPoint, or Outlook manually.
- Use Chat for iteration, then finalize in your preferred app.

If file upload is restricted in your tenant:
- Paste small file content directly into Chat.
- For CSV, paste first 15 to 30 rows and specify that it is a sample.

## Time Saved (Typical)

- Weekly planning: 45 min -> 12 min
- Remediation draft from data: 60 min -> 15 min
- Communication drafting: 30 min -> 10 min
- Rubric + viva preparation: 120 min -> 20 min
- Meeting minutes to action tracker: 40 min -> 10 min

Estimated total saving per faculty per cycle: 3 to 4 hours

## Extension Activities (Optional)

If full Microsoft 365 Copilot in apps is enabled, repeat one scenario each in:
- Word: convert plan into polished handbook format
- Excel: convert risk segmentation into formulas and charts
- PowerPoint: generate a 6-slide faculty review deck
- Outlook: send one-click polished communication draft

The core lab remains complete even without these optional steps.
