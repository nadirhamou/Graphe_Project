import time
from heapq import heappush, heappop

class SolitaireChinois:
    def __init__(self, final_target=None):

        self.board = [
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
        ]

        self.initial_empty = self.get_initial_empty_position()
        self.final_target = final_target or self.initial_empty
        self.board[self.initial_empty[0]][self.initial_empty[1]] = 0
        self.moves = []

    def get_initial_empty_position(self):
        """Prompts the user to input the initial empty position and validates it."""
        while True:
            try:
                x, y = map(int, input("Enter the coordinates of the empty cell (x, y) between 0 and 6: ").split(","))
                if (
                    0 <= x < 7
                    and 0 <= y < 7
                    and self.board[x][y] == 1
                ):
                    return x, y
                else:
                    print("Invalid coordinates. Please enter valid coordinates within the playable area.")
            except ValueError:
                print("Invalid input. Please enter two integers separated by a comma.")

    def display_board(self):
        """Prints the current state of the board."""
        for row in self.board:
            print(' '.join(['.' if cell == -1 else 'O' if cell == 1 else ' ' for cell in row]))
        print()

    def is_valid_move(self, x1, y1, x2, y2):
        """Checks if a move from (x1, y1) to (x2, y2) is valid."""
        if not (0 <= x1 < 7 and 0 <= y1 < 7 and 0 <= x2 < 7 and 0 <= y2 < 7):
            return False
        if self.board[x1][y1] != 1 or self.board[x2][y2] != 0:
            return False
        dx, dy = x2 - x1, y2 - y1
        if abs(dx) == 2 and dy == 0 and self.board[x1 + dx // 2][y1] == 1:
            return True
        if abs(dy) == 2 and dx == 0 and self.board[x1][y1 + dy // 2] == 1:
            return True
        return False

    def make_move(self, x1, y1, x2, y2):
        """Executes a move and removes the jumped marble."""
        dx, dy = (x2 - x1) // 2, (y2 - y1) // 2
        self.board[x1][y1] = 0
        self.board[x1 + dx][y1 + dy] = 0
        self.board[x2][y2] = 1
        self.moves.append(((x1, y1), (x2, y2)))

    def undo_move(self, x1, y1, x2, y2):
        """Reverts a move and restores the jumped marble."""
        dx, dy = (x2 - x1) // 2, (y2 - y1) // 2
        self.board[x1][y1] = 1
        self.board[x1 + dx][y1 + dy] = 1
        self.board[x2][y2] = 0
        self.moves.pop()

    def is_goal(self):
        """Checks if the current board is in the goal state."""
        return sum(row.count(1) for row in self.board) == 1 and self.board[self.final_target[0]][self.final_target[1]] == 1

    def get_possible_moves(self):
        """Generates all valid moves."""
        moves = []
        for x1 in range(7):
            for y1 in range(7):
                if self.board[x1][y1] == 1:
                    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        x2, y2 = x1 + dx, y1 + dy
                        if self.is_valid_move(x1, y1, x2, y2):
                            moves.append((x1, y1, x2, y2))
        return moves

    def dfs(self, explored_states):
        """Solves the puzzle using Depth-First Search."""
        if self.is_goal():
            return True

        explored_states[0] += 1

        for move in self.get_possible_moves():
            x1, y1, x2, y2 = move
            self.make_move(x1, y1, x2, y2)
            if self.dfs(explored_states):
                return True
            self.undo_move(x1, y1, x2, y2)

        return False

    def heuristic(self):
        """Heuristic: Penalize more for pegs that are not in the center or are far apart."""
        distance_from_center = sum(abs(x - 3) + abs(y - 3) for y, row in enumerate(self.board) for x, val in enumerate(row) if val == 1)
        return sum(row.count(1) for row in self.board) + distance_from_center
    def heuristic_A_star(self):
        """Heuristic: Penalize more for pegs that are not in the center or are far apart."""
        distance_from_center = sum(abs(x - 3) + abs(y - 3) for y, row in enumerate(self.board) for x, val in enumerate(row) if val == 1)
        return sum(row.count(1) for row in self.board) + distance_from_center

    def greedy_best_first_search(self, explored_states):
        """Solves the puzzle using Greedy Best-First Search."""
        pq = []
        visited = set()
        initial_state = ([row[:] for row in self.board], [])
        heappush(pq, (self.heuristic(), initial_state))  # (heuristic, (board, moves))
        
        while pq:
            _, (current_board, current_moves) = heappop(pq)
            self.board = [row[:] for row in current_board]
            self.moves = current_moves[:]
            
            if self.is_goal():
                return True
            
            explored_states[0] += 1
            board_tuple = tuple(tuple(row) for row in self.board)
            if board_tuple in visited:
                continue
            
            visited.add(board_tuple)
            
            for move in self.get_possible_moves():
                x1, y1, x2, y2 = move
                self.make_move(x1, y1, x2, y2)
                new_state = ([row[:] for row in self.board], self.moves[:])
                heappush(pq, (self.heuristic(), new_state))
                self.undo_move(x1, y1, x2, y2)
        
        return False

    def a_star_search(self, explored_states):
        """Solves the puzzle using A* Search."""
        pq = []
        visited = set()
        initial_state = ([row[:] for row in self.board], [], 0)  # (board, moves, cost)
        heappush(pq, (self.heuristic_A_star() + 0, initial_state))  # (f(n) = g(n) + h(n), (board, moves, g(n)))
        
        while pq:
            _, (current_board, current_moves, cost) = heappop(pq)
            self.board = [row[:] for row in current_board]
            self.moves = current_moves[:]
            
            if self.is_goal():
                return True
            
            explored_states[0] += 1
            board_tuple = tuple(tuple(row) for row in self.board)
            if board_tuple in visited:
                continue
            
            visited.add(board_tuple)
            
            for move in self.get_possible_moves():
                x1, y1, x2, y2 = move
                self.make_move(x1, y1, x2, y2)
                new_cost = cost + 1  # Increment cost for each move
                new_state = ([row[:] for row in self.board], self.moves[:], new_cost)
                heappush(pq, (new_cost + self.heuristic_A_star(), new_state))
                self.undo_move(x1, y1, x2, y2)
        
        return False




    def solve_and_compare(self):
        """Solves the puzzle using DFS, GBFS, and A* and compares their complexities."""
        print("Solving with DFS...")
        self.moves = []
        start_time = time.time()
        explored_states_dfs = [0]
        solved_dfs = self.dfs(explored_states_dfs)
        dfs_time = time.time() - start_time

        if solved_dfs:
            print(f"DFS solved the puzzle in {dfs_time:.4f} seconds with {explored_states_dfs[0]} explored states.")
        else:
            print("DFS failed to solve the puzzle.")
            
        print("\nSolving with GBFS...")
        self.moves = []
        self.board = [
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
        ]
        self.board[self.initial_empty[0]][self.initial_empty[1]] = 0
        start_time = time.time()
        explored_states_gbfs = [0]
        solved_gbfs = self.greedy_best_first_search(explored_states_gbfs)
        gbfs_time = time.time() - start_time

        if solved_gbfs:
            print(f"GBFS solved the puzzle in {gbfs_time:.4f} seconds with {explored_states_gbfs[0]} explored states.")
        else:
            print("GBFS failed to solve the puzzle.")

        print("\nSolving with A*...")
        self.moves = []
        self.board = [
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
        ]
        self.board[self.initial_empty[0]][self.initial_empty[1]] = 0
        start_time = time.time()
        explored_states_a_star = [0]
        solved_a_star = self.a_star_search(explored_states_a_star)
        a_star_time = time.time() - start_time

        if solved_a_star:
            print(f"A* solved the puzzle in {a_star_time:.4f} seconds with {explored_states_a_star[0]} explored states.")
        else:
            print("A* failed to solve the puzzle.")






# Example Usage
if __name__ == "__main__":
    solitaire = SolitaireChinois()
    solitaire.display_board()
    solitaire.solve_and_compare()