class Prompts:
    """
    Prompts for the DesignBuilder project.
    """
    @staticmethod
    def get_plan_prompt(description: str) -> str:
        return f"""
    You are a senior software engineer planning the implementation of a code component.

    Goal: Generate a concise, actionable plan to implement the component described below.

    Component description:
    {description}

    Include:
    1. Purpose and expected behavior (1–2 sentences)
    2. Key sub-tasks or functions to implement (ordered list)
    3. Dependencies or external modules required
    4. Edge cases or testing considerations
    5. Estimated complexity (Low / Medium / High)

    Constraints:
    - Do not write code.
    - Be concise and technical.
    - Use bullet points or numbered steps only.
    """
    @staticmethod
    def get_write_tests_prompt(description: str) -> str:
        return f"""
    You are an experienced Python developer.

    Write comprehensive unit tests for the following component:
    {description}

    Requirements:
    - Use pytest style.
    - Cover normal, edge, and error cases.
    - Include setup and teardown if applicable.
    - Return only valid Python test code, with no comments, explanations, or markdown formatting.
    """

    @staticmethod
    def get_implement_prompt(plan: str) -> str:
        return f"""Implement the following component in Python based on this plan:
    {plan}

    Requirements:
    - Follow the plan exactly.
    - Use clear, production-quality code.
    - Include necessary imports and helper functions.
    - Return only valid Python code (no markdown, comments, or explanations).
    """

    @staticmethod
    def get_debug_prompt(implementation: str, test_summary: str) -> str:
        return f"""The following Python implementation failed its tests:

    {implementation}

    Test failure summary:
    {test_summary}

    Analyze the root cause of the failures, determine what is wrong, and fix the code following a scientific method approach (hypothesize, experiment, conclude). Return only the corrected Python code, without explanations, comments, or markdown formatting.
    """

    @staticmethod
    def get_guide_prompt(guidance: str, implementation: str) -> str:
        return f"""The user has provided the following guidance:

    {guidance}

    The current code is:

    {implementation}

    Please incorporate this guidance to fix the code. Return only the corrected Python code without any explanations or markdown formatting."""