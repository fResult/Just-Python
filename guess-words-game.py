from random import choice
from typing import Any, Callable, Literal, TypedDict

type PredicateFn[T] = Callable[[T], bool]
type MapperFn[T, R] = Callable[[T], R]
type GameStateKey = Literal["score", "lives", "words", "picked_word", "clue_word"]


class GameState(TypedDict):
    score: int
    lives: int
    words: list[str]
    picked_word: str
    clue_word: str


SCORE_WORD: int = 100
SCORE_CHAR: int = 10
MAX_LIVES: int = 5

INITIAL_GAME_STATE: GameState = {
    "score": 0,
    "lives": MAX_LIVES,
    "words": ["lisa", "cherprang", "jaa", "korn", "jennie"],
    "picked_word": "",
    "clue_word": "",
}


def copy_game_state(game_state: GameState) -> GameState:
    copied_game_state = game_state.copy()
    copied_game_state["words"] = game_state["words"].copy()
    return copied_game_state


def is_alive(lives: int) -> bool:
    return lives > 0


def is_remain[T](items: list[T]) -> bool:
    return len(items) > 0


def is_game_over(game_state: GameState) -> bool:
    return not is_alive(game_state["lives"]) or is_not_remain(game_state["words"])


def negate[T](predicate: PredicateFn[T]) -> PredicateFn[T]:
    def for_arg(arg: T) -> bool:
        return not predicate(arg)

    return for_arg


is_not_remain = negate(is_remain)


def is_guessed_all_chars_in_word(guessed_word: str) -> PredicateFn[list[str]]:
    def for_clue_characters(clue_characters: list[str]) -> bool:
        clue_word = "".join(clue_characters)
        return guessed_word == clue_word

    return for_clue_characters


def is_equal[T](y: T):
    for_x: PredicateFn[T] = lambda x: x == y
    return for_x


def filter_by[T](predicate: PredicateFn[T]):
    def for_xs(xs: list[T]) -> list[T]:
        return [x for x in xs if predicate(x)]

    return for_xs


def map_by[T, R](f: MapperFn[T, R]):
    def for_xs(xs: list[T]) -> list[R]:
        return [f(x) for x in xs]

    return for_xs


def pick_item_from_list[T](items: list[T]) -> T:
    try:
        return choice(items)
    except IndexError:
        IndexError("Error: Cannot pick item bec of the list is empty")


def repeat_chars(n: int):
    def for_str(string: str) -> str:
        return n * string

    return for_str


def create_clue_chars(word: str) -> list[str]:
    return list(repeat_chars(len(word))("?"))


def replace_char_in_clue_chars(word_to_guess: str):
    """Replace character in the list of character

    Args:
      word_to_guess (str): Word

    Returns:
      ((str, list[str]) -> list[str]): The `for_guessed_char_and_clue` function which...
        Args:
          guessed_char (str): Only 1 character
          clue (list[str]): Example: `['?', '?', '?', '?']`

        Returns:
          list[str]: Replaced list of character
    """

    def for_guessed_char_and_clue(
        guessed_char: str, clue_chars: list[str]
    ) -> list[str]:
        word_chars = list(word_to_guess)
        pairs_of_clue_word = list(zip(clue_chars, word_chars))
        return [
            word_ch if word_ch == guessed_char.lower() else clue_ch
            for (clue_ch, word_ch) in pairs_of_clue_word
        ]

    return for_guessed_char_and_clue


def not_equal_to_word(name: str) -> bool:
    """TODO: Use until create `compose` function"""
    return negate(is_equal(name))


def filter_picked_word_out(word: str):
    return filter_by(not_equal_to_word(word))


def create_hearts_display_by_lives(lives: int) -> str:
    return "  ".join(repeat_chars(lives)("🩷").ljust(MAX_LIVES, "❌"))


def display_game_state(game_state: GameState) -> None:
    print(
        f"""
    Your score: {game_state['score']}
    Remaining lives: {create_hearts_display_by_lives(game_state['lives'])}
    """
    )


def update_game_state(game_state: GameState):
    def for_key_and_val(key: GameStateKey, new_value: Any) -> GameState:
        current_game_state = copy_game_state(game_state)
        current_game_state[key] = new_value
        return current_game_state

    return for_key_and_val


def display_clue_chars(clue_chars: list[str]) -> str:
    return f'| {' | '.join(clue_chars)} |'.upper()


def add_score_to_game_state(game_state: GameState):
    def add_score(score_to_add: int) -> GameState:
        current_score = game_state["score"]
        return update_game_state(game_state)("score", current_score + score_to_add)

    return add_score


