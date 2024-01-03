import random
import population as pop
import config


def produce_kids(
    sexes: list[str], sterile: bool = False, crispr: bool = False
) -> pop.Population:

    """Produce number of children based on their sex and genes."""

    males = [pop.MaleCreature(age=0, sterile=sterile) for sex in sexes if sex == "male"]
    females = [pop.FemaleCreature(age=0, crispr=crispr) for sex in sexes if sex == "female"]
    return males, females


def reproduce(males: pop.MalesPopulation, females: pop.FemalesPopulation) -> pop.Population:
    """
    males, females: lists of male and female objects.
    --------------------------------------------------------
    Performs one cycle of mating which returns two lists of
    children (male and female objects with age = 0).
    """
    male_offspring: pop.MalesPopulation = []
    female_offspring: pop.FemalesPopulation = []

    # loop through females
    for female in females:
        # randomly choose partners for this female
        partners_num = min(len(males), random.randrange(1, config.MAX_MALE_PARTNERS))
        partners = random.choices(males, k=partners_num)
        # if all partners are sterile this female will not produce offspring
        if all((partner.sterile for partner in partners)) and female.crispr_resistance:
            num_kids = random.randrange(1, config.MAX_OFFSPRING)
            sexes = [random.choice(("male", "female")) for _ in range(num_kids)]
            male_kids, female_kids = produce_kids(sexes, sterile=True, crispr=True)

            male_offspring += male_kids
            female_offspring += female_kids
            continue

        # prepare a pool of random sexes for this female's children
        num_kids = random.randrange(1, config.MAX_OFFSPRING)
        sexes = [random.choice(("male", "female")) for _ in range(num_kids)]

        # if the female parent doesn't have the CRISPR gene
        male_kids, female_kids = produce_kids(sexes)
        # if the female parent has the CRISPR gene
        if female.crispr:
            male_kids, female_kids = produce_kids(sexes, sterile=True, crispr=True)

        # add this female's children to the pool of population's children
        male_offspring += male_kids
        female_offspring += female_kids

    return male_offspring, female_offspring
