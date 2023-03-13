import os
import time
import re

import openai

# Set up your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]


# Do GPT completion
def prompt_completion(question, engine="davinci-instruct-beta", max_tokens=64, temperature=1.0, n=1, stop=None, return_top_n:int=None, ideal_length=None, collapse_newlines=True, throwaway_empties=True):
    if stop is None:
        stop = ["\n", "DONE"]
    start_time = time.perf_counter()
    prompt = f"{question} "
    response = openai.Completion.create(
        # https://openai.com/blog/introducing-chatgpt-and-whisper-apis suggests "gpt-3.5-turbo", but my API key doesn't work for that
        engine=engine,  # "curie" is cheaper, "davinci" is good, there's also an option to get chatgpt on the website
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=stop,  #["\n", "DONE"],  # ["\n", " Q:"],
        temperature=temperature,
    )
    if collapse_newlines:
        # Replace any number of newlines with a single newline, using regular expressions
        for i in range(len(response.choices)):
            response.choices[i].text = re.sub(r"\n+", "\n", response.choices[i].text)
    if return_top_n is None:
        answer = response.choices[0].text.strip()
    elif ideal_length is not None:
        answer = []
        ordered_choices = sorted(response.choices, key=lambda x: abs(sum(c.isalpha() for c in x.text)) - ideal_length)
        if throwaway_empties:
            ordered_choices = [x for x in ordered_choices if sum(c.isalpha() for c in x.text) > 0]
        for i in range(return_top_n):
            answer.append(response.choices[i].text.strip())
        print(f"Ordered choices: {ordered_choices}")
    else:  # TODO This doesn't really handle all cases
        answer = []
        for i in range(return_top_n):
            answer.append(response.choices[i].text.strip())
    # print(f"\tPROMPT: {question}\n\tANSWER: {answer}\n")
    duration = time.perf_counter() - start_time
    print(f"Duration: {duration:.2f} seconds: {answer}")
    return answer
