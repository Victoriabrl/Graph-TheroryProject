from graph import read_constraint_file
import graph

def main():
    while True:
        filename = input("Enter the name of the .txt file (or 'exit' to quit): ")
        if filename.lower() == "exit":
            break

        try:
            adj_matrix, tasks = read_constraint_file(filename)

            num_vertices = len(adj_matrix) - 2  # Exclure tâches fictives (0 et N+1)
            edges = []

            for i in range(1, num_vertices + 1):
                if not tasks[i]['predecessors']:
                    adj_matrix[0][i] = 0
                    edges.append((0, i, 0))

                has_successor = False
                for j in range(1, num_vertices + 1):
                    if adj_matrix[i][j] != 0:
                        edges.append((i, j, adj_matrix[i][j]))
                        has_successor = True

                if not has_successor:
                    adj_matrix[i][num_vertices + 1] = tasks[i]['duration']
                    edges.append((i, num_vertices + 1, tasks[i]['duration']))

            edges.sort(key=lambda x: x[0])

            print(f"{num_vertices} sommets")
            print(f"{len(edges)} arêtes")
            for edge in edges:
                print(f"{edge[0]} -> {edge[1]} = {edge[2]}")

            # Affichage de la matrice value
            print("\nValue matrix:")

            header = ['0'] + [str(i) for i in range(1, num_vertices + 2)]
            print("{:<4}".format(" "), end="")
            for h in header:
                print(f"{h:<4}", end="")
            print()

            for i in range(num_vertices + 2):
                print(f"{i:<4}", end="")
                for j in range(num_vertices + 2):
                    if adj_matrix[i][j] == 0 and (
                            i != 0 or j not in [k for k in range(1, num_vertices + 1) if not tasks[k]['predecessors']]):
                        print(f"{'*':<4}", end="")
                    else:
                        print(f"{adj_matrix[i][j]:<4}", end="")
                print()

            print("\nInformations des tâches:")

            print(f"Tâche 0: {{'duration': 0, 'predecessors': []}}")

            for task_id, task_info in tasks.items():
                if task_id == 1:
                    task_info['predecessors'] = [0]
                elif task_id != num_vertices + 1:
                    task_info['predecessors'] = [0] if not task_info['predecessors'] else task_info['predecessors']

                print(f"Tâche {task_id}: {task_info}")

            print(f"Tâche {num_vertices + 1}: {{'duration': 0, 'predecessors': [", end="")
            predecessors_of_n1 = [
                str(i) for i in range(1, num_vertices + 1)
                if adj_matrix[i][num_vertices + 1] != 0
            ]
            print(", ".join(predecessors_of_n1), end="")
            print("]}}")


        except FileNotFoundError:
            print(f"Le fichier '{filename}' est introuvable.")
        except Exception as e:
            print(f"Erreur lors du traitement du fichier : {e}")

if graph.t==1:
    print ('negative')
else:
    print("positive")



if __name__ == "__main__":
    main()
