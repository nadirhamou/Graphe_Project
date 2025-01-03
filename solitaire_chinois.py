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

    def dfs(self, explored_states, solution_moves):
        """Solves the puzzle using Depth-First Search and stores the solution moves."""
        if self.is_goal():
            return True  

        explored_states[0] += 1

        for move in self.get_possible_moves():
            x1, y1, x2, y2 = move
            self.make_move(x1, y1, x2, y2) 
            solution_moves.append(move) 
            
            if self.dfs(explored_states, solution_moves): 
                return True 
            
            solution_moves.pop()  
            self.undo_move(x1, y1, x2, y2) 

        return False

    def heuristic(self):
        """Heuristic: Penalize more for pegs that are not in the center or are far apart."""
        distance_from_center = sum(abs(x - 3) + abs(y - 3) for y, row in enumerate(self.board) for x, val in enumerate(row) if val == 1)
        return sum(row.count(1) for row in self.board) + distance_from_center


    def greedy_best_first_search(self, explored_states, solution_moves):
        """Solves the puzzle using Greedy Best-First Search and stores the solution moves."""
        pq = []
        visited = set()
        initial_state = ([row[:] for row in self.board], [])
        heappush(pq, (self.heuristic(), initial_state))  # (heuristic, (board, moves))
        
        while pq:
            _, (current_board, current_moves) = heappop(pq)
            self.board = [row[:] for row in current_board]
            self.moves = current_moves[:]
            
            if self.is_goal():
                solution_moves.extend(current_moves)  
                return True
            
            explored_states[0] += 1
            board_tuple = tuple(tuple(row) for row in self.board)
            if board_tuple in visited:
                continue
            
            visited.add(board_tuple)
            
            for move in self.get_possible_moves():
                x1, y1, x2, y2 = move
                self.make_move(x1, y1, x2, y2)
                new_state = ([row[:] for row in self.board], self.moves[:] + [move])
                heappush(pq, (self.heuristic(), new_state))
                self.undo_move(x1, y1, x2, y2)
        
        return False

    def a_star_search(self, explored_states, solution_moves):
        """Solves the puzzle using A* Search and stores the solution moves."""
        pq = []
        visited = set()
        initial_state = ([row[:] for row in self.board], [], 0)  
        heappush(pq, (self.heuristic() + 0, initial_state))  # (f(n) = g(n) + h(n), (board, moves, g(n)))
        
        while pq:
            _, (current_board, current_moves, cost) = heappop(pq)
            self.board = [row[:] for row in current_board]
            self.moves = current_moves[:]
            
            if self.is_goal():
                solution_moves.extend(current_moves)  
                return True
            
            explored_states[0] += 1
            board_tuple = tuple(tuple(row) for row in self.board)
            if board_tuple in visited:
                continue
            
            visited.add(board_tuple)
            
            for move in self.get_possible_moves():
                x1, y1, x2, y2 = move
                self.make_move(x1, y1, x2, y2)
                new_cost = cost + 1  
                new_state = ([row[:] for row in self.board], self.moves[:] + [move], new_cost)
                heappush(pq, (new_cost + self.heuristic(), new_state))
                self.undo_move(x1, y1, x2, y2)
        
        return False
    
            
    def log_moves(self, solution_moves, algorithm_name):
        """Reconstructs and logs the board evolution using the solution moves to a text file."""
        filename = f"{algorithm_name}_moves.txt"
        
        with open(filename, "w") as file:
            file.write("Initial Board:\n")
            file.write(self.draw_board() + "\n")  

            for move in solution_moves:
                if len(move) != 4:
                    continue  
                x1, y1, x2, y2 = move
                file.write(f"\nMove: {x1, y1} -> {x2, y2}\n")
                self.make_move(x1, y1, x2, y2)  
                file.write(self.draw_board() + "\n")  

        print(f"Solution evolution logged to {filename}")
        
    def draw_board(self):
        """Returns a string representing the current state of the board."""
        return "\n".join(' '.join(['.' if cell == -1 else 'O' if cell == 1 else ' ' for cell in row]) for row in self.board)


    def reset_board(self):
        """Resets the board to the initial configuration."""
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
        self.moves = []

    def solve_and_compare(self):
        """Solves the puzzle using DFS, GBFS, and A* and compares their complexities."""
        print("Solitaire Chinois with DFS, GBFS, A*\n")
        print("Solving with DFS...")
        explored_states_dfs = [0]
        solution_moves_dfs = []
        start_time = time.time()
        solved_dfs = self.dfs(explored_states_dfs, solution_moves_dfs)
        dfs_time = time.time() - start_time

        if solved_dfs:
            print(f"DFS solved the puzzle in {dfs_time:.4f} seconds with {explored_states_dfs[0]} explored states.")
            self.reset_board()  
            self.log_moves(solution_moves_dfs,"DFS")
        else:
            print("DFS failed to solve the puzzle.")
            
        print("\nSolving with GBFS...")
        self.reset_board()  
        explored_states_gbfs = [0]
        solution_moves_gbfs = []
        start_time = time.time()
        solved_gbfs = self.greedy_best_first_search(explored_states_gbfs, solution_moves_gbfs)
        gbfs_time = time.time() - start_time

        if solved_gbfs:
            print(f"GBFS solved the puzzle in {gbfs_time:.4f} seconds with {explored_states_gbfs[0]} explored states.")
            self.reset_board()  
            self.log_moves(solution_moves_gbfs,"GBFS")
        else:
            print("GBFS failed to solve the puzzle.")

        print("\nSolving with A*...")
        self.reset_board()  
        explored_states_a_star = [0]
        solution_moves_a_star = []
        start_time = time.time()
        solved_a_star = self.a_star_search(explored_states_a_star, solution_moves_a_star)
        a_star_time = time.time() - start_time

        if solved_a_star:
            print(f"A* solved the puzzle in {a_star_time:.4f} seconds with {explored_states_a_star[0]} explored states.")
            self.reset_board()  
            self.log_moves(solution_moves_a_star,"A_star")
        else:
            print("A* failed to solve the puzzle.")






if __name__ == "__main__":
    solitaire = SolitaireChinois()
    solitaire.display_board()
    solitaire.solve_and_compare()
