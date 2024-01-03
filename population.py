import random
from dataclasses import dataclass
import config
from typing import List, Tuple

@dataclass
class Creature:
    lifespan: int = random.randrange(1, config.MAX_LIFESPAN)
    age: int = random.randrange(lifespan)
    crispr_resistance: bool = False

    @property
    def is_dead(self) -> bool:
        """Checks whether the individual has expired."""
        return self.age >= self.lifespan

@dataclass
class MaleCreature(Creature):
    # Males are NOT sterile by default.
    sterile: bool = False

@dataclass
class FemaleCreature(Creature):
    # Females do NOT carry edited gene by default.
    crispr: bool = False

MalesPopulation: List[MaleCreature] = []
FemalesPopulation: List[FemaleCreature] = []
Population: Tuple[List[MaleCreature], List[FemaleCreature]] = ([], [])

def create_population() -> Population:
    """Returns: Tuple of two lists of male and female objects."""
    # males and females with random lifespan and age
    half_size = config.INITIAL_POPULATION // 2
    males = [MaleCreature() for _ in range(half_size)]
    females = [FemaleCreature() for _ in range(half_size)]
    females_num = len(females)

    # some number of random females have the CRISPR gene
    for _ in range(int(config.CRISPR_FEMALES * females_num)):
        random_index = random.randint(0, females_num - 1)
        female = females[random_index]
        female.crispr = True

        # Some of the females also have CRISPR resistance
        if random.random() < config.CRISPR_RESISTANCE_RATE:
            female.crispr_resistance = True

    return males, females
