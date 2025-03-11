from graph import read_constraint_file

def main():
    while True:
        filename = input("Enter the name of the .txt file (or 'exit' to quit): ")
        if filename.lower() == "exit":
            break

        try:
            adj_matrix, tasks = read_constraint_file(filename)
            
            print("Creating the scheduling graph:")
            num_vertices = len(adj_matrix) - 2  # excluding fictive tasks (0 and N+1)
            edges = []

            # Correcting the relations with the fictive vertices
            for i in range(1, num_vertices + 1):
                # Connect the fictive task 0 to tasks that have no predecessors
                if not tasks[i]['predecessors']:
                    adj_matrix[0][i] = 0  # Task 0 has no duration, only connects tasks without predecessors
                    edges.append((0, i, 0))  # No duration for the edge from task 0 to task i

                has_successor = False
                for j in range(1, num_vertices + 1):
                    if adj_matrix[i][j] != 0:
                        edges.append((i, j, adj_matrix[i][j]))
                        has_successor = True

                # If no successors, connect the task to the fictive task N+1
                if not has_successor:
                    adj_matrix[i][num_vertices + 1] = tasks[i]['duration']
                    edges.append((i, num_vertices + 1, tasks[i]['duration']))

            edges.sort(key=lambda x: x[0])

            # Display the number of vertices and edges
            print(f"{num_vertices} vertices")
            print(f"{len(edges)} edges")
            for edge in edges:
                print(f"{edge[0]} -> {edge[1]} = {edge[2]}")

            # Display the adjacency matrix with proper grouping (including fictive tasks)
            print("\nAdjacency matrix of the graph:")

            # Create the header row
            header = ['0'] + [str(i) for i in range(1, num_vertices + 2)]  # Add '0' for the fictive task

            # Display header with fixed width
            print("{:<4}".format(" "), end="")  # Print top-left corner aligned
            for h in header:
                print(f"{h:<4}", end="")  # Align each task number in the header
            print()  # Newline after header row

            # Display the matrix with fixed-width columns and '*' for no relation
            for i in range(num_vertices + 2):  # Display all tasks including 0 and N+1
                # Align the task number in the first column
                print(f"{i:<4}", end="")  

                if i == 0:  # Handle task 0 (fictive task)
                    for j in range(1, num_vertices + 1):
                        if tasks[j]['predecessors'] == [] :
                            print(f"{'*':<4}", end="")
                        else:
                            print(f"{'0':<4}", end="")
                    print(f"{'*':<4}", end="")  # Add '*' for the fictive N+1 task as well
                elif i == num_vertices + 1:  # Handle task N+1 (fictive task)
                    for j in range(num_vertices + 1):  # Only tasks from 0 to N
                        if adj_matrix[j][i] != 0:  # If there's a relation to N+1, display it
                            print(f"{adj_matrix[j][i]:<4}", end="")
                        else:
                            print(f"{'*':<4}", end="")  # No relation for tasks with no successors
                    print(f"{'*':<4}", end="")  # Add '*' for the N+1 task
                else:
                    for j in range(num_vertices + 2):
                        if adj_matrix[i][j] == 0 and i != 0:
                            print(f"{'*':<4}", end="")
                        else:
                            print(f"{adj_matrix[i][j]:<4}", end="")
                print()  # Newline after each row

            # Display task information including fictive tasks 0 and N+1
            print("\nTask information:")
            
            # Display task 0 (fictive task)
            print(f"Task 0: {{'duration': 0, 'predecessors': []}}")

            # Add task 1 to N+1
            for task_id, task_info in tasks.items():
                if task_id == 1:
                    task_info['predecessors'] = [0]  # Tâche 1 a pour prédécesseur la tâche 0
                elif task_id != num_vertices + 1:  # Ne pas ajouter de prédécesseur pour N+1
                    task_info['predecessors'] = [0] if not task_info['predecessors'] else task_info['predecessors']

                print(f"Task {task_id}: {task_info}")
            
            # Display task N+1 (fictive task)
            print(f"Task {num_vertices + 1}: {{'duration': 0, 'predecessors': [", end="")
            # List the tasks that are predecessors of N+1
            for i in range(1, num_vertices + 1):
                if adj_matrix[i][num_vertices + 1] != 0:
                    print(f"{i}", end="")
                    if i != num_vertices:
                        print(", ", end="")
            print("]}}")

        except FileNotFoundError:
            print(f"The specified file '{filename}' was not found. Please try again.")
        except Exception as e:
            print(f"Error processing the file: {e}")

if __name__ == "__main__":
    main()

