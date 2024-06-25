import subprocess

def run_enhsp_jar(jar_path=None, args=None):
    
    if not jar_path:
        jar_path = 'solver/enhsp-20.jar'
    if not args:
        args = ['-f', 'solver/problem.pddl', '-o', 'solver/domain.pddl']
        
    command = ['java', '-jar', jar_path] + args
    
    try:
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        return (result.stdout, result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print("Error output:\n", e.stderr)