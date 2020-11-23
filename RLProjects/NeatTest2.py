from RLProjects.NEAT.NEAT import feedforward
from RLProjects.NEAT.NEATPopulation import NEATPopulation
from RLProjects.NEAT.util import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import numpy as np
import random

#test is xor, fitness is found from categorical crossentropy

population_size = 200
connection_mutation_rate = 0.4
node_mutation_rate = 0.6
elite_size = 50
selection_prob = 0.4
weight_shift_prob = 0.25
shift_radius = 0.01

def fitness_function(y,yhat,epislon = 1e-8):
    loss = mean_squared_error(y,yhat)
    return 1/(loss + epislon)

def xor_random_tests(n = 20):
    p_x = [[0,0,1],[0,1,1],[1,0,1],[1,1,1]]
    p_y = [0,1,1,0]

    if(n == -1):
        return p_x,list(map(lambda x:[x],p_y))

    x = []
    y = []

    for i in range(n):
        j = random.randint(0,3)
        x.append(p_x[j])
        y.append([p_y[j]])

    return x,y

test_population = NEATPopulation(3, 1, population_size,init_connections="dense")

genomes = test_population.get_genomes()

test_x, test_y = xor_random_tests(50)

#ind_y = random.sample(list(np.arange(0.0,2.0,0.1)),len(test_y))

for i in range(10):
    # print(f"Genome {i + 1}:")
    # print(genomes[i])
    genomes[i].visualize("Geneome " + str(i + 1), 'Genome_' + str(i + 1))

generations = 0

#test_population.next_generation(test_x, test_y, fitness_function, connection_mutation_rate=connection_mutation_rate,node_mutation_rate=node_mutation_rate,elite_size=elite_size, selection_prob=selection_prob,weight_shift_prob=weight_shift_prob,shift_radius=shift_radius)
#test_population.evaluate_population(test_x, test_y, fitness_function)

for i in range(10):
    g = test_population.genomes[i]
    #print(f"genome {i+1} fitness: {g[1]}")
    g[0].visualize("Geneome " + str(i + 1), 'Genome_' + str(i + 1))

    debug_str = ""
    for j in range(len(test_x)):
        yhat = feedforward(test_x[j],g[0])
        debug_str += str(yhat) + " "
    #print(debug_str)
    #print(test_y)

while 1:
    print()
    choice = input(f"XOR NEAT TEST - Generation {generations}\n\tpopulation: {test_population.population()}\n\tmost fit genome fitness: {test_population.get_fitness_value(0)}\nCheck Genome [c]\nNext Generation [n]\nSkip Generations [s]\nPopulation Statistics [p]\nVisualize Genome [v]\nQuit [q]\n\t-> ")
    if(choice[0] == 'c'):
        print()
        c = int(input(f"Which Genome to check? [0 - {len(test_population.get_genomes()) - 1}]\n-> "))
        print(f"Genome {choice}:\n")
        d = False
        if (len(choice) > 1):
            if (choice[1] == 'd'):
                print(test_population.get_genome(c).debug())
                print(f"\tfitness: {test_population.get_fitness_value(c)}")
        else:
            print(str(test_population.get_genome(c)))
            print(f"\tfitness: {test_population.get_fitness_value(c)}")

    elif(choice == "n"):
        generations += 1
        test_population.next_generation(test_x, test_y, fitness_function, connection_mutation_rate=connection_mutation_rate,node_mutation_rate=node_mutation_rate,elite_size=elite_size, selection_prob=selection_prob,weight_shift_prob=weight_shift_prob,shift_radius=shift_radius)
        test_population.evaluate_population(test_x, test_y, fitness_function)

        for i in range(10):
            g = test_population.genomes[i]
            # print(f"genome {i+1} fitness: {g[1]}")
            g[0].visualize("Geneome " + str(i + 1), 'Genome_' + str(i + 1))
    elif(choice == "s"):
        gens = int(input(f"How many generations to jump? -> "))
        skip = generations + gens
        for i in range(gens):
            print(f"generation {generations}/{skip}")
            generations += 1
            test_population.next_generation(test_x, test_y, fitness_function, connection_mutation_rate=connection_mutation_rate,node_mutation_rate=node_mutation_rate,elite_size=elite_size, selection_prob=selection_prob,weight_shift_prob=weight_shift_prob,shift_radius=shift_radius)
            test_population.evaluate_population(test_x, test_y, fitness_function)

        for i in range(10):
            g = test_population.genomes[i]
            # print(f"genome {i+1} fitness: {g[1]}")
            g[0].visualize("Geneome " + str(i + 1), 'Genome_' + str(i + 1))
    elif(choice == "v"):
        print()
        choice = int(input(f"Which Genome to visualize? [0 - {len(test_population.get_genomes()) - 1}]\n-> "))
        g = test_population.genomes[choice]
        g[0].visualize("Visualization of Geneome " + str(choice + 1), 'V_Genome_' + str(choice + 1))
    elif(choice == "p"):
        print(f"Innovation Nodes: {len(test_population.innovation_manager.innovation_numbers)}")

    elif(choice == "q"):
        break