REPRODUCTION_PROMPT = """
You are an expert ML engineer.

Your goal is to determine how a research paper
should be implemented in the provided repository.

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
TASKS
================================================

1. Summarize the paper.

2. Identify repository files likely requiring changes.

3. Describe implementation tasks.

4. Describe training pipeline changes.

5. Describe evaluation changes.

6. Define benchmark tasks.

7. Define success criteria.

8. Identify engineering risks.

================================================
OUTPUT FORMAT
================================================

PAPER_SUMMARY:
...

REPOSITORY_TARGETS:
- ...

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