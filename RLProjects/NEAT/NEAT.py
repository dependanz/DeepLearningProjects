import random
import math
from graphviz import Digraph
import numpy as np
import string

'''
  Connection Gene Class
'''


class Gene:
    def __init__(self, i=0, o=0, e=True, innov=0,weight_range=(-1,1),w=0):
        self.input = i
        self.output = o
        self.enabled = e
        self.innovation = innov
        if(w == 0):
            self.weight = random.uniform(weight_range[0],weight_range[1])
        else:
            self.weight = w

    def set_link(self, o):
        self.output = o

    def set_weight(self,w):
        self.weight = w

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def is_enabled(self):
        return self.enabled

    def __str__(self):
        return '[' + str(self.input) + "] -> [" + str(self.output) + ']\ninnovation: ' + str(self.innovation) + '\nenabled: ' + str(self.enabled) + "\n"


'''
  Neuron Node Class
  
  do i need this? for now just using dictionary
'''


class Node:
    def __init__(self, i=0, l=0):
        self.id = i
        self.layer = l


'''
  Genome Class
'''


class Genome:
    def __init__(self, n_x, n_y,init_connections="",innovation_manager=None,parents=[]):

        self.n_inputs = n_x
        self.n_outputs = n_y

        # list of genes
        self.connection_genes = list()

        # dictionary of nodes in our network (phenotype) (int node, int layer)
        self.node_genes = {}

        self.id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        self.parents = parents

        for i in range(n_x):
            self.node_genes[i] = 0

        for j in range(n_x, n_x + n_y):
            self.node_genes[j] = 1

        if (init_connections == "dense"):
            inno = 0
            for i in range(n_x):
                for j in range(n_x, n_x + n_y):
                    g = Gene(i, j, True, inno)
                    inno += 1
                    if (innovation_manager.contains_gene(i, j) == -1):
                        innovation_manager.add_gene(g)
                    self.connection_genes.append(g)

    def connection_exists_innov(self,innov):
        #print("connection test innov")
        for g in self.connection_genes:
            if(innov == g.innovation):
                return True
        return False

    def connection_exists_io(self,input,output):
        #print("connection test")
        for g in self.connection_genes:
            if(input == g.input and output == g.output):
                return True
        return False

    def add_gene_io(self, input, output,innovation_manager,w=0):
        if (self.connection_exists_io(input,output)):
            return
        if (input == output): return
        i_n = len(innovation_manager.innovation_numbers)
        g = Gene(input, output, True, i_n)
        if(w != 0):
            g.set_weight(w)
        if(innovation_manager.contains_gene(g.input,g.output) == -1):
            innovation_manager.add_gene(g)
        self.connection_genes.append(g)

    def add_gene(self, g):
        if (self.connection_exists_io(g.input,g.output)):
            return
        self.connection_genes.append(g)

    def add_gene_innov(self,innov,innovation_manager,enabled=True):
        if(self.connection_exists_innov(innov)):
            return
        g = innovation_manager.innovation_numbers[innov][1]
        g.visualize("Disable Test Before", "Disable Test Before")
        if(enabled):
            g.enable()
        else:
            g.disable()
            g.visualize("Disable Test After", "Disable Test After")
        self.connection_genes.append(g)

    def scan_fix(self,i):
        for gene in self.connection_genes:
            if(gene.input == i):
                if(self.node_genes[i] < self.node_genes[gene.output]): continue
                if(self.node_genes[i] == self.node_genes[gene.output]):
                    self.node_genes[gene.output] += 1
                    self.scan_fix(gene.output)

    def add_node(self,input, output,innovation_manager,weight=1):
        if(input == output): return

        n = len(self.node_genes)

        #set topology
        if(input in self.node_genes and output in self.node_genes):
            if(self.node_genes[input] == 0):
                    self.node_genes[n] = 2
                    if(self.node_genes[output] != 1 and self.node_genes[output] == self.node_genes[n]):
                        self.node_genes[output] += 1
                        innovation_manager.new_layer(self.node_genes[output])
                        #self.scan_fix(output)
            else:
                self.node_genes[n] = self.node_genes[input] + 1
                if(not self.node_genes[output] == 1):
                    if(self.node_genes[output] == self.node_genes[n]):
                        self.node_genes[output] += 1
                        innovation_manager.new_layer(self.node_genes[output])
        else:
            self.node_genes[n] = 2
        #check if in innovation manager first then do it

        c1 = innovation_manager.contains_gene(input, n)
        if (c1 != -1):
            #print("innovation number found for: " + str(in_node) + " " + str(out_node) + " -> " + str(c))
            g = Gene(input, n, True, c1,w=1)
            self.add_gene(g)
        else:
            #print("no existing innovation number found for: " + str(input) + " " + str(n) + " adding one")
            self.add_gene_io(input, n, innovation_manager,w=1)

        c2 = innovation_manager.contains_gene(n,output)
        if (c2 != -1):
            # print("innovation number found for: " + str(in_node) + " " + str(out_node) + " -> " + str(c))
            g = Gene(n,output, True, c2,w=weight)
            self.add_gene(g)
        else:
            #print("no existing innovation number found for: " + str(n) + " " + str(output) + " adding one")
            self.add_gene_io(n,output,innovation_manager,w=weight)


    def contains_gene(self,in_node,out_node):
        for i in range(len(self.connection_genes)):
            if(in_node == self.connection_genes[i].input and out_node == self.connection_genes[i].output):
                return True, i
        return False, -1

    def visualize(self,title,filepath,view=False,fitness=0.0):
        dot = Digraph(comment=title)
        dot.graph_attr['rankdir'] = 'LR'

        name = self.id

        if(len(self.parents) > 0):
            name += f" offspring of {self.parents[0]} and {self.parents[1]}"

        dot.node(f"fitness: {fitness} {name}")
        for node in self.node_genes:
            c = 'black'
            text = " layer " + str(self.node_genes[node])

            if(self.node_genes[node] == 0):
                c = 'green'
                text = " input"
            elif(self.node_genes[node] == 1):
                c = 'red'
                text = ' output'

            dot.node(str(node),str(node) + text,color=c)

        for g in self.connection_genes:
            if(g.enabled):
                dot.edge(str(g.input),str(g.output),str(g.weight))

        #print(dot.source)
        dot.render('NEAT_Visualizations/' + filepath + '.gv',view=view)

    def required_for_output(self,input_layer,output_layer):
        '''
        implementation from neat-python on github: https://github.com/CodeReclaimers/neat-python/blob/master
        '''
        required = set(output_layer)
        s = set(output_layer)
        while 1:
            t = set()
            for g in self.connection_genes:
                if(not g.enabled): continue
                if (g.input not in s and g.output in s):
                    t.add(g.input)

            if not t:
                break
            layer_nodes = set(x for x in t if x not in input_layer)
            if not layer_nodes:
                break

            required = required.union(layer_nodes)
            s = s.union(t)
        return required

    def phenotype(self):
        input_layer = []
        output_layer = []
        for n in self.node_genes.keys():
            if(self.node_genes[n] == 0):
                input_layer.append(n)
            elif(self.node_genes[n] == 1):
                output_layer.append(n)

        required = self.required_for_output(input_layer,output_layer)
        #output_layers = np.zeros((len(outputs),1))

        layers = []
        layers.append(set(input_layer))

        s = set(input_layer)
        while 1:
            c = set()
            for g in self.connection_genes:
                if(not g.enabled): continue
                if(g.input in s and g.output not in s):
                    c.add(g.output)

            t = set()
            for n in c:
                if (n in required):
                    for g in self.connection_genes:
                        if(not g.enabled or g.input not in s): continue
                        if(g.output == n):
                            t.add(n)
            if not t:
                break

            layers.append(t)
            s = s.union(t)

        layers.append(set(output_layer))
        return layers

    def debug(self):
        ret = ""
        for i in self.connection_genes:
            ret += str(i)
        return ret

    def __str__(self):
        ret = ""
        for i in self.connection_genes:
            if(i.enabled):
                ret += str(i)
        return ret


