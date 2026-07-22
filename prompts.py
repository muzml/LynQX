# Prompt configurations for LynQX test generation
SCENARIO_GENERATION_PROMPT = """As a Test Scenario Generator, analyze these user stories and generate comprehensive test scenarios.
Include positive test scenarios, negative test scenarios, and edge cases.
- scenario_id: A unique identifier (TS001, TS002, etc.)
- scenario_name: A descriptive name
- scenario_type: "Positive", "Negative", or "Edge case"
- description: Detailed description of the scenario
- related_user_story: The ID or brief description of the related user story
- status: "Pending Review"
User Stories:
{user_stories}
Format: TestCaseID: Description — Expected Result
"""
