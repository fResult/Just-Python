from random import choice
from types import MappingProxyType
from typing import Callable, List

type PredicateFn[T] = Callable[[T], bool]
type MapperFn[T, R] = Callable[[T], R]

INITIAL_GAME_STATE = MappingProxyType({
  "score": 0,
  "lives": 5,
  "names": ['lisa', 'cherprang', 'jaa', 'korn', 'jennie'],
})

def copy_game_state(game_state: dict[str, int | List[str]]) -> dict[str, int | List[str]]:
  copied_game_state = game_state.copy()
  copied_game_state['names'] = game_state['names'].copy()
  return copied_game_state

def is_alive(lives: int) -> bool:
  return lives > 0

def is_remain[T](items: List[T]) -> int:
  return len(items) > 0

def is_guessed_all_char(guessed_name: str, clue_characters: List[str]) -> bool:
  clue_word = ''.join(clue_characters)
  return guessed_name == clue_word

def is_equal[T](y: T) -> Callable[[T], bool]:
  for_x: Callable[[T], bool] = lambda x: x == y
  return for_x

def filter_by[T](predicate: PredicateFn[T]) -> Callable[[List[T]], List[T]]:
  def for_xs(xs: List[T]) -> List[T]:
    return [x for x in xs if predicate(x)]
  return for_xs

def map_by[T, R](f: MapperFn[T, R]) -> Callable[[List[T]], List[R]]:
  def for_xs(xs: List[T]) -> List[R]:
    return [f(x) for x in xs]
  return for_xs

def pick_name_from_names(names: List[str]) -> str:
  return choice(names)

def negate[T](predicate: PredicateFn[T]) -> PredicateFn[T]:
  def for_arg(arg: T) -> bool:
    return not predicate(arg)
  return for_arg

def repeat_chars(n: int) -> Callable[[str], str]:
  def for_str(string: str) -> str:
    return n * string
  return for_str

def create_clue_characters(word: str) -> str:
  return list(repeat_chars(len(word))('?'))

def replace_char_in_clue_chars(guessed_char: str, name: str) -> List[str]:
  """Replace character in the list of character

  Args:
      guessed_char (str): Only 1 character
      name (str): String

  Returns:
      List[str]: Replaced list of character
  """
  name_chars = list(name)
  return [ch if ch == guessed_char else '?' for ch in name_chars]

remaining_words = INITIAL_GAME_STATE['names']
picked_name = pick_name_from_names(remaining_words)
remaining_words = filter_by(negate(is_equal(picked_name)))(remaining_words)

print(f'clue word of {picked_name} is: {create_clue_characters(picked_name)}')
print('picked name:', picked_name)
print('remaining name:', remaining_words)
print('remain?:', is_remain(remaining_words))

picked_name = pick_name_from_names(remaining_words)
remaining_words = filter_by(negate(is_equal(picked_name)))(remaining_words)
print('picked name:', picked_name)
print('remaining name:', remaining_words)
print('remain?:', is_remain(remaining_words))

picked_name = pick_name_from_names(remaining_words)
remaining_words = filter_by(negate(is_equal(picked_name)))(remaining_words)
print('picked name:', picked_name)
print('remaining name:', remaining_words)
print('remain?:', is_remain(remaining_words))

def main():
  game_state = copy_game_state(INITIAL_GAME_STATE)
  print('before', game_state['lives'])
  print('after', game_state['lives'])
  remaining_names = INITIAL_GAME_STATE['names']
  picked_name = pick_name_from_names(remaining_names)
  clue_chars = create_clue_characters(picked_name)
  print(f'Picked Name is: {picked_name}')
  print(f'Clue Name is: {clue_chars}')
  guessed_char = input('Please guess character in a name [a-z]: ')
  replaced_chars = replace_char_in_clue_chars(guessed_char, picked_name)
  print(f'replaced chars: {replaced_chars}')

main()
