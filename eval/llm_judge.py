import json
import re
from prompt import *

import re
def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses 

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f'<{tag}>(.*?)</{tag}>', text, re.DOTALL)
    return match.group(1) if match else ""


def create_client():
    # Define your LLM Judge here
    client = OpenAI(
        api_key="api_key",  
        api_version="api_version",
        base_url=f"{"api_base"}/openai/deployments/{"deployment_name"}"
    )
    return client

def get_llm_score(client, message):
    response_reason = client.chat.completions.create(
        model="o1-mini",
        messages=message
    )
    response_texts = [choice.message.content.strip() for choice in response_reason.choices]
    llm_score = response_texts[0]

    return llm_score
    

def llm_eval(client, mode: str, line: dict) -> str:

    task = line["question_implicit"]
    res = line["response"][0]
    category = line["category"]

    if category == "contradiction":
        prompt = ANS_PROMPT_CONTRADICTION
    elif category == "absence":
        prompt = ANS_PROMPT_ABSENCE
    elif category == "reference":
        prompt = ANS_PROMPT_REFERENCE
    elif category == "feasibility":
        prompt = ANS_PROMPT_FEASIBILITY

    # for implicit and SPP setting
    prompt = prompt + f"\n\nTask: {task}\n"
    prompt += f"Model_Response: {res_answer}\n"

    if mode == "CoT": 
        # evaluate the reasoning trance and final answer separately under the same criteria
        res_reason = extract_xml(res, "reason")
        res_answer = extract_xml(res, "answer")
        # reason
        prompt_reason = prompt + f"\n\nTask: {task}\n"
        prompt_reason += f"Model_Response: {res_reason}\n"
        messages_reason=[
                    { "role": "user", "content": [  
                        { 
                            "type": "text", 
                            "text": prompt_reason,
                        }
                    ] } 
                ]
        llm_score_reason = get_llm_score(client, messages_reason)
        # answer
        prompt_answer = prompt + f"\n\nTask: {task}\n"
        prompt_answer += f"Model_Response: {res_answer}\n"
        messages_answer=[
                    { "role": "user", "content": [  
                        { 
                            "type": "text", 
                            "text": prompt_answer,
                        }
                    ] } 
                ]
        llm_score_answer = get_llm_score(client, messages_answer)
        
        return {
                "i": i, 
                "data" : {
                    "i": line["i"],
                    "category" : category,
                    "sub_category" : line["sub_category"],
                    "image" : line["image"],
                    "question": task,
                    "response": res,
                    "llm_ans_reason": llm_score_reason,
                    "llm_ans_answer": llm_score_answer
                    }
                }
    elif mode == "clarification_free":
        if "question" in res: # model chooses to ask a question
            res = extract_xml(res, "question")
            if category == "contradiction":
                prompt = QS_PROMPT_CONTRADICTION
            elif category == "absence":
                prompt = QS_PROMPT_ABSENCE
            elif category == "reference":
                prompt = QS_PROMPT_REFERENCE
            elif category == "feasibility":
                prompt = QS_PROMPT_FEASIBILITY
            prompt += f"\n\nTask: {task}\n"
            prompt += f"Model_Question: {res}\n"

        else: # model directly answers, using prompts for evaluate answers
            prompt = prompt + f"\n\nTask: {task}\n"
            prompt += f"Model_Response: {res_answer}\n"   
    elif mode == "clarification_forced":
        res = extract_xml(res, "question")
        if category == "contradiction":
            prompt = QS_PROMPT_CONTRADICTION
        elif category == "absence":
            prompt = QS_PROMPT_ABSENCE
        elif category == "reference":
            prompt = QS_PROMPT_REFERENCE
        elif category == "feasibility":
            prompt = QS_PROMPT_FEASIBILITY
        prompt += f"\n\nTask: {task}\n"
        prompt += f"Model_Question: {res}\n"

    messages=[
                { "role": "user", "content": [  
                    { 
                        "type": "text", 
                        "text": prompt,
                    }
                ] }
            ]
    llm_score = get_llm_score(client, messages)

    return {
        "i": i, 
        "data" : {
            "i": line["i"],
            "category" : category,
            "sub_category" : line["sub_category"],
            "image" : line["image"],
            "question": task,
            "response": line["response"][0],
            "llm_ans": llm_score
            }
        }


model_response_file = "o3.json" # the response file you would like to be evaluated
mode = "clarification_force"

with open(model_response_file, 'r') as f:
    if model_response_file.endswith(".json"):
        response_data = json.load(f)
    else:
        response_data = []
        for line in f:
            response_data.append(json.loads(line.strip()))

print(len(response_data))

results = []
for line in response_data:
    results.append(llm_eval(line))

    with open(f"score_{model_response_file}_{mode}.json", 'w') as f:
        json.dump(results, f, indent=4)