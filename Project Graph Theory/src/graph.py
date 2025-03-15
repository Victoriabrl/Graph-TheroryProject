def read_constraint_file(filename):
    val_matrix = []
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
        val_matrix = [['*'] * (num_tasks + 2) for _ in range(num_tasks + 2)]

        for line in lines:
            if line.strip():  # Skip empty lines
                parts = list(map(int, line.split()))  # Split the line and convert txt --> integers
                task_id = parts[0]  
                duration = parts[1]  
                predecessors = parts[2:]  # (optional)
                
                tasks[task_id] = {'duration': duration, 'predecessors': predecessors}

                # Link this task with its predecessors in the adjacency matrix
                for pred in predecessors:
                    val_matrix[pred][task_id] = tasks[pred]['duration']  # Use duration of the predecessor

        # Handle tasks without predecessors (connect them to task 0 with duration 0)
        for task_id in range(1, num_tasks + 1):
            if not tasks[task_id]['predecessors']:  # No predecessors
                val_matrix[0][task_id] = 0  # Task 0 points to task_id with a duration of 0

        # Handle tasks without successors (connect them to task N+1 with their duration)
        for task_id in range(1, num_tasks + 1):
            if not any(task_id in tasks[t]['predecessors'] for t in range(1, num_tasks + 1)):  # No successors
                val_matrix[task_id][num_tasks + 1] = tasks[task_id]['duration']

        # Return the adjacency matrix and task information
        return val_matrix, tasks
    
    # Big Up to ZAHI
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return None, None
    except Exception as e:
        print(f"Error processing the file: {e}")
        return None, None
