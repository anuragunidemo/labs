"""Simple LangChain-based faculty lab scenario.

This file shows a very small orchestration flow for an engineering-college faculty
workshop in India. It uses LangChain to connect prompt templates to an LLM and
turn a few teaching tasks into a simple, repeatable workflow.

What LangChain does here:
- It structures prompts with clear instructions.
- It connects those prompts to an LLM through a chain.
- It lets us run dependent tasks (lecture -> quiz -> feedback plan) in a workflow.
- It makes the lab easy to extend later with memory, tools, or multi-step agents.
"""

import os
import warnings

warnings.filterwarnings(
    "ignore",
    message=r"Core Pydantic V1 functionality isn't compatible with Python 3\.14 or greater\.",
    category=UserWarning,
)

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()


def build_llm():
    """Create a chat model using the same OPENAPI_* settings as 1_llmapiexample.py."""
    return ChatOpenAI(
        base_url=os.getenv("OPENAPI_BASE_URL", "http://127.0.0.1:8765/v1"),
        api_key=os.getenv("OPENAPI_API_KEY", "test-key"),
        model=os.getenv("OPENAPI_MODEL", "mock-model"),
        temperature=0.2,
    )


def build_chains(llm):
    """Create simple LangChain chains for the three dependent faculty tasks."""

    # Why use LangChain here:
    # - Prompt templates keep instructions consistent and reusable across tasks.
    # - Chain composition (prompt -> model -> parser) keeps orchestration readable.
    # - It is easy to extend later with memory, tools, retries, and tracing.
    # If not using LangChain, build plain helper functions that:
    # 1) format prompt strings manually,
    # 2) call the chat-completions API directly, and
    # 3) normalize/validate text output for each step.

    # TODO 1: Replace the sample topic with your own subject area.
    lecture_prompt = ChatPromptTemplate.from_template(
        "You are a faculty assistant for an engineering college in India. "
        "Create a 60-minute lecture plan on {topic} for {course_level} students. "
        "Include: learning objectives, key concepts, classroom activities, "
        "examples, and a short recap. Keep the language practical and easy to use."
    )

    # TODO 2: Choose the Bloom's taxonomy levels you want students to practice.
    quiz_prompt = ChatPromptTemplate.from_template(
        "You are helping a faculty member prepare assessment material. "
        "Based on the lecture plan below, create 5 short quiz questions for {topic}. "
        "Use Bloom's taxonomy levels such as Remember, Understand, Apply, Analyze. "
        "Also create a simple assignment rubric with 4 criteria and 3 performance levels. "
        "Lecture plan:\n{lecture_plan}"
    )

    # TODO 3: Customize remediation strategies to your department context.
    feedback_prompt = ChatPromptTemplate.from_template(
        "You are an academic coordinator in an engineering college in India. "
        "Using the lecture plan and quiz+rubric below, create a post-class action plan for {topic}. "
        "Include: common misconceptions likely from the quiz, targeted remediation activities, "
        "one homework task mapped to Bloom's levels, and a 15-minute next-class bridge plan. "
        "Keep it practical for second/third-year B.Tech classrooms. "
        "Lecture plan:\n{lecture_plan}\n\n"
        "Quiz and rubric:\n{quiz_output}"
    )

    # LangChain chains: prompt -> model -> text output
    lecture_chain = lecture_prompt | llm | StrOutputParser()
    quiz_chain = quiz_prompt | llm | StrOutputParser()
    feedback_chain = feedback_prompt | llm | StrOutputParser()

    return {
        "lecture": lecture_chain,
        "quiz": quiz_chain,
        "feedback": feedback_chain,
    }


def run_lab(topic="Data Structures", course_level="third-year B.Tech"):
    """Run a three-step dependent faculty workflow with LangChain chains."""
    llm = build_llm()
    chains = build_chains(llm)

    # With LangChain, each task is a small, testable chain invoked with inputs.
    # Without LangChain, execute these same steps with direct API calls and
    # keep a shared context object/dict to pass outputs between steps.

    print("Starting workflow...")

    # Step 1: Lecture plan
    print("[1/3] Building lecture plan...")
    lecture_plan = chains["lecture"].invoke(
        {"topic": topic, "course_level": course_level}
    )
    print("[1/3] Lecture plan ready.")

    # Step 2: Quiz + rubric
    print("[2/3] Building quiz and rubric...")
    quiz_output = chains["quiz"].invoke(
        {"topic": topic, "lecture_plan": lecture_plan}
    )
    print("[2/3] Quiz and rubric ready.")

    # Step 3: Post-class feedback and remediation plan (depends on Steps 1 and 2)
    print("[3/3] Building remediation plan...")
    feedback_output = chains["feedback"].invoke(
        {
            "topic": topic,
            "lecture_plan": lecture_plan,
            "quiz_output": quiz_output,
        }
    )
    print("[3/3] Remediation plan ready.")

    return {
        "topic": topic,
        "course_level": course_level,
        "lecture_plan": lecture_plan,
        "quiz_and_rubric": quiz_output,
        "post_class_feedback_and_remediation_plan": feedback_output,
    }


def preview_text(text, max_lines=8):
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    return "\n".join(lines[:max_lines]) + "\n..."


if __name__ == "__main__":
    # TODO 4: Try different subjects such as Embedded Systems, DBMS, or AI/ML.
    result = run_lab(topic="Linked Lists", course_level="second-year B.Tech")

    print("=== Faculty Lab Output ===")
    print("\n1. Lecture Plan (preview)\n")
    print(preview_text(result["lecture_plan"]))

    print("\n2. Quiz and Rubric (preview)\n")
    print(preview_text(result["quiz_and_rubric"]))

    print("\n3. Post-Class Feedback and Remediation Plan (preview)\n")
    print(preview_text(result["post_class_feedback_and_remediation_plan"]))