class InnovationManager:

    def __init__(self):
        # tuple of innovation numbers with connection Gene
        self.innovation_numbers = list()
        self.layers = 2

    def check_gene(self, g):
        # valid gene:
        #   check if connection pair exists in tuple pairing
        for i in self.innovation_numbers:
            if (i[1].input == g.input and i[1].output == g.output):
                if (i[0] != g.innovation):
                    return False
            if(i[0] == g.innovation):
                if (i[1].input != g.input or i[1].output != g.output):
                    return False
        return True

    def new_layer(self,test):
        if(test > self.layers):
            self.layers = test

    def contains_gene(self,in_node,out_node):
        for i in self.innovation_numbers:
            if (i[1].input == in_node and i[1].output == out_node):
                return i[0]
        return -1

    def add_gene(self,g,num=-1):
        if (num != -1):
            self.innovation_numbers.append((num, g))
        else:
            self.innovation_numbers.append((len(self.innovation_numbers), g))

'''
  Connection Mutation
'''
def connection_mutation(genome, innovation_manager):
    disabled_genes = []

    # print(f"connection mutate -> id: {genome.id}")

    for g in genome.connection_genes:
        if(not g.is_enabled()):
            disabled_genes.append((g.input,g.output))


    connection_genes = genome.connection_genes
    node_genes = genome.node_genes
    in_node = random.randint(0, len(node_genes)-1)
    out_node = random.randint(0, len(node_genes)-1)

    #contains_gene, gene_idx = genome.contains_gene(in_node, out_node)

    while (in_node == out_node) or (node_genes[out_node] == 0) or (node_genes[in_node] == 1):
        # if(contains_gene):
        #     if(not genome.connection_genes[gene_idx].is_enabled()):
        #         break
        in_node = random.randint(0, len(node_genes) - 1)
        out_node = random.randint(0, len(node_genes) - 1)
        # contains_gene, gene_idx = genome.contains_gene(in_node, out_node)

    # if connection exists for the genome ignore connection mutation
    # if connection doesn't exist look for it in innovation_manager
    #   if it is in innovation_manager then use that connection
    #   else assign the connection gene an innovation number and add it to the innovation_manager

    contains_gene,gene_idx = genome.contains_gene(in_node,out_node)

    if(not contains_gene):
        #print("doesn't contain: " + str(in_node) + " " + str(out_node) + " look in innovation manager")
        c = innovation_manager.contains_gene(in_node,out_node)
        if(c != -1):
            #print("innovation number found for: " + str(in_node) + " " + str(out_node) + " -> " + str(c))
            g = Gene(in_node, out_node, True, c)
            genome.add_gene(g)
        else:
            #print("no existing innovation number found for: " + str(in_node) + " " + str(out_node) + " adding one")
            genome.add_gene_io(in_node,out_node,innovation_manager)
    else:
        #print("ignoring connection: " + str(in_node) + " " + str(out_node))
        if(genome.connection_genes[gene_idx].is_enabled()):
            genome.connection_genes[gene_idx].disable()
        else:
            genome.connection_genes[gene_idx].enable()
    #print(genome)


