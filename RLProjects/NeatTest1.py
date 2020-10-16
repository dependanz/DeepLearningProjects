from RLProjects.NEAT import Gene, Genome, InnovationManager, connection_mutation, node_mutation

# before doing the galaga project I wanna understand NEAT
genome = Genome(3, 1)
innovationManager = InnovationManager()

connection_mutation(genome,innovationManager)
connection_mutation(genome,innovationManager)
node_mutation(genome,innovationManager)