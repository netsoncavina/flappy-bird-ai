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
        for _ in range(0, self.size):
            self.players.append(player.Player())

    def update_live_players(self):
        for player in self.players:
            if player.alive:
                player.look()
                player.think()
                player.draw(config.window)
                player.update(config.ground)
        if self.players:
            champion = max(self.players, key=operator.attrgetter('fitness'))
            # champion.draw_brain(config.window)

    def natural_selection(self):
        self.speciate()

        self.calculate_fitness()

        self.kill_extinct_species()

        self.kill_stale_species()

        self.sort_species_by_fitness()

        self.next_gen()

    def speciate(self):
        for specie in self.species:
            specie.players = []

        for player in self.players:
            add_to_species = False
            for specie in self.species:
                if specie.similarity(player.brain):
                    specie.add_to_species(player)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(player))

    def calculate_fitness(self):
        for player in self.players:
            player.calculate_fitness()
        for species in self.species:
            species.calculate_average_fitness()

    def kill_extinct_species(self):
        species_bin = []
        for specie in self.species:
            if len(specie.players) == 0:
                species_bin.append(specie)
        for specie in species_bin:
            self.species.remove(specie)

    def kill_stale_species(self):
        player_bin = []
        species_bin = []
        for specie in self.species:
            if specie.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(specie)
                    for player in specie.players:
                        player_bin.append(player)
                else:
                    specie.staleness = 0
        for player in player_bin:
            self.players.remove(player)
        for specie in species_bin:
            self.species.remove(specie)

    def sort_species_by_fitness(self):
        for specie in self.species:
            specie.sort_players_by_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_gen(self):
        children = []

        # Clone of champion is added to each species
        for specie in self.species:
            children.append(specie.champion.clone())

        # Fill open player slots with children
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for specie in self.species:
            for _ in range(0, children_per_species):
                children.append(specie.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players = []
        for child in children:
            self.players.append(child)
        self.generation += 1

    # Return true if all players are dead
    def extinct(self):
        extinct = True
        for player in self.players:
            if player.alive:
                extinct = False
        return extinct
