import re

from pddlrunner import run_enhsp_jar

RE_FOUND_PLAN = re.compile(r"^Found Plan")
RE_MOVE = re.compile(r"^(?:^\d+\.\d+\:\s)(?:\()(.*)(?:.*\))")

def run_program_and_parse_output():
    (out, err) = run_enhsp_jar()
    return parse_output(out)

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
            move = match.group(1)
            action_args = move.split(" ")
            moves.append((action_args[0], tuple(action_args[1:])))
        else: break
    
    return tuple(moves)