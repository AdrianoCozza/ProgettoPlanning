import re

def parse_problem_file(problem_file_path: str):
    with open(problem_file_path, 'r') as f:
        lines = f.read().strip().split('\n')
    
    people = {}
    elevator_x_current_floor = None
    elevator_y_current_floor = None
    num_floors = None

    for line in lines:
        match = re.match(r'.*\(floors\) (\d+)', line)
        if match is not None:
            num_floors = int(match.groups()[0])
        match = re.match(r'.*\(at-person ([a-zA-Z0-9]+)\) (\d+)', line)
        if match is not None:
            person_label, current_floor = match.groups()
            if people.get(person_label) is None:
                people[person_label] = {}
            people[person_label]['current_floor'] = current_floor
            continue

        match = re.match(r'.*\(target ([a-zA-Z0-9]+)\) (\d+)', line)
        if match is not None:
            person_label, target_floor = match.groups()
            if people.get(person_label) is None:
                people[person_label] = {}
            people[person_label]['target_floor'] = target_floor
        
        match = re.match(r'.*\(at-elevator elevatorX.*\) (\d+)', line)
        if match is not None:
            elevator_x_current_floor = int(match.groups()[0]) - 1
        
        match = re.match(r'.*\(at-elevator elevatorY.*\) (\d+)', line)
        if match is not None:
            elevator_y_current_floor = int(match.groups()[0]) - 1

    people_as_list = []
    # Validation
    for key, value in people.items():
        value: dict
        if value.get('current_floor') is None:
            raise ValueError(f"Error parsing person {key}, current floor not found")
        
        if value.get('target_floor') is None:
            raise ValueError(f"Error parsing person {key}, target floor not found")

        people_as_list.append((key, int(value['current_floor'])-1, int(value['target_floor'])-1))

    if elevator_x_current_floor is None or elevator_x_current_floor < 0:
        raise ValueError("Couldn't find elevator current floor")

    return (people_as_list, elevator_x_current_floor, elevator_y_current_floor, num_floors)