
from gpt import prompt_completion

def test_prompt_completion():
    answers = prompt_completion("Please write a 4 line poem about sandwiches:", n=10, return_top_n=3, ideal_length=80, stop=["\n\n\n"], temperature=0.5, collapse_newlines=True)
    for answer in answers:
        print("ANSWER:")
        print(answer)
        print()

if __name__ == "__main__":
    test_prompt_completion()