'''
  Node Mutation:
      1) Choose random connection gene to be split
      2) Disable connection
'''


def node_mutation(genome,innovation_manager):
    if(len(genome.connection_genes) == 0): return
    connection_genes = genome.connection_genes
    node_genes = genome.node_genes

    # print(f"node mutate -> id: {genome.id}")

    g = connection_genes[random.randint(0,len(connection_genes) - 1)]
    if(not g.enabled): return
    #genome.visualize("Disable Test Before", "Disable Test Before")
    g.disable()
    #genome.visualize("Disable Test After", "Disable Test After")

    in_split = g.input
    out_split = g.output

    genome.add_node(in_split,out_split,innovation_manager,weight=g.weight)

    genome.visualize("Disable Test After AFter", "Disable Test After AFter")
    #print(genome)

'''
    Crossover
'''
def Crossover(parent1,parent2,innovation_manager,prob=0.5,debug=False):
    if(debug):
        print("Crossover:")

    offspring = Genome(parent1[0].n_inputs,parent1[0].n_outputs,parents=[parent1[0].id,parent2[0].id])

    genome1 = parent1[0]
    genome2 = parent2[0]
    fitness1 = parent1[1]
    fitness2 = parent2[1]

    i = 0
    j = 0

    n1 = len(genome1.connection_genes)
    n2 = len(genome2.connection_genes)

    g1_innov = 0
    g2_innov = 0

    for g1 in range(n1):
        if (genome1.connection_genes[g1].innovation > g1_innov):
            g1_innov = genome1.connection_genes[g1].innovation

    for g2 in range(n2):
        if (genome2.connection_genes[g2].innovation > g2_innov):
            g2_innov = genome2.connection_genes[g2].innovation

    while (i < n1 and j < n2):
        if (i >= n1 and j < n2):
            if(fitness1 > fitness2): break
            add_cycle_check(offspring, genome1.connection_genes[j])
            j += 1
            continue
        elif (i < n1 and j >= n2):
            if (fitness1 < fitness2): break
            add_cycle_check(offspring, genome1.connection_genes[i])
            i += 1
            continue

        if (genome1.connection_genes[i].innovation == genome2.connection_genes[j].innovation):
            if (random.random() < prob):
                add_cycle_check(offspring, genome1.connection_genes[i])
            else:
                add_cycle_check(offspring, genome2.connection_genes[j])
            i += 1
            j += 1
        else:
            if (genome1.connection_genes[i].innovation > genome2.connection_genes[j].innovation):
                add_cycle_check(offspring, genome2.connection_genes[j])
                j += 1
            elif (genome1.connection_genes[i].innovation < genome2.connection_genes[j].innovation):
                add_cycle_check(offspring, genome1.connection_genes[i])
                i += 1

    if(debug):
        for g in offspring.connection_genes:
            print(f"Offspring")
            print(f"\tInnov: {g.innovation}\t[{g.input}] -> [{g.output}]")
            print(f"\tEnabled: {g.enabled}")

    # for g in parent1.connection_genes:
    #     print(f"[{g.input}] -> [{g.output}]")
    #     print(f"\t{g.innovation}")
    return offspring

