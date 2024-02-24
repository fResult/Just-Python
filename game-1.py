from random import choice
from types import MappingProxyType
from typing import Callable, List, Literal, Any

type PredicateFn[T] = Callable[[T], bool]
type MapperFn[T, R] = Callable[[T], R]
type GameStateKey = Literal['score', 'lives', 'words']
type GameState = dict[GameStateKey, Any]

# TODO: Use class instead of dictionary
INITIAL_GAME_STATE = {
  "score": 0,
  "lives": 5,
  "words": ['lisa', 'cherprang', 'jaa', 'korn', 'jennie'],
  # TODO: May need `picked_word` and `clue`(?)
  # "picked_word": '',
  # "clue": [],
}

def copy_game_state(game_state: GameState) -> GameState:
  copied_game_state = game_state.copy()
  copied_game_state['words'] = game_state['words'].copy()
  return copied_game_state

def is_alive(lives: int) -> bool:
  return lives > 0

def is_remain[T](items: List[T]) -> int:
  return len(items) > 0

def is_game_over(game_state: GameState) -> bool:
  return game_state['lives'] == 0 or is_not_remain(game_state['words'])

def negate[T](predicate: PredicateFn[T]) -> PredicateFn[T]:
  def for_arg(arg: T) -> bool:
    return not predicate(arg)
  return for_arg

is_not_remain = negate(is_remain)

# TODO: Add score +100 when guessing word is correct
def is_guessed_all_chars_in_word(guessed_word: str) -> Callable[[List[str]], bool]:
  def for_clue_characters (clue_characters: List[str]) -> bool:
    clue_word = ''.join(clue_characters)
    return guessed_word == clue_word
  return for_clue_characters

def is_equal[T](y: T):
  for_x: Callable[[T], bool] = lambda x: x == y
  return for_x

def filter_by[T](predicate: PredicateFn[T]):
  def for_xs(xs: List[T]) -> List[T]:
    return [x for x in xs if predicate(x)]
  return for_xs

def map_by[T, R](f: MapperFn[T, R]):
  def for_xs(xs: List[T]) -> List[R]:
    return [f(x) for x in xs]
  return for_xs

def pick_item_from_list[T](items: List[T]) -> T:
  try:
    return choice(items)
  except  (IndexError):
    IndexError('Error: Cannot pick item bec of the list is empty')

def repeat_chars(n: int):
  def for_str(string: str) -> str:
    return n * string
  return for_str

def create_clue_characters(word: str) -> str:
  return list(repeat_chars(len(word))('?'))

# TODO: Add score +10 when guessing character is correct.
def replace_char_in_clue_chars(word_to_guess: str):
  """Replace character in the list of character

  Args:
    word_to_guess (str): Word

  Returns:
    ((str, List[str]) -> List[str]): The `for_guessed_char_and_clue` function which...
      Args:
        guessed_char (str): Only 1 character
        clue (List[str]): Example: `['?', '?', '?', '?']`

      Returns:
        List[str]: Replaced list of character
  """
  def for_guessed_char_and_clue(guessed_char: str, clue_chars: List[str]) -> List[str]:
    word_chars = list(word_to_guess)
    pairs_of_clue_word = list(zip(clue_chars, word_chars))
    return [word_ch if word_ch == guessed_char else clue_ch for (clue_ch, word_ch) in pairs_of_clue_word]

  return for_guessed_char_and_clue

def not_equal_to_word(name: str) -> bool:
  """Use until create `compose` function"""
  return negate(is_equal(name))

def filter_picked_word_out(word: str) -> Callable[[List[str]], List[str]]:
  return filter_by(not_equal_to_word(word))

def create_hearts_display_by_lives(lives: int) -> str:
  MAX_LIVES = 5
  return "  ".join(repeat_chars(lives)('🩷').ljust(MAX_LIVES, '❌'))

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

def display_clue_chars(clue_chars: List[str]) -> str:
  return f'| {' | '.join(clue_chars)} |'

def add_score_to_game_state(game_state: GameState):
  def add_score(score_to_add: int) -> GameState:
    current_score = game_state['score']
    return update_game_state(game_state)('score', current_score + score_to_add)
  return add_score

def remove_current_word_from_game_state(game_state: GameState):
  def remove_current_word(word_to_remove: str) -> GameState:
    words = game_state['words']
    return update_game_state(game_state)(
      'words',
      filter_by(not_equal_to_word(word_to_remove))(words),
    )
  return remove_current_word

