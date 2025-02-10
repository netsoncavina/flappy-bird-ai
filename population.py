import config
import player
import math
import species
import operator

class Population:
    def __init__(self, size):
        self.players = []
        self.generation = 1
        self.species = []
        self.size = size
        for _ in range(0, size):
            self.players.append(player.Player())

    def update_live_players(self):
        for player in self.players:
            if player.alive:
                player.look()
                player.think()
                player.draw(config.window)
                player.update(config.ground)

    def natural_selection(self):
        print('Natural Selection\n')
        print(f'Generation: {self.generation}')

        self.speciate()

        print('Calculating fitness')
        self.calculate_fitness()

        print('Sorting species by fitness')
        self.sort_species_by_fitness()

        print('Children for next generation')
        self.next_generation()

    def speciate(self):
        for species in self.species:
            species.players = []

        for player in self.players:
            add_to_species = False
            for species in self.species:
                if species.similarity(player.brain):
                    species.add_to_species(player)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(player))

    def calculate_fitness(self):
        for player in self.players:
            player.calculate_fitness()

        for species in self.species:
            species.calculate_average_fitness()

    def sort_species_by_fitness(self):
        for species in self.species:
            species.sort_players_by_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_generation(self):
        children = []

        for species in self.species:
            children.append(species.champion.clone())

        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for species in self.species:
            for _ in range(0, children_per_species):
                children.append(species.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players = []
        for child in children:
            self.players.append(child)
        self.generation += 1


    def extinct (self):
        for player in self.players:
            if player.alive:
                return False
        return True
