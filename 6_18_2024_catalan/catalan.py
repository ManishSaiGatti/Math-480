import itertools

def parenthesizations(n):
  """
  Returns a set of all possible parenthesizations of length n.

  Parameters:
    n (int): The length of the parenthesizations.

  Returns:
    A set of strings, where each inner string represents a valid parenthesization of length n.
  
  Example:
  >>> parenthesizations(3)
  {'((()))', '(()())', '(())()', '()(())', '()()()'}
  """
  if n == 0:
    return {""}
  else:
    # For n > 0
    return {"(" + a + ")" + b for i in range(n) for a in parenthesizations(i) for b in parenthesizations(n-i-1)}

def product_orders(n):
  """
  Returns a set of all possible ways to multiply of n elements.

  Parameters:
    n (int): The number of elements multiplied.

  Returns:
    A set of strings where each string represents a way to multiply n elements.
  
  Example:
  >>> product_orders(4)
  {'((?*?)*?)*?', '(?*(?*?))*?', '(?*?)*(?*?)', '?*((?*?)*?)', '?*(?*(?*?))'}
  """
  if n == 0:
    return {""}
  elif n == 1:
    return {"?"}
  elif n == 2:
    return {"?*?"}
  else:
    results = set()
    for i in range(1, n):
      for a in product_orders(i):
        for b in product_orders(n-i):
          results.add("(" + a + ")*(" + b + ")")
    return results

def permutations_avoiding_231(n):
  """
  Returns a set of permutations of length n avoiding the pattern 2-3-1.
  
  Parameters:
    n (int): The length of the permutation.
  
  Returns:
    A set of permutations of length n that do not contain the pattern 2-3-1.
  
  Example:
  >>> permutations_avoiding_231(4)
  {(1, 2, 3, 4), (1, 2, 4, 3), (1, 3, 2, 4), (1, 4, 2, 3), (1, 4, 3, 2), (2, 1, 3, 4), (2, 1, 4, 3), (3, 1, 2, 4), (3, 2, 1, 4), (4, 1, 2, 3), (4, 1, 3, 2), (4, 2, 1, 3), (4, 3, 1, 2), (4, 3, 2, 1)}
  """
  if n < 3:
    return set(itertools.permutations(range(1, n+1)))
  else:
    # general case dont repeat the same number
    def contains_231_pattern(perm):
        for i in range(len(perm)):
            for j in range(i+1, len(perm)):
                for k in range(j+1, len(perm)):
                    if perm[k] < perm[i] < perm[j]:
                        return True
        return False
    
    all_perms = set(itertools.permutations(range(1, n+1)))
    valid_perms = {perm for perm in all_perms if not contains_231_pattern(perm)}
    
    return valid_perms

def triangulations(n):
  """
  Returns a set of all possible triangulations of an n-sided polygon. A triangulation
  is represented as a tuple of internal edges. Vertices are labeled 0 through n-1 clockwise.

  Parameters:
    n (int): The number of sides of the polygon.

  Returns:
    A set of tuple of pairs, where each pair represents an internal edge in the triangulation.
  
  Example:
  >>> triangulations(3)
  {((0, 3), (1, 3)), ((1, 4), (2, 4)), ((1, 3), (1, 4)), ((0, 2), (2, 4)), ((0, 2), (0, 3))}
  """
  if n < 3:
    return set()
  elif n == 3:
    return {tuple()}
  else:
    # General case
    def internal_edges(triang):
            edges = set()
            for i in range(len(triang) - 2):
                for j in range(i + 2, len(triang) - (1 if i == 0 else 0)):
                    edges.add((triang[i], triang[j]))
            return edges
        
    def add_triangulations(triang, a, b, res):
        if b - a < 2:
            return
        for i in range(a + 1, b):
            if (triang[a], triang[i]) not in res and (triang[i], triang[b]) not in res:
                new_res = res | {(triang[a], triang[i]), (triang[i], triang[b])}
                yield from add_triangulations(triang, a, i, new_res)
                yield from add_triangulations(triang, i, b, new_res)
                yield new_res
    
    vertices = list(range(n))
    results = set()
    for triang in itertools.permutations(vertices):
        for res in add_triangulations(triang, 0, n-1, set()):
            results.add(frozenset(res))
    
    return {tuple(sorted(triang)) for triang in results}

print(triangulations(3))
print(triangulations(4))