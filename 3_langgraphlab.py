"""LangGraph-based faculty lab scenario.

This file runs the same three-step faculty workflow as 2_langchainlab.py
(lecture plan → quiz+rubric → remediation) but uses LangGraph instead of
LangChain LCEL chains.

WHY THIS FILE EXISTS
Compare the two side-by-side to understand when to use each approach.

LANGCHAIN LCEL (2_langchainlab.py)          LANGGRAPH (this file)
─────────────────────────────────────────────────────────────────────────
Chains composed with |  (prompt | llm)      Nodes + typed state + edges
Linear flow only                            Supports branching and cycles
State passed as Python variables manually   State is a shared TypedDict
                                            merged automatically per node
Simple to read for short pipelines          Better for agents and
                                            multi-step conditional flows
No built-in retries or human-in-the-loop    First-class interrupt/retry
                                            support via interrupt_before
─────────────────────────────────────────────────────────────────────────

The prompts and LLM settings are identical to 2_langchainlab.py.
Only the orchestration layer changes.
"""

import os
import warnings

warnings.filterwarnings(
    "ignore",
    message=r"Core Pydantic V1 functionality isn't compatible with Python 3\.14 or greater\.",
    category=UserWarning,
)

from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

load_dotenv()


# ── Shared state ──────────────────────────────────────────────────────────────
# LangGraph passes this dict between every node automatically.
# Each node returns only the keys it updates; the rest are preserved.
# In LCEL you would pass variables manually between chain calls.

class FacultyState(TypedDict):
    topic: str
    course_level: str
    lecture_plan: str
    quiz_and_rubric: str
    feedback_plan: str


# ── LLM setup ────────────────────────────────────────────────────────────────

def build_llm():
    """Create a chat model using the same OPENAPI_* settings as 1_llmapiexample.py."""
    return ChatOpenAI(
        base_url=os.getenv("OPENAPI_BASE_URL", "http://127.0.0.1:8765/v1"),
        api_key=os.getenv("OPENAPI_API_KEY", "test-key"),
        model=os.getenv("OPENAPI_MODEL", "mock-model"),
        temperature=0.2,
    )


# ── Nodes ─────────────────────────────────────────────────────────────────────
# Each node is a plain function.  It receives the full state dict and returns
# a partial dict with only the keys it wants to update.
# In LCEL you would write:  lecture_chain = prompt | llm | StrOutputParser()
# Here the same logic lives inside a function body instead.

def lecture_node(state: FacultyState) -> dict:
    print("[1/3] Building lecture plan...")
    llm = build_llm()
    prompt = (
        "You are a faculty assistant for an engineering college in India. "
        f"Create a 60-minute lecture plan on {state['topic']} for "
        f"{state['course_level']} students. "
        "Include: learning objectives, key concepts, classroom activities, "
        "examples, and a short recap. Keep the language practical and easy to use."
    )
    # TODO 1: Replace the sample topic/level by passing different inputs to run_lab().
    result = llm.invoke(prompt).content
    print("[1/3] Lecture plan ready.")
    return {"lecture_plan": result}


def quiz_node(state: FacultyState) -> dict:
    print("[2/3] Building quiz and rubric...")
    llm = build_llm()
    prompt = (
        "You are helping a faculty member prepare assessment material. "
        f"Based on the lecture plan below, create 5 short quiz questions for {state['topic']}. "
        "Use Bloom's taxonomy levels such as Remember, Understand, Apply, Analyze. "
        "Also create a simple assignment rubric with 4 criteria and 3 performance levels.\n"
        # TODO 2: Adjust Bloom's levels or number of questions here.
        f"Lecture plan:\n{state['lecture_plan']}"
    )
    result = llm.invoke(prompt).content
    print("[2/3] Quiz and rubric ready.")
    return {"quiz_and_rubric": result}


def feedback_node(state: FacultyState) -> dict:
    print("[3/3] Building remediation plan...")
    llm = build_llm()
    prompt = (
        "You are an academic coordinator in an engineering college in India. "
        f"Using the lecture plan and quiz+rubric below, create a post-class action plan for {state['topic']}. "
        "Include: common misconceptions likely from the quiz, targeted remediation activities, "
        "one homework task mapped to Bloom's levels, and a 15-minute next-class bridge plan. "
        "Keep it practical for second/third-year B.Tech classrooms.\n"
        # TODO 3: Customize the remediation strategies for your department.
        f"Lecture plan:\n{state['lecture_plan']}\n\n"
        f"Quiz and rubric:\n{state['quiz_and_rubric']}"
    )
    result = llm.invoke(prompt).content
    print("[3/3] Remediation plan ready.")
    return {"feedback_plan": result}


# ── Graph assembly ────────────────────────────────────────────────────────────
# This is the part that has no equivalent in LCEL.
# Nodes are registered, then connected with edges.
# You could later add conditional edges here without touching the node functions.
# Example extension:
#   graph.add_conditional_edges(
#       "quiz",
#       lambda state: "feedback" if len(state["quiz_and_rubric"]) > 100 else "quiz",
#   )

def build_graph():
    graph = StateGraph(FacultyState)

    graph.add_node("lecture", lecture_node)
    graph.add_node("quiz", quiz_node)
    graph.add_node("feedback", feedback_node)

    graph.set_entry_point("lecture")
    graph.add_edge("lecture", "quiz")
    graph.add_edge("quiz", "feedback")
    graph.add_edge("feedback", END)

    return graph.compile()


# ── Run ───────────────────────────────────────────────────────────────────────

def run_lab(topic="Data Structures", course_level="third-year B.Tech"):
    """Run the three-step faculty workflow using LangGraph."""
    app = build_graph()

    print("Starting LangGraph workflow...")
    final_state = app.invoke({
        "topic": topic,
        "course_level": course_level,
        "lecture_plan": "",
        "quiz_and_rubric": "",
        "feedback_plan": "",
    })

    return {
        "topic": final_state["topic"],
        "course_level": final_state["course_level"],
        "lecture_plan": final_state["lecture_plan"],
        "quiz_and_rubric": final_state["quiz_and_rubric"],
        "post_class_feedback_and_remediation_plan": final_state["feedback_plan"],
    }


def preview_text(text, max_lines=8):
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    return "\n".join(lines[:max_lines]) + "\n..."


if __name__ == "__main__":
    # TODO 4: Try different subjects such as Embedded Systems, DBMS, or AI/ML.
    result = run_lab(topic="Linked Lists", course_level="second-year B.Tech")

    sep = "-" * 60
    print("\n=== LangGraph Faculty Lab Output ===")

    print(f"\n{sep}")
    print("1. Lecture Plan (preview)")
    print(sep)
    print(preview_text(result["lecture_plan"]))

    print(f"\n{sep}")
    print("2. Quiz and Rubric (preview)")
    print(sep)
    print(preview_text(result["quiz_and_rubric"]))

    print(f"\n{sep}")
    print("3. Post-Class Feedback and Remediation Plan (preview)")
    print(sep)
    print(preview_text(result["post_class_feedback_and_remediation_plan"]))

    print("\n" + "=" * 60)
    print("KEY DIFFERENCE vs 2_langchainlab.py")
    print("=" * 60)
    print(
        "LCEL (2_langchainlab.py) — chains with |, linear only\n"
        "LangGraph (this file)    — nodes + state graph, supports\n"
        "                           branching, cycles, and retries\n"
        "Same prompts. Same LLM. Different orchestration layer."
    )
    print("=" * 60)
