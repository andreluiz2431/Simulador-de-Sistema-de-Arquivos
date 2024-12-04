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
    # Cenário 1: Teste de Alocação Básica
    print("Executando Cenário 1: Teste de Alocação Básica...")
    fs_allocation = FileSystem(disk_size=100)
    commands_allocation = [
        "create file1.txt 10",
        "create file2.txt 15",
        "create file3.txt 30",
        "delete file2.txt",
        "create file4.txt 20",
        "info",
        "tree"
    ]
    allocation_time = run_test_sequence(fs_allocation, commands_allocation, "log_allocation.txt")

    # Cenário 2: Teste de Navegação e Hierarquia
    print("Executando Cenário 2: Teste de Navegação e Hierarquia...")
    fs_navigation = FileSystem(disk_size=100)
    commands_navigation = [
        "mkdir docs",
        "mkdir images",
        "cd docs",
        "mkdir reports",
        "mkdir drafts",
        "create report1.txt 10",
        "cd reports",
        "create annual_report.txt 20",
        "cd ..",
        "cd drafts",
        "create draft1.txt 5",
        "cd ..",
        "cd ..",
        "cd images",
        "mkdir raw",
        "mkdir processed",
        "info",
        "tree"
    ]
    navigation_time = run_test_sequence(fs_navigation, commands_navigation, "log_navigation.txt")

    # Cenário 3: Teste de Limite de Espaço
    print("Executando Cenário 3: Teste de Limite de Espaço...")
    fs_limit = FileSystem(disk_size=100)
    commands_limit = [
        "create file1.txt 30",
        "create file2.txt 30",
        "create file3.txt 30",
        "create file4.txt 20",  # Deve falhar
        "delete file1.txt",
        "create file4.txt 20",  # Deve ser bem-sucedido agora
        "info",
        "tree"
    ]
    limit_time = run_test_sequence(fs_limit, commands_limit, "log_limit.txt")

    # Cenário 4: Teste de Operações em Arquivos
    print("Executando Cenário 4: Teste de Operações em Arquivos...")
    fs_operations = FileSystem(disk_size=100)
    commands_operations = [
        "create file1.txt 10",
        "write file1.txt 'This is a test file.'",
        "read file1.txt",
        "delete file1.txt",
        "read file1.txt",  # Deve falhar
        "info",
        "tree"
    ]
    operations_time = run_test_sequence(fs_operations, commands_operations, "log_operations.txt")

    # Cenário 5: Teste de Desempenho
    print("Executando Cenário 5: Teste de Desempenho...")
    fs_performance = FileSystem(disk_size=500)
    commands_performance = [
        f"create file{i}.txt {random.randint(1, 50)}" for i in range(1, 50)
    ]
    commands_performance += ["info", "tree"]
    performance_time = run_test_sequence(fs_performance, commands_performance, "log_performance.txt")

    # Geração de gráficos para análise
    times = [allocation_time, navigation_time, limit_time, operations_time, performance_time]
    labels = [
        "Alocação Básica",
        "Navegação e Hierarquia",
        "Limite de Espaço",
        "Operações em Arquivos",
        "Desempenho"
    ]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, times, color="skyblue")
    plt.title("Tempo de Execução dos Cenários")
    plt.ylabel("Tempo de Execução (s)")
    plt.xlabel("Cenários de Teste")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("test_scenarios_performance.png")
    plt.show()

if __name__ == "__main__":
    main()
