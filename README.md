# Onespecies.py

Simple model of evolution with a variable environment. Creatures and environment are each represented as ints from 1 to 100 (wrapping around, so 100 + 1 == 1), and the closer a creature's int value to the environment's, the higher the creature's fitness

# Twospecies.py

Modified version of onespecies.py with the environment replaced by a second sort of creature. Original creatures ("herbivores") are fittest when maximally close to new creatures ("herbs"); herbs are fittest when maximally far from herbivores.