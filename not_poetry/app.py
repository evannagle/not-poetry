import requests
import openai
import os
import time
import random

from not_poetry.calculator import add


class Poem:
    def __init__(self, title, author, lines):
        self.title = title
        self.author = author
        self.lines = lines

    def __str__(self):
        return "\n".join(self.lines)


def get_random_poem() -> Poem:
    api_response = requests.get(
        # "https://poetrydb.org/random"
        "https://poetrydb.org/author,random/Emily%20Dickinson;1"
    ).json()

    return Poem(
        title=api_response[0]["title"],
        author=api_response[0]["author"],
        lines=api_response[0]["lines"],
    )


def pause_as_if_thinking():
    """
    Pause the program for a few seconds to simulate thinking.
    """

    time.sleep(random.randint(5, 15))


def generate_ai_poem():
    """
    Get the AI summary of the changes.
    """

    open_ai_api_key = os.environ.get("OPENAI_API_KEY")

    random_poem = get_random_poem()

    client = openai.Client(api_key=open_ai_api_key)

    messages = [
        {
            "role": "system",
            "content": "\n".join(
                [
                    f"You are {random_poem.author} and you are writing a new poem after having finished {random_poem.title}.",
                    "The subject of the poem should be something different from the previous poem.",
                    "Both poems should be in the same style and have the same number of lines.",
                    "It's your job to ensure that no one would guess that the two poems were written by two different people.",
                ]
            ),
        }
    ]

    messages.append({"role": "user", "content": "\n".join(random_poem.lines[:40])})

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        temperature=0.5,
        messages=messages,
    )

    message = response.choices[0].message.content
    random_poem.lines = message.split("\n")
    return random_poem


def main():
    # split 50/50 between the two functions
    r = random.randint(0, 1)
    ai_generated = r == 0

    if ai_generated:
        poem = generate_ai_poem()
    else:
        # pause_as_if_thinking()
        poem = get_random_poem()

    # print a max of 40 lines
    lines = poem.lines[:40]
    print("\n".join(lines))
    print()

    # ask if the poem is AI generated or not
    print("Is this poem AI generated (y/n)?", end=" ")

    answer = input()

    correct_answer = "y" if ai_generated else "n"
    result = "correct" if answer == correct_answer else "incorrect"

    print(f"Your answer is {result}.")

    if ai_generated:
        print(
            f"The poem was AI generated. Inspired by the real poem, {poem.title} by {poem.author}"
        )
    else:
        print(f"The poem is by {poem.author} and is called {poem.title}.")
