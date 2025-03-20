import node
import connection
import random


class Brain:
    def __init__(self, inputs, clone=False):
        """
        Inicializa uma rede neural simples.
        """

        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.net = []
        self.layers = 2

        if not clone:
            # Nós de entrada
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 0
            # Cria nó de bias
            self.nodes.append(node.Node(3))
            self.nodes[3].layer = 0
            # Cria nó de saída
            self.nodes.append(node.Node(4))
            self.nodes[4].layer = 1

            # Cria conexões entre os nós
            for i in range(0, 4):
                self.connections.append(connection.Connection(self.nodes[i],
                                                              self.nodes[4],
                                                              random.uniform(-1, 1)))

    def connect_nodes(self):
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []

        for i in range(0, len(self.connections)):
            self.connections[i].from_node.connections.append(self.connections[i])

    def generate_net(self):
        self.connect_nodes()
        self.net = []
        for j in range(0, self.layers):
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.net.append(self.nodes[i])

    def feed_forward(self, vision):
        """ Propaga os valores pela rede neural e retorna uma saída entre 0 e 1. """

        for i in range(0, self.inputs):
            self.nodes[i].output_value = vision[i]

        self.nodes[3].output_value = 1

        for i in range(0, len(self.net)):
            self.net[i].activate()

        # Retorna o valor de saída
        output_value = self.nodes[4].output_value

        # Reseta os valores de entrada dos nós
        for i in range(0, len(self.nodes)):
            self.nodes[i].input_value = 0

        return output_value

    def clone(self):
        clone = Brain(self.inputs, True)

        # Clona todos os nós
        for n in self.nodes:
            clone.nodes.append(n.clone())

        # Clona todas as conexões
        for c in self.connections:
            clone.connections.append(c.clone(clone.getNode(c.from_node.id), clone.getNode(c.to_node.id)))

        clone.layers = self.layers
        clone.connect_nodes()
        return clone

    def getNode(self, id):
        for n in self.nodes:
            if n.id == id:
                return n

    # 80 % de chance de mutar o peso de uma conexão
    def mutate(self):
        if random.uniform(0, 1) < 0.5:
            for i in range(0, len(self.connections)):
                self.connections[i].mutate_weight()
