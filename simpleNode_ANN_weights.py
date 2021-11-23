import random
import string
"""
atilla k - simple ANN with weights using Cary Jardin's pseudo code
"""
NODE_COUNT_PER_LAYER = [4, 3, 2]
#NODE_CHR = 'A'
#STR_CHR = 'A'

class Node():
    def __init__(self, layer, same_layer):
        #set the children, weight & connection weight attributes to empty arrays
        self.children = []
        self.weight = []
        self.children_conn_weights = []
        #curr_layer = NODE_COUNT_PER_LAYER[layer]
        if layer == 999:
            self.node_name = 'Layer_master'
        else:
            offset = 0
            #print('layer before loop--> ', layer)
            #here get the offset to add to the letter 'A'
            for  i in range(layer):
                #print('layer--> ', i)
                offset = offset + NODE_COUNT_PER_LAYER[i-1]

           # Set a random name.. this is just to OUTPUT out.. use whatever naming you want
            #self.node_name = ' '.join([random.choice(string.ascii_uppercase) for i in range(3)])

            #set the name, ex: layer 1 has four nodes --> A, B, C, D   layer 2 has three nodes
            #first node of layer 2 is 'A' + offset=4
            self.node_name = ''.join(['Layer_', str(layer+1), '_', chr((ord('A')) + offset + same_layer )])

    def make_children(self, current_layer, nodes_per_layer_map, inLayer_offset):

        #when to terminate the recursive call
        if current_layer >= len(nodes_per_layer_map):
            #print("...end...")
            return
        #needed a varible to keep the offset when in the same node
        inLayer_offset = NODE_COUNT_PER_LAYER[current_layer] - 1
        #create the children for this node --> add to the list
        for i in range(nodes_per_layer_map[current_layer]):
            #print(i, ' --> ', self.node_name)
            #nodes_inlayer = nodes_inlayer + 1
            self.children.append(Node(current_layer, inLayer_offset) )
            print('*nodes in layer', inLayer_offset)
            inLayer_offset += 1

        #first child is the first in the children list
        first_born = self.children[0]
        #connect the first child
        first_born.make_children(current_layer+1, nodes_per_layer_map, inLayer_offset)
        #copy the connections from the first child(from [0]) to each child
        for i in range(1, len(self.children) ):
            self.children[i].children = first_born.children[:]
            #print('children: ', self.children[i].children, 'end')

    def adjust_child_weights(self):
        #stop condition for the recursive call
        if len(self.children) <= 0:
            return
        #initialize children connection weights array to empty & loop recursively
        self.children_conn_weights = []
        #print("*** weights--> ", self.children_conn_weights)

        for i in range(len(self.children)):
            self.children_conn_weights.append(random.uniform(0, 1))
            #print("weights--> ", self.children_conn_weights[i])
            self.children[i].adjust_child_weights()             #recursive call
        #print(self.children_conn_weights)

    def output_children(self, layer):
        indent1 = '-' * ( 2**(layer + 1) ) + '>'
        indent2 = ' ' * (2**(layer + 1)) * 2
        #indent = '   ' * layer

        #recursive output
        if len(self.children) <= 0:
            print ('|', indent1, self.node_name)
            return
        #print('\n')
        print('|', indent1, self.node_name, "is connected to ")
        #print('{:<0}'.format(indent, self.node_name, "is connected to") )

        for i in range(len(self.children)):
           #print('\n')
            print('| ')
            #print(indent, ' with weight ', self.children_conn_weights[i])
            self.children[i].output_children( layer+1 )

            #print('***', end='')
            if i < len(self.children_conn_weights):
                #print('***', end='')
                print( '|', indent2, ' with weight ', "%.6f" % self.children_conn_weights[i])
                #pass
        #print('\n')
if __name__ == '__main__':

    master_layer = 999   #this is to distinguish the master layer
    node_layer = 0      #layers that are not the master
    index_samelayer = 0;
    layer_nodes = 0
    node = []       #node is set to empty list
    master_node = Node(master_layer, index_samelayer)
    #name = chr(ord(name) + 1)

    my_first_node = Node(node_layer, index_samelayer)
    my_first_node.make_children(1, NODE_COUNT_PER_LAYER, layer_nodes)
    master_node.children.append(my_first_node)

    #duplicate the first node and add the same children connections to these nodes
    for i in range(0 , len(NODE_COUNT_PER_LAYER) ):
        #name = chr(ord(name) + 1)
        #node_layer = i
        index_samelayer += 1        #increment the index by one so that name is also one higher letter
        new_node = Node(node_layer, index_samelayer)
        #copy the children to the new node
        new_node.children = my_first_node.children[:]
        master_node.children.append(new_node)

    #output nodes without weights
    #master_node.output_children(0)

    #call the function to intialize the weights for the children
    master_node.adjust_child_weights()

    # output nodes with the assigned weights
    master_node.output_children(0)

