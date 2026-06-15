"""DBMS chatbot lab script using Microsoft Agent Framework.

This file is intentionally simple for classroom use.
It asks the end user for a DBMS topic focus, runs a terminal chatbot,
and prints two evaluation scores after chat ends.
"""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import (
    Agent,
    FunctionInvocationContext,
    InMemoryHistoryProvider,
    LocalEvaluator,
    evaluate_agent,
    keyword_check,
    tool_called_check,
    tool,
)
from agent_framework.openai import OpenAIChatClient

load_dotenv()


FACULTY_MEMORY_KEY = "faculty_profile"


# TODO 2: Tooling task for students.
# Uncomment both tool function blocks below when you are ready to enable tool calling.
#
# @tool(name="save_faculty_context", description="Store one faculty preference in session memory.")
# def save_faculty_context(
#     context: FunctionInvocationContext,
#     subject: str,
#     class_level: str,
# ) -> str:
#     profile = context.session.state.setdefault(FACULTY_MEMORY_KEY, {})
#     profile["subject"] = subject.strip()
#     profile["class_level"] = class_level.strip()
#     return (
#         "Saved faculty context: "
#         f"subject={profile['subject']}, class_level={profile['class_level']}, "
#         "teaching_style=not-set"
#     )
#
#
# @tool(name="suggest_classroom_activity", description="Suggest a short classroom activity for a faculty topic.")
# def suggest_classroom_activity(topic: str) -> str:
#     topic = topic.strip()
#     if not topic:
#         return "Please provide a topic so I can suggest an activity."
#
#     lowered_topic = topic.lower()
#     if "dbms" in lowered_topic or "database" in lowered_topic:
#         return (
#             "Use a quick board exercise: students identify entities, primary keys, and relationships, "
#             "then compare the ER design with a normalized table layout."
#         )
#
#     if "sql" in lowered_topic:
#         return (
#             "Use a live SQL drill: give one SELECT query, one JOIN query, and one GROUP BY query, "
#             "then ask students to explain the output before running it."
#         )
#
#     return (
#         f"Use a think-pair-share activity on {topic}: ask for a one-sentence answer, "
#         "then compare it with a worked example."
#     )


def build_agent(topic_focus: str) -> Agent:
    client = OpenAIChatClient(
        base_url=os.getenv("OPENAPI_BASE_URL", "http://127.0.0.1:8765/v1"),
        api_key=os.getenv("OPENAPI_API_KEY", "test-key"),
        model=os.getenv("OPENAPI_MODEL", "mock-model"),
    )

    instructions = (
        "You are a helpful faculty assistant for a DBMS course. "
        # TODO 1: Uncomment all lines below to improve instruction quality.
        # f"The current topic focus from the end user is: {topic_focus}. "
        # "Keep answers short and practical. "
        # "Use the tools when the user asks to save context or suggest an activity. "
        # "Prefer examples about SQL, normalization, ER diagrams, and transactions."
    )

    return Agent(
        client=client,
        name="faculty-chatbot",
        instructions=instructions,
        # TODO 2: Uncomment the next line to wire tool calling into the agent.
        # tools=[save_faculty_context, suggest_classroom_activity],
        tools=[],
        context_providers=[InMemoryHistoryProvider()],
    )


def _topic_keywords(topic_focus: str) -> list[str]:
    base_words = [part for part in topic_focus.lower().split() if part]
    normalized_words: list[str] = []

    for word in base_words:
        if word.endswith("es") and len(word) > 3:
            normalized_words.append(word[:-2])
        elif word.endswith("s") and len(word) > 2:
            normalized_words.append(word[:-1])
        else:
            normalized_words.append(word)

    # Keep order stable while removing duplicates.
    return list(dict.fromkeys(normalized_words))


async def run_evaluation_demo(user_prompt: str, response, topic_focus: str) -> None:
    print("Evaluation source:")
    print(f"- Topic focus: {topic_focus}")
    print(f"- User prompt: {user_prompt}")
    print("Bot answer:")
    print(response.text)

    # TODO 4: Evaluator task for students.
    # Uncomment the full block below to enable built-in evaluators.
    # topic_words = _topic_keywords(topic_focus)
    # if not topic_words:
    #     topic_words = ["database"]
    #
    # checks = []
    # for topic_word in topic_words:
    #     checks.append(keyword_check(topic_word))
    #
    # # Add a built-in tool-call evaluator to verify at least one expected tool was used.
    # checks.append(tool_called_check("save_faculty_context", "suggest_classroom_activity", mode="any"))
    #
    # evaluator = LocalEvaluator(*checks)
    # eval_results = await evaluate_agent(
    #     queries=user_prompt,
    #     responses=response,
    #     evaluators=evaluator,
    #     eval_name="single-prompt-local-eval",
    #     context=f"Topic focus: {topic_focus}; Prompt: {user_prompt}",
    # )
    #
    # result = eval_results[0]
    # counts = result.result_counts
    # print("Built-in evaluator summary:")
    # print(f"- Passed items: {counts.get('passed', 0)}")
    # print(f"- Failed items: {counts.get('failed', 0)}")
    # print(f"- Errored items: {counts.get('errored', 0)}")
    #
    # if result.items:
    #     item = result.items[0]
    #     for score in item.scores:
    #         status = "pass" if score.passed else "fail"
    #         reason = ""
    #         if score.sample and isinstance(score.sample, dict):
    #             reason = score.sample.get("reason", "")
    #         if reason:
    #             print(f"- {score.name}: {status} ({reason})")
    #         else:
    #             print(f"- {score.name}: {status}")

    print("TODO 4 pending: evaluator block is commented. Uncomment it to run built-in evaluators.")


async def run_chatbot() -> None:
    topic_focus = input("Enter your DBMS topic focus (for example, normalization, indexing, joins): ").strip()
    if not topic_focus:
        topic_focus = "normalization"

    class_level = input(
        "Enter your class level (for example, first-year BCA, second-year CSE, third-year IT, final-year AI-ML): "
    ).strip() or "second-year CSE"

    agent = build_agent(topic_focus)
    session = agent.create_session()

    # TODO 3: Memory task for students.
    # Uncomment the full block below to save faculty context into session memory.
    # This should call the save_faculty_context tool and persist class metadata.
    # await agent.run(
    #     (
    #         # TODO 3: This prompt writes memory using the save_faculty_context tool.
    #         "Save faculty context with "
    #         f"subject=DBMS ({topic_focus}), class_level={class_level}."
    #     ),
    #     session=session,
    # )

    print("\nFaculty chatbot ready.")
    print(f"Current DBMS focus: {topic_focus}")
    print("Enter one prompt for the bot.\n")

    user_message = input("You: ").strip()
    if not user_message:
        print("No prompt entered. Exiting.")
        return

    response = await agent.run(user_message, session=session)
    print(f"Bot: {response.text}\n")

    # TODO 4: Uncomment the next two lines to run built-in evaluators.
    # print("Running evaluation on the same response...")
    # await run_evaluation_demo(user_message, response, topic_focus)


def main() -> None:
    asyncio.run(run_chatbot())


if __name__ == "__main__":
    main()
