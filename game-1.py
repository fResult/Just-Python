from random import choice
from typing import Callable, List, TypeAlias, TypeVar

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

def is_same_name(word: str):
  for_name: Callable[[str], bool] = lambda name: name == word
  return for_name

def filter_by(predicateFn: PredicateFn, xs: List[T]) -> List[T]:
  return list(filter(predicateFn, xs))

def map_by(f: MapperFn, xs: List[T]) -> List[R]:
  return list(map(f, xs))


def pick_name_from_names(names: List[str]) -> str:
  return choice(names)

def negate(predicate_fn: PredicateFn) -> PredicateFn:
    return lambda arg: not predicate_fn(arg)

def create_clue_characters(word: str) -> str:
  return list(len(word) * '?')

def find_index(char: chr, chars: List[chr]) -> int:
  try:
    return chars.index(char)
  except ValueError:
    return -1

def replace_char_in_clue_chars(guessed_char: chr, name: str, clue: List[chr]) -> List[chr]:
  found_idx: int = -1
  name_chars = list(name)
  # updated_clue = clue.copy()

  # while find_index(char, name_chars) >= 0:
  #   found_idx = name_chars.index(char)
  #   if found_idx >= 0:
  #     updated_clue = [name[found_idx] if idx == found_idx else c for idx, c in enumerate(updated_clue)]
  #     name_chars = ['' if idx == found_idx else c for idx, c in enumerate(name_chars)]
  #   else:
  #     updated_clue = clue

  updated_clue = [c if c == guessed_char else '?' for c in name_chars]

  return updated_clue


remainingWords = INITIAL_GAME_STATE['names']
picked_name = pick_name_from_names(remainingWords)
remainingWords = filter_by(negate(is_same_name(picked_name)), remainingWords)

# print(f'clue word of {picked_name} is: {create_clue_characters(picked_name)}')
# print('picked name:', picked_name)
# print('remaining name:', remainingWords)
# print('remain?:', is_remain(remainingWords))

# picked_name = pick_name_from_names(remainingWords)
# remainingWords = filter_by(negate(is_same_name(picked_name)), remainingWords)
# print('picked name:', picked_name)
# print('remaining name:', remainingWords)
# print('remain?:', is_remain(remainingWords))

# picked_name = pick_name_from_names(remainingWords)
# remainingWords = filter_by(negate(is_same_name(picked_name)), remainingWords)
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
  print(replaced_chars)

main()