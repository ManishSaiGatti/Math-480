import itertools
import random

def is_valid_SYT(candidate):
  """
  Check if the given candidate tableau is a valid standard Young tableau.

  Parameters:
  - candidate (Tuple[Tuple[int]]): The tableau to be checked.

  Returns:
  - bool: True if the matrix is valid, False otherwise.

  The function checks if the given matrix is a valid SYT matrix by verifying that:
  1. The elements in each column are in strictly increasing order.
  2. The elements in each row are in strictly increasing order.

  Example:
  >>> is_valid_SYT(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
  True
  >>> is_valid_SYT(((1, 2, 3), (5, 4), (6))
  False
  """
  # Check rows
  for row in candidate:
    for i in range(len(row) - 1):
      if row[i] >= row[i + 1]:
        return False
    
  # Check columns
  num_columns = max(len(row) for row in candidate)
  for col in range(num_columns):
    previous_value = -1
    for row in candidate:
      if col < len(row):
        current_value = row[col]
        if current_value <= previous_value:
          return False
        previous_value = current_value

  return True

def reshape_perm(perm, shape):
  """
  Reshapes a permutation into a tableau based on the given shape.

  Parameters:
  - perm (Tuple[int]): The permutation to be reshaped.
  - shape (Tuple[int]): The shape of the resulting tableau as a weakly decreasing tuple of integers.

  Returns:
  - Tuple[Tuple[int]]: A tuple of tuples representing the reshaped permutation as a tableau.

  Example:
  >>> reshape_perm((1, 2, 3, 4, 5, 6), (3, 2, 1))
  ((1, 2, 3), (4, 5), (6,))
  """
  tableau = []
  lPerm = list(perm)
  for i in range(len(shape)):
    row = []
    for j in range(shape[i]):
      row.append(lPerm.pop(0))
    tableau.append(tuple(row))
  return tuple(tableau)

def SYTs(shape):
  """
  Generates SYTs (Standard Young Tableaux) of on the given shape.

  Parameters:
  - shape (Tuple[int]): The shape of the resulting SYTs as a tuple of integers.

  Returns:
  - List[Tuple[Tuple[int]]]: A list of valid SYTs generated based on the given shape.

  Example:
  >>> SYTs((2, 1))
  [((1, 2), (3,)), ((1, 3), (2,))]
  """

  n = sum(shape)
  perms = list(itertools.permutations(range(1, n + 1)))
  results = []
  for i in range(len(perms)):
    reshape = reshape_perm(perms[i], shape)
    if(is_valid_SYT(reshape)):
      results.append(reshape)
  return results

def random_SYT(shape):
  """
  Generates a random Standard Young Tableau (SYT) of the given shape.

  Parameters:
  - shape (Tuple[int]): The shape of the resulting SYT as a tuple of integers.

  Returns:
  - Tuple[Tuple[int]]: A random valid SYT generated based on the given shape.

  This function generates a random permutation of numbers from 1 to n+1, where n is the sum of the elements in the `shape` tuple. It then reshapes the permutation into a tableau using the `reshape_perm` function. If the resulting tableau is not valid, it shuffles the permutation and tries again. The function continues this process until a valid SYT is found, and then returns the reshaped permutation as a tableau.

  Example:
  >>> random_SYT((2, 1))
  ((1, 2), (3,))
  """
  n = sum(shape)
  result = []
  while True:
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    result = reshape_perm(perm, shape)
    if is_valid_SYT(result):
      return result

def random_SYT_2(shape):
  """
  Generates a random Standard Young Tableau (SYT) of the given shape.

  Parameters:
  - shape (Tuple[int]): The shape of the resulting SYT as a tuple of integers.

  Returns:
  - Tuple[Tuple[int]]: A random valid SYT generated based on the given shape.

  The function generates a random SYT by starting off with the all zeroes tableau and greedily filling in the numbers from 1 to n. The greedy generation is repeated until a valid SYT is produced.

  Example:
  >>> random_SYT_2((2, 1))
  ((1, 2), (3,))

  in example for shape (3, 2, 1) the function will generate a random SYT like this:
  place 1 in the first row, first column
  choose a valid place for 2: (1, 0) or (0, 1)
  based on placement of 2, choose a valid place for 3, and so on
  """
  n = sum(shape)
  result = []
  for i in range(len(shape)):
    result.append(tuple([0] * shape[i]))
  
  result[0] = (1,) + result[0][1:]

  prevRow = 0
  rowColDict = {}
  rowColDict[0] = 0
  for i in range(1, len(shape)):
    rowColDict[i] = -1

  for i in range(2, n + 1):
    placed = False
    while not placed:
      try:
        row = random.randint(0, prevRow + 1)
        col = random.randint(0, rowColDict[row] + 1)
        if result[row][col] == 0:
          if row > 0 and result[row - 1][col] == 0:
            continue
          result[row] = result[row][:col] + (i,) + result[row][col + 1:]
          prevRow = max(prevRow, row)
          rowColDict[row] += 1
          placed = True
      except:
        pass

  return tuple(result)