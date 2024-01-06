# from typing import List, Union

# CYCLES = 500
# INITIAL_POPULATION = 500
# MAX_OFFSPRING = 3
# MAX_LIFESPAN = 30
# MAX_MALE_PARTNERS = 4
# CRISPR_FEMALES = 0.016
# POPULATION_LIMIT = 2000

# Vector = List[Union[float, int]]




# from typing import List, Union

# CYCLES = 120
# INITIAL_POPULATION = 2000
# MAX_OFFSPRING = 6
# MAX_LIFESPAN = 20
# MAX_MALE_PARTNERS = 4
# CRISPR_FEMALES = 0.016
# POPULATION_LIMIT = 3000
# CRISPR_RESISTANCE_RATE = 50

# Vector = List[Union[float, int]]

from typing import List, Union


CYCLES = 150  #simulation duration for an observation period
INITIAL_POPULATION = 2500  #initial population for more stability
MAX_OFFSPRING = 5  #number of offspring per female
MAX_LIFESPAN = 25  #ifespan to better represent a species with a 20-year lifespan
MAX_MALE_PARTNERS = 3  # Moderate polygamy for reproduction
CRISPR_FEMALES = 0.02  #percentage of females with the CRISPR-edited gene
POPULATION_LIMIT = 3500  #Adjust the population limit based on environmental capacity
CRISPR_RESISTANCE_RATE = 30  #chance of CRISPR resistance for more realistic scenarios

Vector = List[Union[float, int]]