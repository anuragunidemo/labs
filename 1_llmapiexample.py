import os

import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load values from the local .env file (copy .env.example to .env for your own settings).
load_dotenv()


class OpenApiSdkClient:
    """Use the SDK when you want cleaner code and easier maintenance.

    Advantages:
    - simpler syntax for chat completions
    - typed client objects and built-in helpers
    - easier to evolve as the API grows
    """

    def __init__(self, base_url=None, api_key=None, model=None):
        # Set your Foundry endpoint here in .env: OPENAPI_BASE_URL
        # Example: https://<resource-name>.openai.azure.com/openai/deployments/<deployment-name>
        self.base_url = base_url or os.getenv("OPENAPI_BASE_URL", "http://127.0.0.1:8765/v1")

        # Set your Foundry API key in .env: OPENAPI_API_KEY
        self.api_key = api_key or os.getenv("OPENAPI_API_KEY", "test-key")

        # Set your deployed model name in .env: OPENAPI_MODEL
        self.model = model or os.getenv("OPENAPI_MODEL", "mock-model")

    def ask(self, question, temperature=0.2):
        client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": question}],
            temperature=temperature,
        )
        return response.choices[0].message.content

    def ask_with_system_prompt(self, system_prompt, user_message):
        client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content


class OpenApiRawClient:
    """Use raw HTTP when you need full control over the request.

    Advantages:
    - complete control of headers, payload, and retries
    - no SDK dependency
    - useful for debugging or custom integrations
    """

    def __init__(self, base_url=None, api_key=None, model=None):
        # The raw client uses the same endpoint configured in .env: OPENAPI_BASE_URL
        self.base_url = base_url or os.getenv("OPENAPI_BASE_URL", "http://127.0.0.1:8765/v1")

        # The API key comes from .env: OPENAPI_API_KEY
        self.api_key = api_key or os.getenv("OPENAPI_API_KEY", "test-key")

        # The model/deployment name comes from .env: OPENAPI_MODEL
        self.model = model or os.getenv("OPENAPI_MODEL", "mock-model")

    def ask(self, question):
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.2,
        }
        response = requests.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
def main():
    # Same question asked in three different ways to show system prompt impact.
    question = "What is a primary key in a database?"

    # Without a system prompt the model picks its own style and length.
    sdk_client = OpenApiSdkClient()
    raw_client = OpenApiRawClient()

    sep = "-" * 60

    print(sep)
    print("EXAMPLE 1 | SDK client | no system prompt")
    print("           (model chooses its own style and length)")
    print(sep)
    print(sdk_client.ask(question))

    print("\n" + sep)
    print("EXAMPLE 2 | Raw HTTP client | no system prompt")
    print("           (same question, full manual control over request)")
    print(sep)
    print(raw_client.ask(question))

    # With a system prompt we lock the persona, audience, and format.
    # Notice how the *same* user question produces a very different answer below.
    system_prompt_beginner = (
        "You are a patient tutor explaining database concepts to first-year students. "
        "Use a simple real-world analogy, avoid jargon, and keep the answer to two sentences."
    )
    print("\n" + sep)
    print("EXAMPLE 3 | SDK client | system prompt: first-year student tutor")
    print(f"           System prompt: \"{system_prompt_beginner}\"")
    print(sep)
    print(sdk_client.ask_with_system_prompt(system_prompt_beginner, question))

    system_prompt_expert = (
        "You are a senior database engineer reviewing design decisions with your team. "
        "Be precise and technical. Mention constraints, uniqueness, and indexing in one short paragraph."
    )
    print("\n" + sep)
    print("EXAMPLE 4 | SDK client | system prompt: senior engineer reviewer")
    print(f"           System prompt: \"{system_prompt_expert}\"")
    print(sep)
    print(sdk_client.ask_with_system_prompt(system_prompt_expert, question))

    print("\n" + "=" * 60)
    print("KEY TAKEAWAY — SYSTEM PROMPT")
    print("=" * 60)
    print(
        "The user message was identical in examples 3 and 4.\n"
        "The system prompt alone changed the audience, tone,\n"
        "depth, and format of the answer."
    )
    print("=" * 60)

    # ── Temperature examples ──────────────────────────────────────
    # Temperature controls how deterministic vs. creative the model is.
    #   0.0  → near-deterministic, factual, minimal variation
    #   0.7  → balanced, some creativity, still coherent
    #   1.5  → highly creative, varied, occasionally unpredictable
    # Same question, same system prompt — only temperature changes.
    temp_question = "Give one tip to help students remember the difference between DELETE and TRUNCATE in SQL."
    temp_system   = "You are a friendly CS faculty member. Keep the answer to one or two sentences."

    for temp in [0.0, 0.7, 1.5]:
        label = {0.0: "low (0.0)  — factual, consistent",
                 0.7: "mid (0.7)  — balanced creativity",
                 1.5: "high (1.5) — creative, more varied"}[temp]
        print(f"\n{sep}")
        print(f"TEMPERATURE EXAMPLE | temperature={label}")
        print(f"           User prompt: \"{temp_question}\"")
        print(sep)
        # Instantiate a fresh client for each call so temperature is applied cleanly.
        print(OpenApiSdkClient().ask_with_system_prompt(temp_system, temp_question))
        # NOTE: run the script multiple times — high temperature answers will vary;
        # low temperature answers will stay nearly identical across runs.

    print("\n" + "=" * 60)
    print("KEY TAKEAWAY — TEMPERATURE")
    print("=" * 60)
    print(
        "Low temperature  → safe, repetitive, good for factual Q&A.\n"
        "Mid temperature  → best default for most classroom tasks.\n"
        "High temperature → creative tasks (brainstorming, stories),\n"
        "                   but may drift off-topic or repeat itself."
    )
    print("=" * 60)

if __name__ == "__main__":
    main()
