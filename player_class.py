from settings import *
import pygame

vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = vec(pos[0], pos[1])
        self.grid_pos_none_vec = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(0, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 1
        self.temp = self.pix_pos
        self.target = None

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move(None)
        else:
            self.eat_coin()

        # Tracking the player
        self.grid_pos[0] = (
            self.pix_pos[0] - TOP_BOTTOM_BUFFER // 2) // self.app.cell_width
        self.grid_pos[1] = (
            self.pix_pos[1] - TOP_BOTTOM_BUFFER // 2) // self.app.cell_height

        if self.mid_grid():
            self.eat_coin()
        else:
            self.minus_one_score()

    def mid_grid(self):
        if self.grid_pos in self.app.coins:
            # eat coin when at center
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 20

    def minus_one_score(self):
        if self.grid_pos in self.app.empty_grid and len(self.app.empty_grid_score) == 0 and self.grid_pos not in self.app.empty_grid_score:
            #print("we got empty grid in")
            self.app.empty_grid_score.append(
                [self.grid_pos[0], self.grid_pos[1]])
        if self.grid_pos in self.app.empty_grid and len(self.app.empty_grid_score) == 1:
            if [self.grid_pos[0], self.grid_pos[1]] not in self.app.empty_grid_score:
                self.app.empty_grid_score.pop()
                self.current_score -= 1

    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOR,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.app.cell_width//2-2)

        # draw lives of player
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOR,
                               (30 + x*20, HEIGHT - 15), self.app.cell_width//2-2)

        # Draw the tracking box
        pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width + TOP_BOTTOM_BUFFER//2,
                                                self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, self.app.cell_width, self.app.cell_height), 1)

    def get_pix_pos(self):
        return (
            vec((self.grid_pos.x*self.app.cell_width)+TOP_BOTTOM_BUFFER//2 + (self.app.cell_width//2),
                (self.grid_pos.y*self.app.cell_height)+TOP_BOTTOM_BUFFER//2 + (self.app.cell_height//2)))

    # allow to move when at a cell
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    # unesscessary already check in BFS => For human player
    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True

    def move(self, direction):
        #self.stored_direction = direction
        self.direction = self.get_path_direction(self.target)

    # AI - pacman functions
    def set_target(self):
        for x_id, y_id in self.app.coins:
            #print(vec(x_id, y_id))
            return vec(x_id, y_id)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
                        int(target[0]), int(target[1])])

        return path[1]

    def BFS(self, start_pos, target_pos):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start_pos]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target_pos:
                break
            for enemy in self.app.enemies:
                if current == enemy.grid_pos:
                    break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [
                                neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append(
                                        {"Current":  current, "Next":  next_cell})
        shortest = [target_pos]
        while target_pos != start_pos:
            for step in path:
                if step["Next"] == target_pos:
                    target_pos = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest
