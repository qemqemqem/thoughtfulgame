import os

import openai

# Set up your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]


# Do GPT completion
def prompt_completion(question):
    prompt = f"{question} "
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=64,
        n=1,
        stop=["."],  # ["\n", " Q:"],
        temperature=0.5,
    )
    answer = response.choices[0].text.strip()
    print(f"\tPROMPT: {question}\n\tANSWER: {answer}\n")
    return answer


if __name__ == "__main__":
    # Load questions from a file
    with open("questions.txt", "r") as f:
        questions = [line.strip() for line in f]

    # Generate answers for each question and print the result
    for question in questions:
        answer = prompt_completion(question)
        print(f"\tQ: {question}\n\tA: {answer}\n")
