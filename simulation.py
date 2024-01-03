import random
import population as pop
import reproduction as rep
import config

def simulate() -> dict[str, config.Vector]:
    """
    Records the relevant numbers after every cycle.
    Returns the numbers for each population category in a dict.
    """
    # build the population
    males, females = pop.create_population()

    # record the initial numbers
    population = len(males) + len(females)
    total_pop, crispr, sterile = [population], [config.CRISPR_FEMALES], [0]
    non_sterile, non_crispr = [0], [len(females) - config.CRISPR_FEMALES]
    crispr_resistance = [0]  # Initialize the list for CRISPR resistance
    
    # go through the given number of cycles
    for _ in range(config.CYCLES):
        # produce offspring
        male_kids, female_kids = rep.reproduce(males, females)
        # add children to population
        males += male_kids
        females += female_kids

        # increase the age of males and females
        for m in males:
            m.age += 1
        for f in females:
            f.age += 1

        # remove the dead individuals
        males = [m for m in males if not m.is_dead]
        females = [f for f in females if not f.is_dead]

        # remove extra population if any to stay within the population limit
        if (extra := len(males) + len(females) - config.POPULATION_LIMIT) > 0:
            males = random.sample(males, k=len(males) - extra // 2)
            females = random.sample(females, k=len(females) - extra // 2)

        # refresh the population number
        population = len(males) + len(females)

        # introduce CRISPR and CRISPR resistance in some of the females
        count = int((config.INITIAL_POPULATION // 2) * config.CRISPR_FEMALES)
        for f in females:
            if count <= 0 or f.crispr:
                continue
            f.crispr = True
            count -= 1

            # Introduce CRISPR resistance
            if random.random() < config.CRISPR_RESISTANCE_RATE:
                f.crispr_resistance = True

        # check sterile males and crispr females numbers
        crispr_fems = [f for f in females if f.crispr]
        sterile_males = [m for m in males if m.sterile]
        crispr_resistance_fems = [f for f in females if f.crispr_resistance]  # Count females with CRISPR resistance

        # record (append) the population numbers for this cycle
        crispr.append(len(crispr_fems))  # CRISPR females
        non_crispr.append(len(females) - len(crispr_fems))  # NON CRISPR females
        sterile.append(len(sterile_males))  # STERILE males
        non_sterile.append(len(males) - len(sterile_males))  # NON STERILE males
        crispr_resistance.append(len(crispr_resistance_fems))  # CRISPR Resistance females
        total_pop.append(population)  # total population

        # shuffle males and females
        random.shuffle(males)
        random.shuffle(females)

    return dict(
        crispr=crispr,
        sterile=sterile,
        non_sterile=non_sterile,
        non_crispr=non_crispr,
        total_pop=total_pop,
        crispr_resistance=crispr_resistance, 
    )
