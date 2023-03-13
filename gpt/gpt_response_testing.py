
from gpt import *


def test_prompt_completion():
    answers = prompt_completion("Please write a 4 line poem about sandwiches:", n=10, return_top_n=3, ideal_length=80,
                                stop=["\n\n\n"], temperature=0.5, collapse_newlines=True)
    for answer in answers:
        print("ANSWER:")
        print(answer)
        print()


def test_room_description():
    dsc = "Here are the details of a place.\nThe place is a grassy plane with many trees.\nThese are the things in the place:\n * 3 goblins\n * an old shrine\n * a ruined building\n\nHere is a one paragraph description of the place in the style of JRR Tolkien:\n"
    answer = prompt_completion_chat(dsc)
    print("ANSWER:")
    print(answer)


if __name__ == "__main__":
    # test_prompt_completion()
    test_room_description()
