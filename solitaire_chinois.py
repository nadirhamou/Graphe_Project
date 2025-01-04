import time
from heapq import heappush, heappop

class SolitaireChinois:
    def __init__(self):
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
        self.final_target = self.get_final_target()
        self.board[self.initial_empty[0]][self.initial_empty[1]] = 0
        self.moves = []

    def get_initial_empty_position(self):
        """Demande à l'utilisateur de saisir la position initiale vide et la valide."""
        while True:
            try:
                x, y = map(int, input("Entrez la position vide initiale (x, y) entre 0 et 6 : ").split(","))
                if (
                    0 <= x < 7
                    and 0 <= y < 7
                    and self.board[x][y] == 1
                ):
                    return x, y
                else:
                    print("Coordonnées invalides. Veuillez entrer des coordonnées valides dans la zone jouable.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer deux entiers séparés par une virgule.")

    def get_final_target(self):
        """Demande à l'utilisateur de saisir la position cible finale et la valide."""
        while True:
            try:
                x, y = map(int, input("Entrez la position cible finale (x, y) entre 0 et 6 : ").split(","))
                if 0 <= x < 7 and 0 <= y < 7 and self.board[x][y] == 1:
                    return x, y
                else:
                    print("Coordonnées invalides. Veuillez entrer des coordonnées valides dans la zone jouable.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer deux entiers séparés par une virgule.")

    def display_board(self):
        """Affiche l'état actuel du plateau."""
        for row in self.board:
            print(' '.join(['.' if cell == -1 else 'O' if cell == 1 else ' ' for cell in row]))
        print()

    def is_valid_move(self, x1, y1, x2, y2):
        """Vérifie si un déplacement de (x1, y1) à (x2, y2) est valide."""
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
        """Exécute un déplacement et supprime la bille sautée."""
        dx, dy = (x2 - x1) // 2, (y2 - y1) // 2
        self.board[x1][y1] = 0
        self.board[x1 + dx][y1 + dy] = 0
        self.board[x2][y2] = 1
        self.moves.append(((x1, y1), (x2, y2)))

    def undo_move(self, x1, y1, x2, y2):
        """Annule un déplacement et restaure la bille sautée."""
        dx, dy = (x2 - x1) // 2, (y2 - y1) // 2
        self.board[x1][y1] = 1
        self.board[x1 + dx][y1 + dy] = 1
        self.board[x2][y2] = 0
        self.moves.pop()

    def is_goal(self):
        """Vérifie si le plateau actuel est dans l'état cible."""
        return sum(row.count(1) for row in self.board) == 1 and self.board[self.final_target[0]][self.final_target[1]] == 1

    def get_possible_moves(self):
        """Génère tous les déplacements valides."""
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
        """Résout le puzzle en utilisant la recherche en profondeur (DFS) et stocke les mouvements de solution."""
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
        """Fonction heuristique : Pénalise la distance des pions par rapport à la cible finale."""
        target_x, target_y = self.final_target
        distance_sum = 0
        for x in range(7):
            for y in range(7):
                if self.board[x][y] == 1:
                    distance_sum += abs(x - target_x) + abs(y - target_y)
        return distance_sum + sum(row.count(1) for row in self.board)


    def greedy_best_first_search(self, explored_states, solution_moves):
        """Résout le puzzle en utilisant la recherche gloutonne (GBFS) et stocke les mouvements de solution."""
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
        """Résout le puzzle en utilisant A* et stocke les mouvements de solution."""
        pq = []
        visited = set()
        initial_state = ([row[:] for row in self.board], [], 0)  
        heappush(pq, (self.heuristic() + 0, initial_state))  # (heuristic + cost, (board, moves, cost))
        
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
        """Reconstitue et enregistre l'évolution du plateau en utilisant les mouvements de solution dans un fichier texte."""
        filename = f"{algorithm_name}_moves.txt"
        
        with open(filename, "w") as file:
            file.write("Plateau initial :\n")
            file.write(self.draw_board() + "\n")  

            for move in solution_moves:
                if len(move) != 4:
                    continue  
                x1, y1, x2, y2 = move
                file.write(f"\nMouvement: {x1, y1} -> {x2, y2}\n")
                self.make_move(x1, y1, x2, y2)  
                file.write(self.draw_board() + "\n")  

        print(f"Évolution de la solution enregistrée dans {filename}")
        
    def draw_board(self):
        """Retourne une chaîne représentant l'état actuel du plateau."""
        return "\n".join(' '.join(['.' if cell == -1 else 'O' if cell == 1 else ' ' for cell in row]) for row in self.board)


    def reset_board(self):
        """Réinitialise le plateau à la configuration initiale."""
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
        """Résout le puzzle en utilisant DFS, GBFS et A* et compare leurs complexités."""
        print("Solitaire Chinois avec DFS, GBFS, A*\n")
        print("Résolution avec DFS...")
        explored_states_dfs = [0]
        solution_moves_dfs = []
        start_time = time.time()
        solved_dfs = self.dfs(explored_states_dfs, solution_moves_dfs)
        dfs_time = time.time() - start_time

        if solved_dfs:
            print(f"DFS a résolu le puzzle en {dfs_time:.4f} secondes avec {explored_states_dfs[0]} états explorés.")
            self.reset_board()  
            self.log_moves(solution_moves_dfs,"DFS")
        else:
            print("DFS n'a pas réussi à résoudre le puzzle.")
            
        print("\nRésolution avec GBFS...")
        self.reset_board()  
        explored_states_gbfs = [0]
        solution_moves_gbfs = []
        start_time = time.time()
        solved_gbfs = self.greedy_best_first_search(explored_states_gbfs, solution_moves_gbfs)
        gbfs_time = time.time() - start_time

        if solved_gbfs:
            print(f"GBFS a résolu le puzzle en {gbfs_time:.4f} secondes avec {explored_states_gbfs[0]} états explorés.")
            self.reset_board()  
            self.log_moves(solution_moves_gbfs,"GBFS")
        else:
            print("GBFS n'a pas réussi à résoudre le puzzle.")

        print("\nRésolution avec A*...")
        self.reset_board()  
        explored_states_a_star = [0]
        solution_moves_a_star = []
        start_time = time.time()
        solved_a_star = self.a_star_search(explored_states_a_star, solution_moves_a_star)
        a_star_time = time.time() - start_time

        if solved_a_star:
            print(f"A* a résolu le puzzle en {a_star_time:.4f} secondes avec {explored_states_a_star[0]} états explorés.")
            self.reset_board()  
            self.log_moves(solution_moves_a_star,"A_star")
        else:
            print("A* n'a pas réussi à résoudre le puzzle.")






if __name__ == "__main__":
    solitaire = SolitaireChinois()
    solitaire.display_board()
    solitaire.solve_and_compare()
