from RLProjects.NEAT import Gene, Genome, InnovationManager, connection_mutation, node_mutation

# before doing the galaga project I wanna understand NEAT

x_n = 2
y_n = 1
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
    print("Genome " + str(i + 1))
    print(genomes[i])
    genomes[i].visualize("Geneome " + str(i+1), 'Genome_' + str(i+1))

#print(genomes[0].node_genes)