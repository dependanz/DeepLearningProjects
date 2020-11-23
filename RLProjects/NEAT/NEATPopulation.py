from RLProjects.NEAT.NEAT import Genome, InnovationManager, connection_mutation,node_mutation,Crossover,weight_shift,feedforward
import random

class NEATPopulation:

    def __init__(self,n_x,n_y,pop,init_connections=""):
        self.genomes = []
        self.innovation_manager = InnovationManager()

        for i in range(pop):
            g = Genome(n_x, n_y,init_connections,self.innovation_manager)
            #connection_mutation(g,self.innovation_manager)
            self.genomes.append((g,0.0))

    def get_genomes(self):
        return list(map(lambda x:x[0],self.genomes))

    def get_fitness_values(self):
        return list(map(lambda x:x[1],self.genomes))

    def get_genome(self,i):
        return self.genomes[i][0]

    def get_fitness_value(self,i):
        return self.genomes[i][1]

    def population(self):
        return len(self.genomes)

    def evaluate_population(self,x,y,fitness_function,debug=False):
        test_yhat = []
        for g in range(len(self.genomes)):
            yhat = []
            for i in x:
                yhat.append(feedforward(i,self.genomes[g][0]))

            fitness = fitness_function(y,yhat)
            #print(f"fitness: {fitness}")
            self.genomes[g] = (self.genomes[g][0],fitness)
            test_yhat.append(yhat)

        if(debug):
            print(f"x: {x}")
            print(f"y: {y}")
            for i in range(len(self.genomes)):
                print(f"genome {i+1}")
                print(f"\tyhat: {test_yhat[i]}")
                print(f"\tfitness: {self.genomes[i][1]}")

        self.genomes.sort(key=lambda x: x[1],reverse=True)

    def proportional_selection(self,prob,elite_size):
        # random(0.45,1) 1-0.45 = 0.55
        # if 1 - random(i,1) <= 0.5 => good selection
        selection = []

        for i in range(elite_size):
            if(i >= len(self.genomes)): return selection
            selection.append(self.genomes[i])

        max_fitness = self.genomes[0][1]
        for g in range(elite_size,len(self.genomes)):
            p = self.genomes[g][1]/max_fitness
            #print(f"probability: {p}")
            t = 1 - random.uniform(p,1.0)
            #print(f"\tt: {t}\n\tprob: {prob}")
            if(t <= prob):
                #print("\tpicking this")
                selection.append(self.genomes[g])
        return selection

    def breed(self,selection,elite_size):
        offspring = []
        for i in range(elite_size):
            if(i >= len(selection)): break
            offspring.append(selection[i])

        #random.shuffle(selection)

        for i in range(len(selection)):
            parent1 = selection[i][0]
            parent2 = selection[len(selection)-1-i][0]
            child = Crossover(parent1,parent2,self.innovation_manager)
            offspring.append((child,0.0))

        return offspring

    def mutate(self,offspring,connection_mutate_rate,node_mutate_rate,elite_size=10,weight_shift_prob=0.25,shift_radius=0.01):
        if(elite_size > len(offspring)): return

        for i in range(len(offspring)):
            if (random.random() < connection_mutate_rate and i >= elite_size):
                connection_mutation(offspring[i][0],self.innovation_manager)

            if (random.random() < node_mutate_rate and i >= elite_size):
                node_mutation(offspring[i][0],self.innovation_manager)

            weight_shift(offspring[i][0], prob=weight_shift_prob, shift_radius=shift_radius)


    def next_generation(self,x,y,fitness_function,elite_size=10,selection_approach="proportion",selection_prob=0.5,connection_mutation_rate=0.35,node_mutation_rate=0.35,weight_shift_prob=0.25,shift_radius=0.01,debug=False):
        '''
        1) Rank Population based off of fitness values
        2) Fitness Proportionate Selection (with elitism) - probability of keep = fitness/(max_fitness) - from here we have our mating pool
        3) Crossover (Martin Gaye)
        4) Mutations (Connection and Node)
        5) next generation
        '''
        # evaluate population
        self.evaluate_population(x,y,fitness_function,debug)
        if(debug):
            for i in range(len(self.genomes)):
                print(self.genomes[i][0])
                print(f"\tdebug fitness: {self.genomes[i][1]}")

        #mating pool
        matingpool = None
        if(selection_approach == "proportion"):
            matingpool = self.proportional_selection(selection_prob,elite_size)
            #print(len(matingpool))

        #crossover
        offspring = self.breed(matingpool,elite_size)
        #print(offspring,len(offspring))

        #mutations
        offspring[0][0].visualize("Mutation Test Before", "Mutation Test Before")
        self.mutate(offspring,connection_mutation_rate,node_mutation_rate,weight_shift_prob=weight_shift_prob,shift_radius=shift_radius)
        offspring[0][0].visualize("Mutation Test After", "Mutation Test After")

        self.genomes = offspring

        #print("genomes: " + str(max(self.genomes,key=lambda x:x[1])))
        #print("offspring: " + str(max(offspring, key=lambda x: x[1])))
