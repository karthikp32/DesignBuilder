class Prompts:
    """
    Prompts for the DesignBuilder project.
    """

    @staticmethod
    def get_design_doc_extraction_prompt(full_text: str) -> str:
        return f"""You are an expert system architect. Extract all architectural components from the following system design document(s).

    For each component, provide:
    - name: the component's name
    - description: a detailed summary of its responsibilities, behavior, and role in the system
    - language: the main programming language or technology used

    Example:

    - name: UserService
    description: Manages user accounts including registration, authentication, profile updates, and account deletion. Ensures secure password storage and validation, and interfaces with notification and analytics subsystems.
    language: Python

    - name: PaymentGateway
    description: Handles all payment processing including credit card transactions, refunds, and recurring billing. Integrates with external payment providers and logs all transactions for auditing purposes.
    language: null

    Now extract components from the document below:

    {full_text}

    Return only a valid YAML list with keys: name, description, and language. Each description should be detailed and informative.

        """

    def get_unified_plan_prompt(components_desc_yaml) -> str:
        return f"""
    You are a senior software engineer planning implementations for multiple components.

    Each component has name and description.

    For each, provide:
    - purpose
    - key sub_tasks
    - dependencies
    - edge_cases
    - complexity (Low/Medium/High)

    Return **YAML list**:
    - name: <component name>
    plan:
        purpose: ...
        sub_tasks: [...]
        dependencies: [...]
        edge_cases: [...]
        complexity: Low/Medium/High

    Components:
    {components_desc_yaml}
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
    def get_implement_prompt(plan: str) -> str:
        return f"""Implement the following component in Python based on this plan:
    {plan}

    Requirements:
    - Follow the plan exactly.
    - Use clear, production-quality code.
    - Include necessary imports and helper functions.
    - Return only valid Python code (no markdown, comments, or explanations).
    - Write elegant, efficient, and maintainable code using a minimalist approach.
    """

    @staticmethod
    def get_write_tests_prompt(implementation: str, component: str) -> str:
        return f"""
    You are an experienced Python developer.

    Write comprehensive unit tests for the component given this implementation:
    {implementation}

    Requirements:
    - Use pytest style.
    - Cover normal, edge, and failure cases. 
    - Keep tests elegant, minimal, and focused on verifying correctness and robustness.
    - Include setup and teardown if necessary.
    - Return only valid Python test code with no markdown, comments, or explanations.
    """

    @staticmethod
    def get_debug_prompt(implementation: str, test_summary: str) -> str:
        return f"""The following Python implementation failed its tests:

    {implementation}

    Test failure summary:
    {test_summary}

    Perform a root cause analysis to identify why the failures occurred. 
    Use a scientific method mindset: hypothesize, reason through likely causes, and apply only necessary fixes.
    Revise the implementation to produce an elegant, minimalist, and correct solution.

    Return only the corrected Python code with no markdown, comments, or explanations.
    """

    @staticmethod
    def get_guide_prompt(guidance: str, implementation: str) -> str:
        return f"""The user has provided the following guidance:

    {guidance}

    The current code is:

    {implementation}

    Please incorporate this guidance to fix the code. Return only the corrected Python code without any explanations or markdown formatting."""