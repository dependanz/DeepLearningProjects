import random
import math
from graphviz import Digraph
import numpy as np

'''
  Connection Gene Class
'''


class Gene:
    def __init__(self, i=0, o=0, e=True, innov=0):
        self.input = i
        self.output = o
        self.enabled = e
        self.innovation = innov
        self.weight = random.randint(1, 200) * 0.01

    def set_link(self, o):
        self.output = o

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def __str__(self):
        return '[' + str(self.input) + "] -> [" + str(self.output) + ']\ninnovation: ' + str(self.innovation) + '\n'


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
    def __init__(self, n_x, n_y):

        self.n_inputs = n_x
        self.n_outputs = n_y

        # list of genes
        self.connection_genes = list()

        # dictionary of nodes in our network (phenotype) (int node, int layer)
        self.node_genes = {}

        for i in range(n_x):
            self.node_genes[i] = 0

        for j in range(n_x, n_x + n_y):
            self.node_genes[j] = 1

    def add_gene_io(self, input, output,innovation_manager):
        i_n = len(innovation_manager.innovation_numbers)
        g = Gene(input, output, True, i_n)
        innovation_manager.add_gene(g)
        self.connection_genes.append(g)

    def add_gene(self, g):
        self.connection_genes.append(g)

    def add_gene_innov(self,innov,innovation_manager,enabled=True):
        g = innovation_manager.innovation_numbers[innov][1]
        if(enabled):
            g.enable()
        else:
            g.disable()
        self.connection_genes.append(g)

    def scan_fix(self,i):
        for gene in self.connection_genes:
            if(gene.input == i):
                if(self.node_genes[i] < self.node_genes[gene.output]): continue
                if(self.node_genes[i] == self.node_genes[gene.output]):
                    self.node_genes[gene.output] += 1
                    self.scan_fix(gene.output)

    def add_node(self,input, output,innovation_manager):
        n = len(self.node_genes)

        #set topology
        if(self.node_genes[input] == 0):
                self.node_genes[n] = 2
                if(self.node_genes[output] != 1 and self.node_genes[output] == self.node_genes[n]):
                    self.node_genes[output] += 1
                    innovation_manager.new_layer(self.node_genes[output])
                    self.scan_fix(output)
        else:
            self.node_genes[n] = self.node_genes[input] + 1
            if(not self.node_genes[output] == 1):
                if(self.node_genes[output] == self.node_genes[n]):
                    self.node_genes[output] += 1
                    innovation_manager.new_layer(self.node_genes[output])
        #check if in innovation manager first then do it

        c1 = innovation_manager.contains_gene(input, n)
        if (c1 != -1):
            #print("innovation number found for: " + str(in_node) + " " + str(out_node) + " -> " + str(c))
            g = Gene(input, n, True, c1)
            self.add_gene(g)
        else:
            #print("no existing innovation number found for: " + str(in_node) + " " + str(out_node) + " adding one")
            self.add_gene_io(input, n, innovation_manager)

        c2 = innovation_manager.contains_gene(n,output)
        if (c2 != -1):
            # print("innovation number found for: " + str(in_node) + " " + str(out_node) + " -> " + str(c))
            g = Gene(n,output, True, c2)
            self.add_gene(g)
        else:
            # print("no existing innovation number found for: " + str(in_node) + " " + str(out_node) + " adding one")
            self.add_gene_io(n,output,innovation_manager)


    def contains_gene(self,in_node,out_node):
        for i in self.connection_genes:
            if(in_node == i.input and out_node == i.output):
                return True
        return False

    def visualize(self,title,filepath,view=False):
        dot = Digraph(comment=title)
        dot.graph_attr['rankdir'] = 'LR'
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

    def add_gene(self,g):
        self.innovation_numbers.append((len(self.innovation_numbers),g))

