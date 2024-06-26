import re
from datetime import datetime
from pddl.pddlrunner import run_enhsp_jar

RE_FOUND_PLAN = re.compile(r"^Found Plan")
RE_MOVE = re.compile(r"^(?:(^\d+\.\d+\:)\s)(?:\()(.*)(?:.*\))")

def parse_output(out):
    lines = out.split("\n")
    found_plan = False
    moves = []
    for line in lines:
        if not found_plan:
            if RE_FOUND_PLAN.match(line):
                found_plan = True
            continue
        match = RE_MOVE.search(line)
        if match:
            idx, move = match.groups()
            action_args = move.split(" ")
            moves.append((idx, action_args[0], tuple(action_args[1:])))
        else: break
    
    return moves

def run_program_and_parse_output():
    (out, err) = run_enhsp_jar()
    filename = datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + '.txt'
    with open(f'logs/{filename}', 'w') as f:
        print(f'Solution stored in "{filename}" log file')
        f.write(out)
    return parse_output(out)