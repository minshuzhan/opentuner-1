# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab autoindent smarttab
import random
import time
import logging
from fn import _
from technique import register
from technique import SequentialSearchTechnique
import math
import copy
log = logging.getLogger(__name__)


class GeneticAlgorithm(SequentialSearchTechnique):
  """
  based on http://cci.lbl.gov/cctbx_sources/scitbx/differential_evolution.py
  """

  def __init__(self,
               domain_param=None,
               population_size=30,
               cr=0.9,  # crossover rate
               mr=0.01,  # mutation rate
               elite_count=1,  # number of population members with high fitness to enter the next generation directly
               *pargs, **kwargs):
    super(GeneticAlgorithm, self).__init__(*pargs, **kwargs)
    self.domain_param = domain_param
    self.name='GA'
    if domain_param:
      self.name += '-'+domain_param.__name__[:-9]

    self.population_size = population_size
    self.cr = cr
    self.mr = mr
    self.elite_count = elite_count
    self.population_size = population_size
    self.population = []  # list of Configuration instances

  def initial_population(self):
    # Initiate particles with seed configurations if given
    seeds = self.driver.seed_cfgs_copy
    for z in range(self.population_size):
      if seeds and self.domain_param:
        seed = random.choice(seeds)
        cfg = self.manipulator.copy(seed)
        for p in self.manipulator.parameters(seed):
          if isinstance(p, self.domain_param):
            p.randomize(cfg)
        self.seed = seed
      else:
        cfg = self.manipulator.random()
        self.seed = None
      self.population.append(self.driver.get_configuration(cfg)) 


  def select(self):
    """
    Return two parent PopulationMember's selected from current population. Selection is fitness based. 
    """
    #TODO: check if all candidates in population have been evaluated?
    # Rank-based selection
    raw = [1.0/i**0.5 for i in range(1, 1+self.population_size)]
    scores = map(lambda x: x/sum(raw)*2, raw)
    i1, i2 = SUS(scores, 2)
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
    log.debug('Population initiated')
    self.update_pop_scores()

    while True:
      log.debug('Unique population members: %s'%len(set(map(lambda x: self.manipulator.hash_config(x.data), self.population))))
      self.population=sorted(self.population, key=lambda member: min(map(lambda x: x.time, self.driver.results_query(config=member)))) # sort population based on minimal run time of configuration
      new_gen=self.population[:self.elite_count]
      log.debug('Scores %r' % self.get_scores())
      # Create a new generation of population
      while len(new_gen)<self.population_size:
        # selection
        p1, p2 = self.select()
        log.debug('parents %r, %r'% (self.manipulator.hash_config(p1.data), self.manipulator.hash_config(p2.data)))
        # crossover
        if random.random()<self.cr:
          children = self.manipulator.crossover_uniform(p1.data, p2.data, domain=self.domain_param)
        else:
          children = [p1.data,p2.data]
        # mutate
        for c in children:
          self.manipulator.mutate(c, mr=self.mr, domain=self.domain_param)
          config = self.driver.get_configuration(c)
          yield config
          new_gen.append(config)
      self.population = new_gen
      self.update_pop_scores()

  def update_pop_scores(self):
    pop = self.population
    for p in pop:
      # TODO WARNING: WORKS ONLY FOR MINIMIZING TIME! NOT READY FOR PUSH!
      p.score = 1/min(map(lambda x: x.time, self.driver.results_query(config=p)))

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

register(GeneticAlgorithm())
