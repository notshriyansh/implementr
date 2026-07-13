REPRODUCTION_PROMPT = """
You are a senior ML engineer and research engineer.

Your task is to determine how a research paper
can be reproduced inside the provided repository.

You MUST use the provided repository context.

Do NOT invent files, services, training pipelines,
symbols, architectures, or infrastructure that
do not exist in the provided repository context.

If repository evidence is insufficient,
explicitly state:

Repository context insufficient.

================================================
QUESTION
================================================

{question}

================================================
PAPER CONTEXT
================================================

{paper_context}

================================================
REPOSITORY CONTEXT
================================================

{repository_context}

================================================
ARCHITECTURE CONTEXT
================================================

{architecture_context}

================================================
RELEVANT SYMBOLS
================================================

{symbols_context}

================================================
PAPER CONCEPTS
================================================

{paper_concepts}

================================================
REPOSITORY CONCEPTS
================================================

{repo_concepts}

================================================
CONCEPT MAPPINGS
================================================

{concept_mappings}

================================================
ARCHITECTURE GAPS
================================================

{architecture_gaps}

================================================
TASKS
================================================

1. Summarize the paper.

2. Identify repository files likely requiring changes.

3. Identify concept mappings between the paper
   and repository.

4. Identify architecture gaps.

5. Describe implementation tasks.

6. Describe training pipeline changes.

7. Describe evaluation changes.

8. Define benchmark tasks.

9. Define success criteria.

10. Identify engineering risks.

11. Identify exact repository symbols that
    should be modified.

Rules:

- Use ONLY symbols listed in RELEVANT SYMBOLS.
- Do NOT invent symbol names.
- Every modification target MUST reference
  a symbol from RELEVANT SYMBOLS.
- Only include symbols that are directly
  involved in reproducing the paper.
- Do NOT include utility functions,
  helper methods, logging functions,
  built-in functions, or unrelated symbols.
- If no valid symbol exists, return:
  Repository context insufficient.

12. For each modification target provide:
    - Symbol name
    - File path
    - Reason for modification

13. Map architecture gaps to the repository
    symbols that would address those gaps.

================================================
OUTPUT FORMAT
================================================

PAPER_SUMMARY:
...

REPOSITORY_TARGETS:
- ...

CONCEPT_MAPPINGS:
- ...

ARCHITECTURE_GAPS:
- ...

IMPLEMENTATION_STEPS:
- ...

MODIFICATION_TARGETS:

- SYMBOL: <symbol name>
  FILE: <file path>
  REASON: <why this symbol must change>

- SYMBOL: <symbol name>
  FILE: <file path>
  REASON: <why this symbol must change>

GAP_TO_SYMBOL_MAPPING:

- GAP: <architecture gap>
  SYMBOL: <symbol name>

- GAP: <architecture gap>
  SYMBOL: <symbol name>

REQUIRED_CHANGES:
- ...

TRAINING_CHANGES:
- ...

EVALUATION_CHANGES:
- ...

BENCHMARK_TASKS:
- ...

SUCCESS_CRITERIA:
- ...

RISKS:
- ...
"""