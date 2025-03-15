def read_constraint_file(filename):
    adj_matrix = []
    tasks = {}
    t=0
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        num_tasks = 0
        for line in lines:
            if line.strip():
                num_tasks += 1

        adj_matrix = [[0] * (num_tasks + 2) for _ in range(num_tasks + 2)]

        # Étape 1 : Lire les tâches sans traiter les prédécesseurs
        for line in lines:
            if line.strip():
                parts = list(map(int, line.split()))
                task_id, duration = parts[0], parts[1]
                tasks[task_id] = {'duration': duration, 'predecessors': []}

        # Étape 2 : Ajouter les prédécesseurs après que toutes les tâches existent
        for line in lines:
            if line.strip():
                parts = list(map(int, line.split()))
                task_id = parts[0]
                predecessors = parts[2:]

                for pred in predecessors:
                    if pred in tasks:
                        tasks[task_id]['predecessors'].append(pred)
                        adj_matrix[pred][task_id] = tasks[pred]['duration']
                        if tasks[pred]['duration']<0 :
                            t=1
                    else:
                        print(f"⚠️ Avertissement : Le prédécesseur {pred} de la tâche {task_id} n'existe pas encore.")

        # Connecter les tâches sans prédécesseurs à la tâche fictive 0
        for task_id in range(1, num_tasks + 1):
            if not tasks[task_id]['predecessors']:
                adj_matrix[0][task_id] = 0  # Connexion à la tâche fictive 0

        # Connecter les tâches sans successeurs à la tâche fictive (N+1)
        for task_id in range(1, num_tasks + 1):
            if not any(task_id in tasks[t]['predecessors'] for t in range(1, num_tasks + 1)):
                adj_matrix[task_id][num_tasks + 1] = tasks[task_id]['duration']

        return adj_matrix, tasks

    except FileNotFoundError:
        print(f"Le fichier {filename} est introuvable.")
    except Exception as e:
        print(f"Erreur lors du traitement du fichier : {e}")
