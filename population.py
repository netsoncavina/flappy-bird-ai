import config
import player

class Population:
    def __init__(self, size):
        self.players = []
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

    def extinct (self):
        for player in self.players:
            if player.alive:
                return False
        return True
