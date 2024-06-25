from pddl.pddloutparser import parse_output, run_enhsp_jar

def run_program_and_parse_output():
    (out, err) = run_enhsp_jar()
    return parse_output(out)