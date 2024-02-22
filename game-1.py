from random import choice
from typing import Callable, List, TypeVar

T = TypeVar('T')
R = TypeVar('R')
PredicateFn = Callable[[T], bool]
MapperFn = Callable[[T], R]

INITIAL_GAME_STATE = {
  "score": 0,
  "lives": 3,
  "names": ['great', 'cherprang', 'jaa', 'korn', 'jennie'],
}

def is_alive(lives: int) -> bool:
  return lives > 0

def is_remain(items: List[T]) -> int:
  return len(items) > 0

def is_guess_all(guessed_name: str, clue_characters: List[str]) -> bool:
  clue_word = ''.join(clue_characters)
  return guessed_name == clue_word

def is_equal(y: T):
  for_x: Callable[[T], bool] = lambda x: x == y
  return for_x

def filter_by(predicate: PredicateFn):
  def for_xs(xs: List[T]) -> List[T]:
    return [x for x in xs if predicate(x)]
  return for_xs

def map_by(f: MapperFn):
  def for_xs(xs: List[T]) -> List[R]:
    return [f(x) for x in xs]
  return for_xs

def pick_name_from_names(names: List[str]) -> str:
  return choice(names)

def negate(predicate_fn: PredicateFn) -> PredicateFn:
    return lambda arg: not predicate_fn(arg)

def create_clue_characters(word: str) -> str:
  return list(len(word) * '?')

def replace_char_in_clue_chars(guessed_char: chr, name: str, clue: List[chr]) -> List[chr]:
  name_chars = list(name)
  return [ch if ch == guessed_char else '?' for ch in name_chars]


remainingWords = INITIAL_GAME_STATE['names']
picked_name = pick_name_from_names(remainingWords)
remainingWords = filter_by(negate(is_equal(picked_name)))(remainingWords)

# print(f'clue word of {picked_name} is: {create_clue_characters(picked_name)}')
# print('picked name:', picked_name)
# print('remaining name:', remainingWords)
# print('remain?:', is_remain(remainingWords))

# picked_name = pick_name_from_names(remainingWords)
# remainingWords = filter_by(negate(is_equal(picked_name)))(remainingWords)
# print('picked name:', picked_name)
# print('remaining name:', remainingWords)
# print('remain?:', is_remain(remainingWords))

# picked_name = pick_name_from_names(remainingWords)
# remainingWords = filter_by(negate(is_equal(picked_name)))(remainingWords)
# print('picked name:', picked_name)
# print('remaining name:', remainingWords)
# print('remain?:', is_remain(remainingWords))

def main():
  remaining_names = INITIAL_GAME_STATE['names']
  picked_name = pick_name_from_names(remaining_names)
  print(f'Picked Name is: {picked_name}')
  clue_chars = create_clue_characters(picked_name)
  guessed_char = input('Please guess character in a name: ')
  replaced_chars = replace_char_in_clue_chars(guessed_char, picked_name, clue_chars)
  print('replaced chars:', replaced_chars)

# main()