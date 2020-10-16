import random
import math
'''
  Connection Gene Class
'''


class Gene:
    def __init__(self, i=0, o=0, e=True, innov=0):
        self.input = i
        self.output = o
        self.enabled = e
        self.innovation = innov
        self.weight = random.randint(-100, 100) * 0.01

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

        # list of genes
        self.connection_genes = list()

        # dictionary of nodes in our network (phenotype) (int node, int layer)
        self.node_genes = {}

        for i in range(n_x):
            self.node_genes[i] = 0

        for j in range(n_x, n_x + n_y):
            self.node_genes[j] = 2

    def add_gene(self, input, output, innovation_manager):
        i_n = len(innovation_manager.innovation_numbers)
        g = Gene(input, output, True, i_n)
        if (innovation_manager.check_gene(g)):
            innovation_manager.add_gene(g)
            self.connection_genes.append(g)
            return True
        else:
            return False

    def add_node(self,input, output,innovation_manager):
        n = len(self.node_genes)
        self.node_genes[n] = 1
        self.add_gene(input,n,innovation_manager)
        self.add_gene(n,output,innovation_manager)

    def __str__(self):
        ret = ""
        for i in self.connection_genes:
            if(i.enabled):
                ret += str(i)
        return ret


'''
  I don't believe i need this
'''


class InnovationManager:

    def __init__(self):
        # tuple of innovation numbers with connection Gene
        self.innovation_numbers = list()

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
    while (in_node == out_node) or (node_genes[out_node] == 0):
        in_node = random.randint(0, len(node_genes) - 1)
        out_node = random.randint(0, len(node_genes)-1)

    i = 0
    while (not genome.add_gene(in_node,out_node,innovation_manager)) and i < max(len(connection_genes),10):
        in_node = random.randint(0, len(node_genes)-1)
        while (in_node == out_node) or (node_genes[out_node] == 0):
          in_node = random.randint(0, len(node_genes) - 1)
          out_node = random.randint(0, len(node_genes) - 1)

        i += 1
        #print("test",in_node,out_node)

    print(genome)


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

    print(genome)