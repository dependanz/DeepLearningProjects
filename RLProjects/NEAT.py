import random
import math
from graphviz import Digraph

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
            self.node_genes[j] = 1

    def add_gene_io(self, input, output,innovation_manager):
        i_n = len(innovation_manager.innovation_numbers)
        g = Gene(input, output, True, i_n)
        innovation_manager.add_gene(g)
        self.connection_genes.append(g)

    def add_gene(self, g):
        self.connection_genes.append(g)

    def add_node(self,input, output,innovation_manager):
        n = len(self.node_genes)

        #set topology
        if(self.node_genes[input] == 0):
                self.node_genes[n] = 2
                if(self.node_genes[output] != 1):
                    self.node_genes[output] += 1
        else:
            self.node_genes[n] = self.node_genes[input] + 1
            if(not self.node_genes[output] == 1):
                if(self.node_genes[output] == self.node_genes[n]):
                    self.node_genes[output] += 1
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
                dot.edge(str(g.input),str(g.output))

        #print(dot.source)
        dot.render('NEAT_Visualizations/' + filepath + '.gv',view=view)

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