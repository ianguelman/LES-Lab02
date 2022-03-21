from threading import Thread
import os
from math import ceil

class Multithreading:
  threads = []
  max_cpu = 0

  def __init__(self):
      self.max_cpu = os.cpu_count()

  def instance_threads(self, process, parameters, percent_use_cpu):
    for i in range(0, ceil(self.max_cpu * percent_use_cpu)):
      t = Thread(target=process, args=parameters)
      t.start()
      self.threads.append(t)
    for thread in self.threads:
        thread.join()