def update_lives_in_game_state(game_state: GameState):
  def update_lives_by_clue_chars_diff(clue_chars: str, new_clue_chars: str) -> GameState:
    current_lives = game_state['lives']
    updated_lives = current_lives - 1 if is_equal(clue_chars)(new_clue_chars) else current_lives

    if negate(is_equal(current_lives))(update_game_state):
      print(
        """
        You guess wrong!!
        Lose 1 live!
        """
      )
      updated_game_state = update_game_state(game_state)('lives', updated_lives)
      display_game_state(updated_game_state)
    return updated_game_state

  return update_lives_by_clue_chars_diff

def game_words_cycle(game_state: GameState) -> GameState:
  if is_game_over(game_state):
    print(
      f"""
      You {"win!" if is_not_remain(game_state['words']) else "lose!"}
      """
    )
    display_game_state(game_state)
    return game_state

  current_game_state = copy_game_state(game_state)
  picked_word = pick_item_from_list(current_game_state['words'])

  clue_chars = create_clue_characters(picked_word)

  is_remaining_some_clue_chars = negate(is_guessed_all_chars_in_word(picked_word))
  update_clue_by_guessed_char_and_clue_chars = replace_char_in_clue_chars(picked_word)
  updated_clue_chars = list(clue_chars)

  while is_remaining_some_clue_chars(updated_clue_chars):
    # TODO: Remove printing `Picked word: {picked_word}` when finish developing this function
    print(f'Clue of the word: {display_clue_chars(updated_clue_chars)}, Picked word: {picked_word}')
    guessed_char = input('Please guess character in a name [a-z]: ')
    prev_clue_word = ''.join(updated_clue_chars)
    updated_clue_chars = update_clue_by_guessed_char_and_clue_chars(guessed_char, updated_clue_chars)
    updated_clue_word = ''.join(updated_clue_chars)
    print('clue_chars', updated_clue_chars)
    print(f'Clue characters: {display_clue_chars(updated_clue_chars)}, Guessed char: {guessed_char}')

    not_equal_to_prev_clue_word = negate(is_equal(prev_clue_word))

    current_game_state = add_score_to_game_state(current_game_state)(
      score_to_add = 10 if not_equal_to_prev_clue_word(updated_clue_word) else 0
    )
    current_game_state = update_lives_in_game_state(current_game_state)(
      clue_chars = prev_clue_word,
      new_clue_chars = updated_clue_word,
    )

  # Use `compose` function instead
  current_game_state = add_score_to_game_state(current_game_state)(score_to_add = 100)
  current_game_state = remove_current_word_from_game_state(current_game_state)(word_to_remove = picked_word)
  print(
    f"""
    You are correct!
    The current word is {picked_word}
    """
  )
  display_game_state(current_game_state)

  return game_words_cycle(current_game_state)

# remaining_words = INITIAL_GAME_STATE['words']
# picked_name = pick_item_from_list(remaining_words)
# remaining_words = filter_picked_word_out(remaining_words)

# print(f'clue word of {picked_name} is: {create_clue_characters(picked_name)}')
# print('picked name:', picked_name)
# print('remaining name:', remaining_words)
# print('remain?:', is_remain(remaining_words))

# picked_name = pick_item_from_list(remaining_words)
# remaining_words = filter_by(negate(is_equal(picked_name)))(remaining_words)
# print('picked name:', picked_name)
# print('remaining name:', remaining_words)
# print('remain?:', is_remain(remaining_words))

# picked_name = pick_item_from_list(remaining_words)
# remaining_words = filter_by(negate(is_equal(picked_name)))(remaining_words)
# print('picked name:', picked_name)
# print('remaining name:', remaining_words)
# print('remain?:', is_remain(remaining_words))

def main():
  # game_state = copy_game_state(INITIAL_GAME_STATE)
  # remaining_names = INITIAL_GAME_STATE['words']
  # picked_name = pick_item_from_list(remaining_names)
  # print('is not remain', is_not_remain(remaining_names))
  # clue_chars = create_clue_characters(picked_name)
  # print(f'Picked Name is: {picked_name}')
  # print(f'Clue Name is: {clue_chars}')
  # guessed_char = input('Please guess character in a name [a-z]: ')
  # replaced_chars = replace_char_in_clue_chars(guessed_char, picked_name)
  # print(f'replaced chars: {replaced_chars}')
  game_words_cycle(INITIAL_GAME_STATE)

main()
