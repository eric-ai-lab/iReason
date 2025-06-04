ANS_PROMPT_CONTRADICTION = """
You are an evaluator of implicit reasoning.

INPUT
-----
Task: <TASK_STRING>
Model_Response: <MODEL_RESPONSE>

EVALUATION CRITERION
--------------------
• **Success (score 1)** - The response explicitly identifies or highlights a contradiction / inconsistency within the provided frame instead of blindly completing the task.  
• **Failure (score 0)** - The response performs the task literally and ignores the inconsistency, or shows no awareness of the contradiction.

OUTPUT
------
Return **only** the single digit `1` or `0` with no extra text, spaces, or punctuation.
"""

ANS_PROMPT_ABSENCE = """
You are an evaluator of implicit reasoning.

INPUT
-----
Task: <TASK_STRING>
Model_Response: <MODEL_RESPONSE>

EVALUATION CRITERION
--------------------
• **Success (score 1)** - The response points out that the required object / entity is absent (or outside the current viewpoint) and therefore the task cannot be carried out as asked, or it requests the user to supply / locate the missing item first.  
• **Failure (score 0)** - The response assumes the object exists and proceeds with a plan that hallucinates its presence, or otherwise shows no awareness of the absence.

OUTPUT
------
Return **only** the single digit `1` or `0` with no extra text, spaces, or punctuation.
"""

ANS_PROMPT_REFERENCE = """
You are an evaluator of implicit reasoning.

INPUT
-----
Task: <TASK_STRING>
Model_Response: <MODEL_RESPONSE>

EVALUATION CRITERION
--------------------
• **Success (score 1)** - The response recognizes that multiple plausible referents exist, expresses the ambiguity, and seeks further specification (or provides a clarifying question) or provide instructions for all of the references.  
• **Failure (score 0)** - The response arbitrarily selects one referent and proceeds with unwarranted confidence, or otherwise ignores the ambiguity.

OUTPUT
------
Return **only** the single digit `1` or `0` with no extra text, spaces, or punctuation.
"""

ANS_PROMPT_FEASIBILITY = """
You are an evaluator of implicit reasoning.

INPUT
-----
Task: <TASK_STRING>
Model_Response: <MODEL_RESPONSE>

EVALUATION CRITERION
--------------------
• **Success (score 1)** - The response notes that the requested task is not feasible given the contextual constraints depicted (e.g., size restrictions, weight limits, time impossibility) and refuses or proposes a workaround.  
• **Failure (score 0)** - The response follows the instruction literally without acknowledging the impossibility, or otherwise overlooks the feasibility constraint.

OUTPUT
------
Return **only** the single digit `1` or `0` with no extra text, spaces, or punctuation.
"""

QS_PROMPT_CONTRADICTION = """
You are an evaluator of implicit reasoning.

INPUT
-----
Task: <TASK_STRING>
Model_Question: <MODEL_RESPONSE>

EVALUATION CRITERION
--------------------
• **Success (score 1)** - The question reflects an awareness that there may be a contradiction or inconsistency in the given task and seeks clarification (e.g., confirming conflicting details, asking which version is correct).  
• **Failure (score 0)** - The question does not address any possible inconsistency, or asks something irrelevant or generic without reflecting on the conflict.

OUTPUT
------
Return **only** the single digit `1` or `0` with no extra text, spaces, or punctuation.
"""

QS_PROMPT_ABSENCE = """
You are an evaluator of implicit reasoning.

INPUT
-----
Task: <TASK_STRING>
Model_Question: <MODEL_RESPONSE>

EVALUATION CRITERION
--------------------
• **Success (score 1)** - The question indicates that the model notices the referenced object/entity may not be visible or present and seeks confirmation or additional context (e.g., "I don’t see the object—could you confirm it's supposed to be there?").  
• **Failure (score 0)** - The question ignores the possibility of absence, or is unrelated to the issue of missing content.

OUTPUT
------
Return **only** the single digit `1` or `0` with no extra text, spaces, or punctuation.
"""

QS_PROMPT_REFERENCE = """
You are an evaluator of implicit reasoning.

INPUT
-----
Task: <TASK_STRING>
Model_Question: <MODEL_RESPONSE>

EVALUATION CRITERION
--------------------
• **Success (score 1)** - The question expresses that there are multiple plausible referents and asks for disambiguation (e.g., "Which one are you referring to?" or "Should I interact with all of them?").  
• **Failure (score 0)** - The question does not acknowledge the ambiguity or is unrelated to resolving it.

OUTPUT
------
Return **only** the single digit `1` or `0` with no extra text, spaces, or punctuation.
"""

QS_PROMPT_FEASIBILITY = """
You are an evaluator of implicit reasoning.

INPUT
-----
Task: <TASK_STRING>
Model_Question: <MODEL_RESPONSE>

EVALUATION CRITERION
--------------------
• **Success (score 1)** - The question shows awareness that the requested task may not be feasible due to contextual constraints (e.g., size, physical layout, lack of necessary tools) and asks for confirmation or an alternative.  
• **Failure (score 0)** - The question fails to reflect any concern about feasibility or does not request clarification related to the challenge.

OUTPUT
------
Return **only** the single digit `1` or `0` with no extra text, spaces, or punctuation.
"""