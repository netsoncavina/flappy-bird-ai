import config
import player
import math
import species
import operator
import pandas as pd
from datetime import datetime


class Population:
    def __init__(self, size):
        self.players = []
        self.generation = 1
        self.species = []
        self.size = size
        self.best_players = []

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
            champion.draw_brain(config.window)

    def natural_selection(self):
        self.speciate()

        self.calculate_fitness()

        self.kill_extinct_species()

        self.kill_stale_species()

        self.sort_species_by_fitness()

        self.save_best_player()

        self.next_gen()

    def save_best_player(self):
        if not self.players:
            return

        champion = max(self.players, key=operator.attrgetter('fitness'))
        self.best_players.append({'Generation': self.generation, 'Champion Fitness': champion.fitness})

        print(f'Generation: {self.generation} | Champion Fitness: {champion.fitness} (saved in memory)')

    # Separa os jogadores em espécies
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

    # Exclui espécies sem jogadores
    def kill_extinct_species(self):
        species_bin = []
        for specie in self.species:
            if len(specie.players) == 0:
                species_bin.append(specie)
        for specie in species_bin:
            self.species.remove(specie)

    # Exclui espécies com jogadores estagnados
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

        # Clone dos campeões de cada espécie
        for specie in self.species:
            children.append(specie.champion.clone())

        # Preenche os slots de jogadores vazios com filhos
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

    # Return true se todos os jogadores estiverem mortos
    def extinct(self):
        extinct = True
        for player in self.players:
            if player.alive:
                extinct = False
        return extinct

    def save_excel(self):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f'fitness_tracker/best_players_{now}.xlsx'

        if self.best_players:
            df = pd.DataFrame(self.best_players)
            df.to_excel(file_path, index=False)
            print(f"Results saved to {file_path}")
        else:
            print("No results to save.")
