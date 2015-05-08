#!/usr/bin/python

import adddeps #fix sys.path
import copy

import opentuner
from opentuner.search.manipulator import ConfigurationManipulator, IntegerParameter
from opentuner.measurement import MeasurementInterface

class SquareCover(MeasurementInterface):
  def __init__(self, args, puzzle):
    super(SquareCover, self).__init__(args)
    self.parallel_compile = True
    self.puzzle = puzzle
    # pad with false to simplify max_square
    for row in puzzle:
      row.append(False)
    puzzle.append([False]*len(puzzle[0]))

  def manipulator(self):
    m = ConfigurationManipulator()
    rows = len(self.puzzle)
    cols = len(self.puzzle[0])
    for r in xrange(0, rows):
      for c in xrange(0, cols):
        if self.puzzle[r][c]:
          m.add_parameter(IntegerParameter("{},{}".format(r, c), 1, self.max_square(self.puzzle, r, c)))
    return m

  def compile(self, cfg, id):
    cover = copy.deepcopy(self.puzzle)
    size = 0
    for r in xrange(len(cover)):
      for c in xrange(len(cover[0])):
        if cover[r][c]:
          s = min(cfg["{},{}".format(r, c)], self.max_square(cover, r, c))
          for row in cover[r:r+s]:
            row[c:c+s] = [False]*s
          size += 1
    return opentuner.resultsdb.models.Result(state='OK', time=float(size))

  def run_precompiled(self, desired_result, input, limit, compile_result, id):
    return compile_result

  def run(self, desired_result, input, limit):
    pass

  def save_final_config(self, configuration):
    cfg = configuration.data
    self.cover = []
    for r in xrange(len(self.puzzle)):
      for c in xrange(len(self.puzzle[0])):
        if self.puzzle[r][c]:
          s = min(cfg["{},{}".format(r, c)], self.max_square(self.puzzle, r, c))
          for row in self.puzzle[r:r+s]:
            row[c:c+s] = [False]*s
          self.cover.append({'X': c, 'Y': r, 'Size': s})

  @staticmethod
  def max_square(puzzle, r, c):
    s = 0
    while 1:
      for d in xrange(0, s+1):
        if not (puzzle[r+d][c+s] and puzzle[r+s][c+d]):
          return s
      s += 1

