BLUEPRINT_PROMPT = """
You are a senior software architect.

Your job is to convert a research
reproduction plan into a concrete
engineering implementation blueprint.

You MUST use ONLY the provided
repository symbols.

Do NOT invent files.

Do NOT invent symbols.

Do NOT invent services.

Every blueprint step MUST reference
a modification target provided below.

================================================
QUESTION
================================================

{question}

================================================
PAPER SUMMARY
================================================

{paper_summary}

================================================
MODIFICATION TARGETS
================================================

{modification_targets}

================================================
GAP TO SYMBOL MAPPING
================================================

{gap_to_symbol_mapping}

================================================
TASK
================================================

For each modification target:

1. Identify the repository file.

2. Identify the repository symbol.

3. Determine whether the change is:
   - add
   - modify
   - replace

4. Explain WHY the change is needed.

5. Describe implementation steps.

6. Describe validation steps.

7. Describe the expected outcome.

================================================
OUTPUT RULES
================================================

Return ONLY valid JSON.

Do NOT include markdown.

Do NOT include explanations.

Do NOT wrap JSON in code fences.

================================================
OUTPUT SCHEMA
================================================

{{
  "blueprint_steps": [
    {{
      "file_path": "string",
      "symbol_name": "string",
      "change_type": "add | modify | replace",
      "reason": "string",
      "implementation_steps": [
        "string"
      ],
      "validation_steps": [
        "string"
      ],
      "expected_outcome": "string"
    }}
  ]
}}
"""