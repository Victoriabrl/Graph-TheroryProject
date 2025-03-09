def read_constraint_file(filename):
    adj_matrix = []
    tasks = {}

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        # Count the number of tasks from the lines -->ignore empty lines error "too many values to unpack"
        num_tasks = 0
        for line in lines:
            if line.strip():  # Ignore empty lines
                num_tasks += 1

        # Initialize the adjacency matrix with zeros (for N tasks + 2 fictive tasks)
        adj_matrix = [[0] * (num_tasks + 2) for _ in range(num_tasks + 2)]

        for line in lines:
            if line.strip():  # Skip empty lines
                parts = list(map(int, line.split()))  # Split the line and convert txt --> integers
                task_id = parts[0]  
                duration = parts[1]  
                predecessors = parts[2:]  # (optional)
                

                tasks[task_id] = {'duration': duration, 'predecessors': predecessors}

                # Link this task with its predecessors in the adjacency matrix
                for pred in predecessors:
                    adj_matrix[pred][task_id] = duration

        # Return the adjacency matrix and task information
        return adj_matrix, tasks
    
    # Big Up to ZAHI
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
    except Exception as e:
        print(f"Error processing the file: {e}")



