from random import choice
from typing import Callable, List, TypeVar

T = TypeVar('T')
PredicateFn = Callable[[T], bool]

INITIAL_GAME_STATE = {
  "score": 0,
  "lives": 3,
  "words": ['great', 'cherprang', 'jaa', 'korn', 'jennie'],
}

def is_alive(lives: int) -> bool:
  return lives > 0

def is_remain(items: List[T]) -> int:
  return len(items) > 0

def is_same_name(word: str):
  for_name: Callable[[str], bool] = lambda name: name == word
  return for_name

def filter_by(predicateFn: PredicateFn, xs):
  return list(filter(predicateFn, xs))

def pick_name_from_names(names: List[str]) -> str:
  return choice(names)

def negate(predicate_fn: PredicateFn) -> PredicateFn:
    return lambda arg: not predicate_fn(arg)

def create_clue_characters(word: str) -> str:
  return list(len(word) * '?')

# def replace_char_in_clue_chars(char: chr) -> List[chr]:

remainingWords = INITIAL_GAME_STATE['words']
picked_name = pick_name_from_names(remainingWords)
remainingWords = filter_by(negate(is_same_name(picked_name)), remainingWords)

print(f'clue word of {picked_name} is: {create_clue_characters(picked_name)}')
print('picked name:', picked_name)
print('remaining name:', remainingWords)
print('remain?:', is_remain(remainingWords))

picked_name = pick_name_from_names(remainingWords)
remainingWords = filter_by(negate(is_same_name(picked_name)), remainingWords)
print('picked name:', picked_name)
print('remaining name:', remainingWords)
print('remain?:', is_remain(remainingWords))

picked_name = pick_name_from_names(remainingWords)
remainingWords = filter_by(negate(is_same_name(picked_name)), remainingWords)
print('picked name:', picked_name)
print('remaining name:', remainingWords)
print('remain?:', is_remain(remainingWords))
