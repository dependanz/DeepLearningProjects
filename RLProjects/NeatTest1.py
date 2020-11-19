from RLProjects.NEAT import Gene, Genome, InnovationManager, connection_mutation, node_mutation, feedforward, Crossover

# before doing the galaga project I wanna understand NEAT
# plus having my own implementation of NEAT will give me more control of my projects

x_n = 2
y_n = 1
x = [1,1]
y = [0]

num_genomes = 10
genomes = list()

for i in range(num_genomes):
    genomes.append(Genome(x_n,y_n))

innovationManager = InnovationManager()

generations = 5

for i in range(generations):
    for g in genomes:
        connection_mutation(g, innovationManager)
        node_mutation(g,innovationManager)

for i in range(len(genomes)):
    #print("Genome " + str(i + 1))
    #print(genomes[i])
    genomes[i].visualize("Geneome " + str(i+1), 'Genome_' + str(i+1))

offspring1 = Crossover(genomes[0],genomes[1],innovationManager,debug=True)
offspring1.visualize("Offspring 0 & 1", "Offspring_0_1")

offspring2 = Crossover(genomes[2],genomes[3],innovationManager,debug=True)
offspring2.visualize("Offspring 2 & 3", "Offspring_2_3")

feedforward(x,offspring1,debug=True)
feedforward(x,offspring2,debug=True)

offspring3 = Crossover(offspring1,offspring2,innovationManager,debug=True)
offspring3.visualize("Offspring of offsprings 1 & 2", "Offspring_of_offspring_2_3")
feedforward(x,offspring3,debug=True)
#genomes[0].forward_propagate([0,1],[1],innovationManager)
#feedforward(x,genomes[0])
#feedforward(x,genomes[1])
#feedforward(x,genomes[2])
#feedforward(x,genomes[3])
#print(genomes[0].node_genes)