def weight_shift(genome,prob=0.15,shift_radius=0.01):
    for connection in genome.connection_genes:
        if(random.random() <= 0.15):
            connection.weight += random.uniform(-shift_radius,shift_radius)

def add_cycle_check(genome,gene):
    if(gene.input == gene.output): return False

    gene_cpy = Gene(gene.input,gene.output,gene.enabled,gene.innovation,w=gene.weight)

    connections = genome.connection_genes
    nodes = genome.node_genes
    makes_cycle = False
    visited = set()
    visited.add(gene.output)

    while 1:
        #print("add_cycle_check loop")
        num_added = 0
        for g in connections:
            if(g.input in visited and g.output not in visited):
                if(g.output == gene.input):
                    makes_cycle = True
                    break
                visited.add(g.output)
                num_added += 1

        if(makes_cycle or num_added == 0):
            break
    if(not makes_cycle):
        genome.add_gene(gene_cpy)

    return True

def feedforward(x,genome,debug=False):
    phenotype = genome.phenotype()
    layers = {}
    if(debug):
        print("Phenotype: ")
        print(phenotype)

    i_count = 0
    o_count = 0
    for n in genome.node_genes.keys():
        if(genome.node_genes[n] == 0):
            i_count += 1
        if(genome.node_genes[n] == 1):
            o_count += 1

    if(i_count != len(x)):
        print("Error: input size doesn't match input layer (expected: " + str(i_count) + ")")
        return

    for l in phenotype:
        for n in l:
            layers[n] = 0.0

    for i in range(i_count):
        layers[i] = x[i]

    if(debug):
        print(layers)

    for l in range(len(phenotype)-1):
        for n in phenotype[l]:
            for g in genome.connection_genes:
                if(not g.enabled or g.input != n): continue
                if(g.output in genome.node_genes):
                    if(genome.node_genes[g.output] == 1): continue
                if(g.output in layers and g.input in layers):
                    layers[g.output] += g.weight * layers[g.input]
                if(debug):
                    print(f"{g.input} -> {g.output}: {layers}")

    #evaluate the output nodes last
    for n in phenotype[-1]:
        for g in genome.connection_genes:
            if(not g.enabled or g.output != n): continue
            if (g.output in layers and g.input in layers):
                layers[g.output] += g.weight * layers[g.input]
            if (debug):
                print(f"{g.input} -> {g.output}: {layers}")

    if(debug):
        print(layers)
    outputs = []

    for i in range(i_count,i_count+o_count):
        outputs.append(layers[i])
    return outputs