'''
  Connection Mutation
'''
def connection_mutation(genome, innovation_manager):
    connection_genes = genome.connection_genes
    node_genes = genome.node_genes
    in_node = random.randint(0, len(node_genes)-1)
    out_node = random.randint(0, len(node_genes)-1)

    while (in_node == out_node) or (node_genes[out_node] == 0) or (node_genes[in_node] == 1) or (node_genes[in_node] >= node_genes[out_node]):
        in_node = random.randint(0, len(node_genes) - 1)
        out_node = random.randint(0, len(node_genes)-1)

    # if connection exists for the genome ignore connection mutation
    # if connection doesn't exist look for it in innovation_manager
    #   if it is in innovation_manager then use that connection
    #   else assign the connection gene an innovation number and add it to the innovation_manager

    if(not genome.contains_gene(in_node,out_node)):
        #print("doesn't contain: " + str(in_node) + " " + str(out_node) + " look in innovation manager")
        c = innovation_manager.contains_gene(in_node,out_node)
        if(c != -1):
            #print("innovation number found for: " + str(in_node) + " " + str(out_node) + " -> " + str(c))
            g = Gene(in_node, out_node, True, c)
            genome.add_gene(g)
        else:
            #print("no existing innovation number found for: " + str(in_node) + " " + str(out_node) + " adding one")
            genome.add_gene_io(in_node,out_node,innovation_manager)
    #else:
        #print("ignoring connection: " + str(in_node) + " " + str(out_node))

    #print(genome)


'''
  Node Mutation:
      1) Choose random connection gene to be split
      2) Disable connection
'''


def node_mutation(genome,innovation_manager):
    connection_genes = genome.connection_genes
    node_genes = genome.node_genes

    g = connection_genes[random.randint(0,len(connection_genes) - 1)]
    g.disable()

    in_split = g.input
    out_split = g.output

    genome.add_node(in_split,out_split,innovation_manager)

    #print(genome)

'''
    Crossover
'''
def Crossover(parent1,parent2,innovation_manager,debug=False):
    print("Crossover:")

    offspring = Genome(parent1.n_inputs,parent1.n_outputs)

    for i in range(len(innovation_manager.innovation_numbers)):
        p1 = None
        p2 = None
        for g in parent1.connection_genes:
            if(g.innovation != i): continue
            if(debug):
                print(f"Parent 1")
                print(f"\tInnov: {g.innovation}\t[{g.input}] -> [{g.output}]")
                print(f"\tEnabled: {g.enabled}")
            p1 = g
            break

        for g in parent2.connection_genes:
            if(g.innovation != i): continue
            if(debug):
                print(f"Parent 2")
                print(f"\tInnov: {g.innovation}\t[{g.input}] -> [{g.output}]")
                print(f"\tEnabled: {g.enabled}")
            p2 = g
            break

        if(p1 != None and p2 != None):
            if(not p1.enabled):
                offspring.add_gene(p1)
            elif(not p2.enabled):
                offspring.add_gene(p2)
            else:
                offspring.add_gene_innov(i, innovation_manager)
        elif(p1 != None):
            offspring.add_gene(p1)
        elif (p2 != None):
            offspring.add_gene(p2)

    if(debug):
        for g in offspring.connection_genes:
            print(f"Offspring")
            print(f"\tInnov: {g.innovation}\t[{g.input}] -> [{g.output}]")
            print(f"\tEnabled: {g.enabled}")

    # for g in parent1.connection_genes:
    #     print(f"[{g.input}] -> [{g.output}]")
    #     print(f"\t{g.innovation}")
    return offspring


def feedforward(x,genome,debug=False):
    phenotype = genome.phenotype()
    layers = {}
    print(phenotype)

    i_count = 0
    for n in genome.node_genes.keys():
        if(genome.node_genes[n] == 0):
            i_count += 1

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

    for l in phenotype:
        for n in l:
            for g in genome.connection_genes:
                if(not g.enabled or g.input != n): continue
                layers[g.output] += g.weight * layers[g.input]
                if(debug):
                    print(f"{g.input} -> {g.output}: {layers}")

    print(layers)