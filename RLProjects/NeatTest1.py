from RLProjects.NEAT import Gene, Genome, InnovationManager, connection_mutation, node_mutation

# before doing the galaga project I wanna understand NEAT
genome = Genome(3, 1)
innovationManager = InnovationManager()

connection_mutation(genome,innovationManager)

#print(genome)

connection_mutation(genome,innovationManager)

#print(genome)

for i in range(3):
    connection_mutation(genome,innovationManager)


#print(genome)
