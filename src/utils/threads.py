import time
from concurrent.futures import ThreadPoolExecutor

def my_task(args):
    print("Inicio task", args[0])
    time.sleep(args[1])
    print("Fin task", args[0])
    return args[0]

items = [(1, 10), (2, 15), (3, 10), (4, 15), (5, 12), (6, 10)]

def execute_threads():
  print('Inicio threads')
  with ThreadPoolExecutor() as executor:
      print('MAX_THREADS', executor._max_workers) # Por defecto toma la cantidad de hilos del servidor
      results = executor.map(my_task, items)

  # Iterate over the results
  for result in results:
      print('Respondiendo thread', result)
  print('Fin threads')