def remove_current_word_from_game_state(game_state: GameState):
    def remove_current_word(word_to_remove: str) -> GameState:
        words = game_state["words"]
        return update_game_state(game_state)(
            "words",
            filter_by(not_equal_to_word(word_to_remove))(words),
        )

    return remove_current_word


def update_lives_in_game_state(game_state: GameState):
    def update_lives_by_clue_word_diff(clue_word: str, new_clue_word: str) -> GameState:
        current_lives = game_state["lives"]
        updated_lives = (
            current_lives - 1 if is_equal(clue_word)(new_clue_word) else current_lives
        )

        if negate(is_equal(current_lives))(update_game_state):
            updated_game_state = update_game_state(game_state)("lives", updated_lives)
            display_game_state(updated_game_state)
        return updated_game_state

    return update_lives_by_clue_word_diff


def display_guess_result(guessed_char: str):
    def display_result(clue_word: str) -> None:
        guessed_correct = guessed_char in clue_word
        print(
            f"""
      You guessed {'correct' if guessed_correct else 'wrong'}!!
      {'Lose 1 live!' if not(guessed_correct) else f'There are [{guessed_char.upper()}]s in the word'}
    """.strip(" ")
        )

    return display_result


def display_when_word_correct(word: str) -> None:
    print(
        f"""
    You are correct!
    The current word is [{word.upper()}]
    """
    )


def game_word_cycle(game_state: GameState):
    if is_game_over(game_state):
        return game_state

    picked_word = game_state["picked_word"]
    updated_clue_chars = game_state["clue_word"]
    update_clue_by_guessed_char_and_clue_chars = replace_char_in_clue_chars(picked_word)

    # TODO: Remove printing `Picked word: {picked_word}` when finish developing this function
    print(
        f"Clue of the word: {display_clue_chars(updated_clue_chars)}, Picked word: {picked_word}"
    )

    guessed_char = input("Please guess character in a name [a-z]: ")

    prev_clue_word: str = "".join(updated_clue_chars)
    updated_clue_chars: list[str] = update_clue_by_guessed_char_and_clue_chars(
        guessed_char, updated_clue_chars
    )

    updated_clue_word: str = "".join(updated_clue_chars)
    game_state = update_game_state(game_state)("clue_word", updated_clue_word)

    display_guess_result(guessed_char)(updated_clue_word)
    print(
        f"""
    Clue characters: {display_clue_chars(updated_clue_chars)}
  """
    )

    not_equal_to_prev_clue_word = negate(is_equal(prev_clue_word))
    game_state = add_score_to_game_state(game_state)(
        score_to_add=SCORE_CHAR if not_equal_to_prev_clue_word(updated_clue_word) else 0
    )
    game_state = update_lives_in_game_state(game_state)(
        clue_word=prev_clue_word,
        new_clue_word=updated_clue_word,
    )
    return game_state


def display_game_result(game_state: GameState) -> None:
    no_more_words = is_not_remain(game_state["words"])
    filler = "" if no_more_words else "#"
    print(
        f"""
      ##############{filler}
      ## You {"win!" if no_more_words else "lose!"} ##
      ##############{filler}
      """
    )
    display_game_state(game_state)


def game_cycle(game_state: GameState) -> GameState:
    if is_game_over(game_state):
        display_game_result(game_state)
        return game_state

    current_game_state = copy_game_state(game_state)

    picked_word: str = pick_item_from_list(current_game_state["words"])
    current_game_state = update_game_state(current_game_state)(
        "picked_word", picked_word
    )

    clue_chars = create_clue_chars(picked_word)
    current_game_state = update_game_state(current_game_state)(
        "clue_word", "".join(clue_chars)
    )

    is_remaining_some_clue_chars = negate(is_guessed_all_chars_in_word(picked_word))
    is_not_game_over = negate(is_game_over)

    while is_remaining_some_clue_chars(clue_chars) and is_not_game_over(
        current_game_state
    ):
        current_game_state = game_word_cycle(current_game_state)
        clue_chars = list(current_game_state["clue_word"])

    if is_not_game_over(current_game_state):
        current_game_state = add_score_to_game_state(current_game_state)(
            score_to_add=SCORE_WORD - SCORE_CHAR
        )
        current_game_state = remove_current_word_from_game_state(current_game_state)(
            word_to_remove=picked_word
        )
        display_when_word_correct(picked_word)

    display_game_state(current_game_state)

    return game_cycle(current_game_state)


def main():
    game_cycle(INITIAL_GAME_STATE)


main()
