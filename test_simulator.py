import time
import random
import matplotlib.pyplot as plt
from main import FileSystem  # Certifique-se de que `main.py` esteja no mesmo diretório ou no PYTHONPATH

def run_test_sequence(fs, commands, log_file):
    """Executa uma sequência de comandos, salva o log e exibe a estrutura final."""
    with open(log_file, "w") as log:
        start_time = time.time()
        for command in commands:
            try:
                if command.startswith("mkdir"):
                    _, name = command.split()
                    log.write(fs.mkdir(name) + "\n")
                elif command.startswith("create"):
                    _, name, size = command.split()
                    log.write(fs.create_file(name, int(size)) + "\n")
                elif command == "ls":
                    log.write(fs.ls() + "\n")
                elif command.startswith("cd"):
                    _, name = command.split()
                    log.write(fs.cd(name) + "\n")
                elif command.startswith("delete"):
                    _, name = command.split()
                    log.write(fs.delete(name) + "\n")
                elif command == "info":
                    log.write(fs.info() + "\n")
                elif command.startswith("write"):
                    _, path, data = command.split(maxsplit=2)
                    log.write(fs.write(path, data) + "\n")
                elif command.startswith("read"):
                    _, path = command.split()
                    log.write(fs.read(path) + "\n")
            except Exception as e:
                log.write(f"Erro ao executar '{command}': {str(e)}\n")

        # Adicionar comando tree no final do log
        log.write("\nEstrutura final do sistema de arquivos:\n")
        log.write(fs.tree())
        
        # Adicionar comando info no final do log
        log.write("\nInfo do sistema de arquivos:\n")
        log.write(fs.info())
        end_time = time.time()
    return end_time - start_time

def generate_random_commands(num_commands, max_size=10):
    """Gera uma sequência aleatória de comandos com estrutura mais complexa."""
    commands = []
    current_path = "/RAIZ"
    created_dirs = ["RAIZ"]  # Diretórios já criados
    created_files = []       # Arquivos já criados

    for _ in range(num_commands):
        action = random.choice(["mkdir", "create", "cd", "ls", "info", "write", "read", "delete"])
        
        if action == "mkdir":
            dir_name = f"dir_{random.randint(1, 100)}"
            commands.append(f"mkdir {dir_name}")
            created_dirs.append(dir_name)
        
        elif action == "create" and created_dirs:
            file_name = f"file_{random.randint(1, 100)}"
            size = random.randint(1, max_size)
            commands.append(f"create {file_name} {size}")
            created_files.append(file_name)
        
        elif action == "cd" and created_dirs:
            # Navegar para um diretório aleatório
            dir_name = random.choice(created_dirs)
            if dir_name != "RAIZ":  # Não navegar para a raiz se já estiver nela
                commands.append(f"cd {dir_name}")
                current_path = f"{current_path}/{dir_name}"
        
        elif action == "ls":
            commands.append("ls")
        
        elif action == "info":
            commands.append("info")
        
        elif action == "write" and created_files:
            file_name = random.choice(created_files)
            commands.append(f"write {file_name} 'Random data for {file_name}'")
        
        elif action == "read" and created_files:
            file_name = random.choice(created_files)
            commands.append(f"read {file_name}")
        
        elif action == "delete" and (created_files or created_dirs):
            if random.choice(["file", "dir"]) == "file" and created_files:
                file_name = random.choice(created_files)
                commands.append(f"delete {file_name}")
                created_files.remove(file_name)
            elif created_dirs:
                dir_name = random.choice(created_dirs)
                if dir_name != "RAIZ":  # Não deletar a raiz
                    commands.append(f"delete {dir_name}")
                    created_dirs.remove(dir_name)
    
    # Garantir que terminamos na raiz e executamos o comando tree
    if current_path != "/RAIZ":
        commands.append("cd /RAIZ")
    commands.append("tree")
    commands.append("info")
    return commands

def plot_results(results_fixed, results_random):
    """Gera gráficos comparativos de tempo de execução."""
    plt.figure()
    plt.bar(["Teste Fixo", "Teste Aleatório"], [results_fixed, results_random])
    plt.title("Comparação de Desempenho")
    plt.ylabel("Tempo de Execução (s)")
    plt.xlabel("Tipo de Teste")
    plt.savefig("performance_comparison.png")
    plt.show()

def main():
    # Teste com comandos fixos
    fs_fixed = FileSystem(disk_size=500)
    commands_fixed = [
        "mkdir docs",
        "mkdir images",
        "mkdir projects",
        "create file1.txt 10",
        "create file2.txt 15",
        "create file3.txt 25",
        "cd docs",
        "mkdir reports",
        "mkdir drafts",
        "create report1.txt 20",
        "create report2.txt 30",
        "cd reports",
        "create annual_report.txt 40",
        "create monthly_report.txt 20",
        "cd ..",
        "cd drafts",
        "create draft1.txt 10",
        "create draft2.txt 5",
        "write draft1.txt 'Initial draft content.'",
        "write draft2.txt 'Draft 2 content.'",
        "cd ..",
        "ls",
        "info",
        "cd ..",
        "cd images",
        "mkdir raw",
        "mkdir processed",
        "create image1.png 50",
        "create image2.jpg 40",
        "cd raw",
        "create raw_image1.png 30",
        "create raw_image2.png 35",
        "cd ..",
        "cd processed",
        "create processed_image1.png 25",
        "create processed_image2.jpg 20",
        "cd ..",
        "cd ..",
        "cd projects",
        "mkdir project1",
        "mkdir project2",
        "cd project1",
        "create proj1_file1.txt 10",
        "create proj1_file2.txt 20",
        "write proj1_file1.txt 'Content for project 1 file 1.'",
        "cd ..",
        "cd project2",
        "create proj2_file1.txt 15",
        "create proj2_file2.txt 25",
        "write proj2_file2.txt 'Content for project 2 file 2.'",
        "ls",
        "cd ..",
        "cd ..",
        "tree"
    ]

    fixed_time = run_test_sequence(fs_fixed, commands_fixed, "log_fixed.txt")

    # Teste com comandos aleatórios
    fs_random = FileSystem(disk_size=500)
    commands_random = generate_random_commands(50)
    random_time = run_test_sequence(fs_random, commands_random, "log_random.txt")

    # Geração de gráficos
    plot_results(fixed_time, random_time)

if __name__ == "__main__":
    main()
