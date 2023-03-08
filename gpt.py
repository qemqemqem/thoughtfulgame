import os
import time

import openai

# Set up your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]


# Do GPT completion
def prompt_completion(question):
    start_time = time.perf_counter()
    prompt = f"{question} "
    response = openai.Completion.create(
        engine="curie", # "curie" is cheaper, "davinci" is good, there's also an option to get chatgpt on the website
        prompt=prompt,
        max_tokens=64,
        n=1,
        stop=["."],  # ["\n", " Q:"],
        temperature=0.5,
    )
    answer = response.choices[0].text.strip()
    # print(f"\tPROMPT: {question}\n\tANSWER: {answer}\n")
    duration = time.perf_counter() - start_time
    print("Duration: {:.2f} seconds".format(duration))
    return answer


if __name__ == "__main__":
    # Load questions from a file
    with open("questions.txt", "r") as f:
        questions = [line.strip() for line in f]

    # Generate answers for each question and print the result
    for question in questions:
        answer = prompt_completion(question)
        print(f"\tQ: {question}\n\tA: {answer}\n")
