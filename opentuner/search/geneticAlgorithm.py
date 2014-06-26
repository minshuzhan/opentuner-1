# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab autoindent smarttab
import random
import time
import logging
from fn import _
from technique import register
from technique import SequentialSearchTechnique

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)


class GeneticAlgorithm(SequentialSearchTechnique):
  """
  based on http://cci.lbl.gov/cctbx_sources/scitbx/differential_evolution.py
  """

  def __init__(self,
               population_size=10,
               cr=0.9,  # crossover rate
               mr=0.01,  # mutation rate
               elite_count=2,  # number of population members with high fitness to enter the next generation directly
               *pargs, **kwargs):

    self.population_size = population_size
    self.cr = cr
    self.mr = mr
    self.elite_count = elite_count
    self.population_size = population_size
    self.population = None  # list of Configuration instances
    super(GeneticAlgorithm, self).__init__(*pargs, **kwargs)

  def initial_population(self):
    self.population = [self.driver.get_configuration(self.manipulator.random()) for z in range(self.population_size)]

  def select(self):
    """
    Return two parent PopulationMember's selected from current population. Selection is fitness based. 
    """
    #TODO: check if all candidates in population have been evaluated?
    i1, i2 = SUS(self.get_scores(), 2)
    print 'SELECT', i1, i2
    return self.population[i1], self.population[i2] 

  def get_scores(self):
   # pop = self.population
   # objective = self.driver.objective
   # base = pop[0] 
   # scores = []
   # for p in pop:
   #   scores.append(objective.config_relative(p, base))
   # return scores
   scores = [p.score for p in self.population]
   return scores

  def main_generator(self):
    if not self.population:
      # first time called
      self.initial_population()
    for p in self.population:
      yield p
    print 'Pop initiated'
    self.update_pop_scores()

    while True:
      print 'NEW GEN'
      self.population=sorted(self.population, key=lambda x: x.score, reverse=True)
      print self.get_scores()
      new_gen=self.population[:self.elite_count]
      # Create a new generation of population
      while len(new_gen)<self.population_size:
        # selection
        p1, p2 = self.select()
        # crossover
        if random.random()<self.cr:
          children = self.manipulator.crossover_uniform(p1.data, p2.data)
        else:
          children = [p1.data,p2.data]
        # mutate
        for c in children:
          self.manipulator.mutate(c, mr=self.mr)
          config = self.driver.get_configuration(c)
          yield config
          new_gen.append(config)
      self.population = new_gen
      self.update_pop_scores()

  def update_pop_scores(self):
    pop = self.population
    objective = self.driver.objective
    base = pop[0] 
    for p in pop:
      p.score = objective.config_relative(base,p)

def SUS(scores, n):
  """ 
  Stochastic Universal Sampling
  score: ordered list of fitness scores (in the order of parents)
  n: number of offspring to be selected
  return list of offspring indices  
  """
  score_index = [(scores[i], i) for i in range(len(scores))]  # list of (score, index) tuples
  d = sum(scores)/float(n)
  r = random.random()*d
  pointers = [r+i*d for i in range(n)]
  keep = []
  i=0
  ssum = 0
  for pointer in pointers:
    while ssum < pointer:
      ssum+=score_index[i][0]
      i+=1
    keep.append(i-1)
  return [score_index[i][1] for i in keep]

register(GeneticAlgorithm(name='GA'))

