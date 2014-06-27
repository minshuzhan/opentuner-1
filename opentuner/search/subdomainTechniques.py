# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab autoindent smarttab
from manipulator import PermutationParameter, BooleanParameter, PowerOfTwoParameter
from technique import register
from bandittechniques import AUCBanditMetaTechnique
from pso import PSO
from geneticAlgorithm import GeneticAlgorithm
from differentialevolution import DESubdomain 

register(AUCBanditMetaTechnique([
	PSO('OX3', PermutationParameter),
	PSO('PX', PermutationParameter),
	PSO('PMX', PermutationParameter),
	GeneticAlgorithm(domain_param=PermutationParameter),
	DESubdomain(PermutationParameter)
	],
	name='PSO_GA_DE-PERM'))

register(AUCBanditMetaTechnique([
	PSO('OX3', BooleanParameter),
	PSO('PX', BooleanParameter),
	PSO('PMX', BooleanParameter),
	GeneticAlgorithm(domain_param=BooleanParameter),
	DESubdomain(BooleanParameter)
	],
	name='PSO_GA_DE-BOOL'))

register(AUCBanditMetaTechnique([
	PSO('OX3', PowerOfTwoParameter),
	PSO('PX', PowerOfTwoParameter),
	PSO('PMX', PowerOfTwoParameter),
	GeneticAlgorithm(domain_param=PowerOfTwoParameter),
	DESubdomain(PowerOfTwoParameter)
	],
	name='PSO_GA_DE-POW2'))


