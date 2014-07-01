# -*- coding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab autoindent smarttab
from manipulator import *
from opentuner.search import technique
import random
import math

class PSO(technique.SequentialSearchTechnique ):
  """ Particle Swarm Optimization """
  def __init__(self, crossover='OX3', domain_param=None, N = 30, *pargs, **kwargs):
    """
    crossover: name of crossover operator function
    domain_params: list of applicable Parameter classes
    """
    super(PSO, self).__init__(*pargs, **kwargs)
    self.crossover = crossover
    if domain_param:
      self.domain_param = domain_param
      self.name = '-'.join(['PSO', domain_param.__name__[:-9]])
    else:
      self.name = 'PSO'
      self.domain_param = Parameter
    self.N = N

  def main_generator(self):

    objective   = self.objective
    driver    = self.driver
    m = self.manipulator
    def config(cfg):
      return driver.get_configuration(cfg)
    # Initiate particles with seed configurations if given
    seeds = self.driver.seed_cfgs_copy
    if not seeds:
      seeds = [None]
    population = [HybridParticle(m, self.crossover, self.domain_param, cfg=random.choice(seeds)) for i in range(self.N)]

    for p in population:
      yield driver.get_configuration(p.position)

    while True:
      for particle in population:
        g = driver.best_result.configuration.data
        old=m.copy(particle.position)
        particle.move(g)
        yield config(particle.position)
        # update individual best
        if objective.lt(config(particle.position), config(particle.best)):
          particle.best = particle.position

class HybridParticle(object):
  def __init__(self, m, crossover_choice, domain_param, omega=0.5, phi_l=0.5, phi_g=0.5, cfg=None):

    """
    m: a configuraiton manipulator
    omega: influence of the particle's last velocity, a float in range [0,1] ; omega=1 means even speed
    phi_l: influence of the particle's distance to its historial best position, a float in range [0,1]
    phi_g: influence of the particle's distance to the global best position, a float in range [0,1]
    """

    self.manipulator = m
    self.domain_param = domain_param
    if cfg:
      self.position = cfg
      for p in m.parameters(cfg):
        if isinstance(p, domain_param):
          p.randomize(self.position)
    else:
      self.position = self.manipulator.random()   
    self.best = self.position
    self.omega = omega
    self.phi_l = phi_l
    self.phi_g = phi_g
    self.crossover_choice = crossover_choice
    self.velocity = {}
    for p in self.manipulator.params:
      # Velocity as a continous value
      self.velocity[p.name]=0  

  def move(self, global_best):
    """
    Update parameter values using corresponding operators. 
    TODO: introduce operator choice map
    """
    m = self.manipulator
    for p in m.params:
      if isinstance(p, self.domain_param):
        self.velocity[p.name] = p.sv_swarm(self.position, global_best, self.best, omega=self.omega, phi_g=self.phi_g, phi_l=self.phi_l, c_choice=self.crossover_choice, velocity=self.velocity[p.name])


technique.register(PSO())
