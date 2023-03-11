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
        # https://openai.com/blog/introducing-chatgpt-and-whisper-apis suggests "gpt-3.5-turbo", but my API key doesn't work for that
        engine="davinci-instruct-beta", # "curie" is cheaper, "davinci" is good, there's also an option to get chatgpt on the website
        prompt=prompt,
        max_tokens=64,
        n=1,
        stop=[".", "DONE"],  # ["\n", " Q:"],
        temperature=0.5,
    )
    answer = response.choices[0].text.strip()
    # print(f"\tPROMPT: {question}\n\tANSWER: {answer}\n")
    duration = time.perf_counter() - start_time
    print(f"Duration: {duration:.2f} seconds: {answer}")
    return answer


if __name__ == "__main__":
    # Load questions from a file
    with open("questions.txt", "r") as f:
        questions = [line.strip() for line in f]

    # Generate answers for each question and print the result
    for question in questions:
        answer = prompt_completion(question)
        print(f"\tQ: {question}\n\tA: {answer}\n")
