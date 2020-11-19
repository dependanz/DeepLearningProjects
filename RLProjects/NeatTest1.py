from RLProjects.NEAT import Gene, Genome, InnovationManager, connection_mutation, node_mutation, feedforward, Crossover

# before doing the galaga project I wanna understand NEAT
# plus having my own implementation of NEAT will give me more control of my projects

x_n = 2
y_n = 1
x = [0,1]

num_genomes = 10
genomes = list()

for i in range(num_genomes):
    genomes.append(Genome(x_n,y_n))

innovationManager = InnovationManager()

generations = 2

for i in range(generations):
    for g in genomes:
        connection_mutation(g, innovationManager)
        node_mutation(g,innovationManager)

for i in range(len(genomes)):
    print("Genome " + str(i + 1))
    print(genomes[i])
    genomes[i].visualize("Geneome " + str(i+1), 'Genome_' + str(i+1))

offspring = Crossover(genomes[0],genomes[1],innovationManager,debug=True)
offspring.visualize("Offspring 0 & 1", "Offspring_0_1")

feedforward(x,offspring,debug=True)

#genomes[0].forward_propagate([0,1],[1],innovationManager)
#feedforward(x,genomes[0])
#feedforward(x,genomes[1])
#feedforward(x,genomes[2])
#feedforward(x,genomes[3])
#print(genomes[0].node_genes)