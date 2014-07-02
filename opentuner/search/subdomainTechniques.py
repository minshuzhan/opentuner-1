# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab autoindent smarttab
from manipulator import Parameter, PermutationParameter, BooleanParameter, PowerOfTwoParameter
from technique import register, PartialRandom
from bandittechniques import AUCBanditMetaTechnique
from pso import PSO
from geneticAlgorithm import GeneticAlgorithm
from differentialevolution import DESubdomain 

register(PSO(domain_param=PermutationParameter))
register(PSO(domain_param=BooleanParameter))
register(PSO(domain_param=PowerOfTwoParameter))

register(DESubdomain(PermutationParameter))
register(DESubdomain(BooleanParameter))
register(DESubdomain(PowerOfTwoParameter))

register(GeneticAlgorithm(domain_param=PermutationParameter))
register(GeneticAlgorithm(domain_param=BooleanParameter))
register(GeneticAlgorithm(domain_param=PowerOfTwoParameter))

register(PartialRandom(domain_param=PermutationParameter))
register(PartialRandom(domain_param=BooleanParameter))
register(PartialRandom(domain_param=PowerOfTwoParameter))
register(PartialRandom())

register(AUCBanditMetaTechnique([
	PSO('OX3'),
	GeneticAlgorithm(),
	DESubdomain(Parameter)
	],
	name='PSO_GA_DE'))

register(AUCBanditMetaTechnique([
	PSO('OX3', PermutationParameter),
	GeneticAlgorithm(domain_param=PermutationParameter),
	DESubdomain(PermutationParameter)
	],
	name='PSO_GA_DE-Permutation'))

register(AUCBanditMetaTechnique([
	PSO('OX3', BooleanParameter),
	GeneticAlgorithm(domain_param=BooleanParameter),
	DESubdomain(BooleanParameter)
	],
	name='PSO_GA_DE-Boolean'))

register(AUCBanditMetaTechnique([
	PSO('OX3', PowerOfTwoParameter),
	GeneticAlgorithm(domain_param=PowerOfTwoParameter),
	DESubdomain(PowerOfTwoParameter)
	],
	name='PSO_GA_DE-PowerOfTwo'))


