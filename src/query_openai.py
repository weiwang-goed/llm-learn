import argparse
import os
from typing import List
from openai.types.chat import ChatCompletionMessageParam
import openai
import chromadb

def prompt_content_extract(query: str, context: str) -> List:
    """
    Prompt for extraction-only.
    Args:
        - query (str): The original query.
        - context (List[str]): Local doc context, returned by embedding search.

    Returns:
        - A prompt for the LLM (List).
    """
    system = {
        "role": "system",
        "content": "you are to answer the question based only on the provided context, and not any other information."
        "If there is not enough information in the context to answer the question,"
        'start with "I am not sure: ", then try to make a guess, otherwise start with "Yes I do: " '
    }
    user = {
        "role": "user",
        "content": f"The question is {query}. \n Here is the context: \n" + context
    }
    return [system, user]


def prompt_content_refer(query: str, context: str) -> List:
    """
    Prompt for refering to context, but also combines its onw knowledge.
    Args:
        - query (str): The original query.
        - context (List[str]): Local doc context, returned by embedding search.

    Returns:
        - A prompt for the LLM (List).
    """
    system = {
        "role": "system",
        "content":'''
            You are an AI assistant that can answer questions using both your knowledge and information from provided context.
            1. Answer the user question using the information from the local document and your own knowledge.
            2. Clearly indicate which part of your answer is derived from the local document by starting with "According to the document:".
            3. Ensure that your response is concise and informative.
        '''
    }
    user = {
        "role": "user",
        "content": f"The question is {query}. \n Here is the context: \n" + context
    }

    return [system, user]


def get_response_openai(query: str, context: str, model: str, task='extract') -> str:
    """
    Queries the GPT API to get a response to the question.

    Args:
        - query (str): The original query.
        - context (List[str]): The context of the query.
    Returns:
        - A response (str) to the question.
    """
    if task=='extract':
        messages=prompt_content_extract(query, context)
    elif task=='refer':
        messages=prompt_content_refer(query, context)
    
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
    )

    return response.choices[0].message.content  # type: ignore



