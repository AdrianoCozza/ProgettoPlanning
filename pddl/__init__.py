from pddl.pddloutparser import run_program_and_parse_output
from pddl.pddlinparser import parse_problem_file

class Parser:
    def __init__(self):
        self.moves = run_program_and_parse_output()
        self.count = 0

    def get(self):
        return parse_problem_file('solver/problem.pddl')

    def get_moves(self):
        return self.moves

    def done(self):
        return self.count >= len(self.moves)

    def next_move(self):
        if self.count >= len(self.moves):
            return None

        move = self.moves[self.count]
        self.count += 1
        return move