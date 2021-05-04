from RLProjects.NEAT.NEAT import Genome, InnovationManager, connection_mutation,node_mutation,Crossover,weight_shift,feedforward
from RLProjects.NEAT.util import progressBar, collapse_list_of_lists
import random

class NEATPopulation:

    def __init__(self,n_x,n_y,pop,init_connections=""):
        self.genomes = []
        self.species = []

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
        for g in progressBar(range(len(self.genomes)), prefix = 'Evaluating Population:', suffix = 'Complete', length = 50):
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

    def proportional_selection(self,genomes,prob,selection_keep_size):
        # random(0.45,1) 1-0.45 = 0.55
        # if 1 - random(i,1) <= 0.5 => good selection
        if(selection_keep_size >= len(genomes)): return genomes
        selection = []

        for i in range(selection_keep_size):
            if(i >= len(genomes)): return selection
            selection.append(genomes[i])

        max_fitness = genomes[0][1]
        #progressBar(range(elite_size,len(genomes)), prefix = 'Proportional Selection:', suffix = 'Complete', length = 50,off=True)
        for g in range(selection_keep_size,len(genomes)):
            #print(f"\t\t{g}")
            p = genomes[g][1]/max_fitness
            #print(f"probability: {p}")
            t = 1 - random.uniform(p,1.0)
            #print(f"\tt: {t}\n\tprob: {prob}")
            if(t <= prob):
                #print("\tpicking this")
                selection.append(genomes[g])
        return selection

    def breed(self,selection):
        offspring = []

        # for i in range(elite_size):
        #     if(i >= len(selection)): break
        #     offspring.append(selection[i])

        random.shuffle(selection)

        for i in range(len(selection)-1):
            parent1 = selection[i]
            parent2 = selection[i+1]
            child = Crossover(parent1,parent2,self.innovation_manager)
            offspring.append((child,0.0))
        offspring.append((Crossover(selection[len(selection)-1],selection[0],self.innovation_manager), 0.0))

        return offspring

    def mutate(self,offspring,connection_mutate_rate,node_mutate_rate,elite_size=10,weight_shift_prob=0.25,shift_radius=0.01):
        if(elite_size > len(offspring)): return

        # for i in range(elite_size):
        #     weight_shift(offspring[i][0], prob=weight_shift_prob, shift_radius=shift_radius)

        for i in range(elite_size,len(offspring)):
            if (random.random() < connection_mutate_rate and i >= elite_size):
                #print(f"connection mutate -> id: {offspring[i][0].id}")
                connection_mutation(offspring[i][0],self.innovation_manager)

            if (random.random() < node_mutate_rate and i >= elite_size):
                #print(f"node mutate -> id: {offspring[i][0].id}")
                node_mutation(offspring[i][0],self.innovation_manager)

            weight_shift(offspring[i][0], prob=weight_shift_prob, shift_radius=shift_radius)

    def compatibility_distance(self,genome1,genome2,c1=1,c2=1,c3=1,epsilon=10e-5):
        # 91 species 2
        # AGXUJT =
        # P949NZ

        E = 0
        D = 0
        W = 0
        i = 0
        j = 0

        n_matching = 0
        n1 = len(genome1.connection_genes)
        n2 = len(genome2.connection_genes)
        N = max(n1,n2)

        g1_innov = 0
        g2_innov = 0

        for g1 in range(n1):
            if(genome1.connection_genes[g1].innovation > g1_innov):
                g1_innov = genome1.connection_genes[g1].innovation

        for g2 in range(n2):
            if(genome2.connection_genes[g2].innovation > g2_innov):
                g2_innov = genome2.connection_genes[g2].innovation

        while(i < n1 and j < n2):
            if(i >= n1 and j < n2):
                E += 1
                j += 1
                continue
            elif(i < n1 and j >= n2):
                E += 1
                i += 1
                continue

            if (genome1.connection_genes[i].innovation == genome2.connection_genes[j].innovation):
                W += abs(genome1.connection_genes[i].weight - genome2.connection_genes[j].weight)
                n_matching += 1
                i += 1
                j += 1
            else:
                D += 1
                if(genome1.connection_genes[i].innovation > genome2.connection_genes[j].innovation):
                    j += 1
                elif(genome1.connection_genes[i].innovation < genome2.connection_genes[j].innovation):
                    i += 1

        if(n_matching > 0):
            return (E*c1/(N+epsilon)) + (D*c2/(N+epsilon)) + (W*c3)/n_matching
        return (E*c1/(N+epsilon)) + (D*c2/(N+epsilon))

    def speciate(self,c_thresh=0.3):
        for g in progressBar(self.genomes, prefix = 'Speciating:', suffix = 'Complete', length = 50):
            if(len(self.species) == 0):
                self.species.append([g])
                continue

            c = 9999999
            index = -1
            for s in range(len(self.species)):
                c_d = self.compatibility_distance(g[0],random.choice(self.species[s])[0])
                if(c_d <= c and c_d < c_thresh):
                    c = c_d
                    index = s

            if(index == -1):
                self.species.append([g])
            else:
                self.species[index].append(g)

    def remove_least_fit(self,keep_percent):
        collapsed = []
        for s in range(len(self.species)):
            for g in range(len(self.species[s])):
                collapsed.append((self.species[s][g],s))

        sorted(collapsed,key=lambda x:x[0][1])

        for i in range(int(keep_percent*len(collapsed)),len(collapsed)):
            s = collapsed[i][1]
            del self.species[s][-1]

    def next_generation(self,x,y,fitness_function,elite_size=10,
                        selection_approach="proportion",selection_prob=0.5,selection_keep_size=5,connection_mutation_rate=0.35,node_mutation_rate=0.35,
                        weight_shift_prob=0.25,shift_radius=0.01,c_thresh=0.3,keep_percent=0.5,debug=False):
        '''
        1) Rank Population based off of fitness values
        1b) Speciation
        2) Fitness Proportionate Selection (with elitism) - probability of keep = fitness/(max_fitness) - from here we have our mating pool
        3) Crossover (Martin Gaye)
        4) Mutations (Connection and Node)
        5) next generation
        '''
        # evaluate population
        self.evaluate_population(x,y,fitness_function,debug)
        print("test before: " + str(len(self.genomes)))
        #speciation
        print("\tnumber of species before: " + str(len(self.species)))
        self.speciate(c_thresh=c_thresh)
        print("\tnumber of species after: " + str(len(self.species)))

        #adjust fitness and sort by fitness per species
        sorted_species = []
        for s in range(len(self.species)):
            sorted_species.append([])
            for g in range(len(self.species[s])):
                sorted_species[s].append((self.species[s][g][0], self.species[s][g][1] / (len(self.species[s]))))
            if(len(sorted_species[s]) == 0):
                continue
            sorted(sorted_species[s], key=lambda x: x[1])

            for g in sorted_species[s]:
                print(f"species {s+1}: {g[0].id}")
            #sorted_species[s] = sorted_species[s][0:keep_size]
        #self.genomes = collapse_list_of_lists(sorted_species,s=True,key=lambda x:x[1])

        self.species = sorted_species
        # remove the least fit organisms using the keep_percent hyperparameter
        self.remove_least_fit(keep_percent)

        if(debug):
            for i in range(len(self.genomes)):
                print(self.genomes[i][0])
                print(f"\tdebug fitness: {self.genomes[i][1]}")

        #mating pool
        matingpool = []
        if (selection_approach == "proportion"):
            # print(len(matingpool))
            for s in range(len(self.species)):
                if(len(self.species[s]) == 0):
                    continue
                print(f"\tspecies pop size -> {len(sorted_species[s])}")
                matingpool.append(self.proportional_selection(sorted_species[s],selection_prob,selection_keep_size))
        self.species = matingpool

        #crossover
        offspring = []

        for g in range(elite_size):
            offspring.append(self.genomes[g])

        for s in range(len(self.species)):
            print("\tbefore breed: " + str(len(matingpool[s])))
            s_breed = self.breed(matingpool[s])
            print("\tafter breed: " + str(len(s_breed)))
            offspring += s_breed
        print("test after: " + str(len(offspring)))
        #print(offspring,len(offspring))
        sorted(offspring, key=lambda x: x[1])

        #mutations
        #offspring[0][0].visualize("Mutation Test Before", "Mutation Test Before")
        self.mutate(offspring,connection_mutation_rate,node_mutation_rate,weight_shift_prob=weight_shift_prob,shift_radius=shift_radius,elite_size=elite_size)
        #offspring[0][0].visualize("Mutation Test After", "Mutation Test After")

        self.genomes = offspring

        print(f"Top two compatibility distance: {self.compatibility_distance(self.genomes[0][0],self.genomes[1][0])}")

        print(len(self.species))
        for s in self.species:
            print("\t-> " + str(len(s)))

        # for s in range(len(self.species)):
        #     for g in range(2):
        #         if(g >= len(self.species[s])): break
        #         self.species[s][g][0].visualize(f"Species {s+1} Genome {g+1}", f"Species {s+1} Genome {g+1}")

        # for s in range(len(self.species)):
        #     for g in self.species[s]:
        #         print()
        #print("genomes: " + str(max(self.genomes,key=lambda x:x[1])))
        #print("offspring: " + str(max(offspring, key=lambda x: x[1])))
