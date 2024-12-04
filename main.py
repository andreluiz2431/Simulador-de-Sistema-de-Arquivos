import os

# Representação do disco virtual
class VirtualDisk:
    def __init__(self, size):
        self.size = size
        self.blocks = [0] * size  # 0 = bloco livre, 1 = bloco ocupado

    def allocate(self, size):
        """Aloca blocos contíguos."""
        free_blocks = [i for i in range(self.size) if self.blocks[i] == 0]
        if len(free_blocks) < size:
            return None  # Espaço insuficiente

        allocated_blocks = free_blocks[:size]
        for block in allocated_blocks:
            self.blocks[block] = 1
        return allocated_blocks

    def free(self, blocks):
        """Libera blocos especificados."""
        for block in blocks:
            if block < self.size:
                self.blocks[block] = 0

    def get_free_space(self):
        return self.blocks.count(0)

# Representação de diretórios e arquivos
class File:
    def __init__(self, name, size=0):
        self.name = name
        self.size = size
        self.data = ""
        self.blocks = []

class Directory:
    def __init__(self, name):
        self.name = name
        self.contents = {}  # Nome -> (Diretório ou Arquivo)

# Sistema de Arquivos
class FileSystem:
    def __init__(self, disk_size):
        self.disk = VirtualDisk(disk_size)
        self.root = Directory("RAIZ")
        self.current_dir = self.root
        self.path = "/RAIZ"
        self.log = []

    def log_operation(self, command, result, details=""):
        """Adiciona uma entrada ao log de operações."""
        self.log.append(f"Comando: {command}\nResultado: {result}\nDetalhes: {details}\n")

    def mkdir(self, name):
        if name in self.current_dir.contents:
            self.log_operation(f"mkdir {name}", "Erro", "Diretório já existe.")
            return "Erro: Diretório já existe."

        self.current_dir.contents[name] = Directory(name)
        self.log_operation(f"mkdir {name}", "Sucesso", f"Diretório criado: {name}.")
        return f"Diretório '{name}' criado com sucesso."

    def create_file(self, name, size):
        if name in self.current_dir.contents:
            self.log_operation(f"create {name} {size}", "Erro", "Arquivo já existe.")
            return "Erro: Arquivo já existe."

        blocks = self.disk.allocate(size)
        if blocks is None:
            self.log_operation(f"create {name} {size}", "Erro", "Espaço insuficiente.")
            return "Erro: Espaço insuficiente."

        file = File(name, size)
        file.blocks = blocks
        self.current_dir.contents[name] = file
        self.log_operation(
            f"create {name} {size}",
            "Sucesso",
            f"Arquivo criado: {name}, Blocos alocados: {blocks}."
        )
        return f"Arquivo '{name}' criado com sucesso."

    def delete(self, name):
        if name not in self.current_dir.contents:
            self.log_operation(f"delete {name}", "Erro", "Arquivo/Diretório não encontrado.")
            return "Erro: Arquivo/Diretório não encontrado."

        obj = self.current_dir.contents[name]
        if isinstance(obj, File):
            self.disk.free(obj.blocks)
            self.log_operation(
                f"delete {name}",
                "Sucesso",
                f"Arquivo excluído: {name}, Blocos liberados: {obj.blocks}."
            )
        elif isinstance(obj, Directory):
            if obj.contents:
                self.log_operation(f"delete {name}", "Erro", "Diretório não está vazio.")
                return "Erro: Diretório não está vazio."
            self.log_operation(f"delete {name}", "Sucesso", f"Diretório excluído: {name}.")

        del self.current_dir.contents[name]
        return f"'{name}' excluído com sucesso."

    def ls(self):
        contents = [f"[DIR] {name}" if isinstance(obj, Directory) else f"[FILE] {name}"
                    for name, obj in self.current_dir.contents.items()]
        self.log_operation("ls", "Sucesso", f"Conteúdo: {contents}")
        return "\n".join(contents)

    def cd(self, name):
        if name == "..":
            # Caso especial: Verificar se já estamos na raiz
            if self.current_dir == self.root:
                self.log_operation("cd ..", "Erro", "Já está no diretório raiz.")
                return "Erro: Já está no diretório raiz."

            # Navegar para o diretório pai
            parts = self.path.split("/")
            parent_path = "/".join(parts[:-1]) or "/RAIZ"
            self.path = parent_path

            # Reconstruir `current_dir` a partir do novo caminho
            self.current_dir = self.root
            if parts[-2] == "RAIZ":
                self.current_dir = self.root
                self.log_operation("cd ..", "Sucesso", f"Navegou para {self.path}.")
                return f"Navegou para {self.path}."
            self.current_dir = self.current_dir.contents[parts[-2]]
            self.log_operation("cd ..", "Sucesso", f"Navegou para {self.path}.")
            return f"Navegou para {self.path}."

        # Navegar para um subdiretório
        if name not in self.current_dir.contents or not isinstance(self.current_dir.contents[name], Directory):
            self.log_operation(f"cd {name}", "Erro", "Diretório não encontrado.")
            return "Erro: Diretório não encontrado."

        # Atualizar o diretório atual
        self.current_dir = self.current_dir.contents[name]
        self.path += f"/{name}"
        self.log_operation(f"cd {name}", "Sucesso", f"Navegou para {self.path}.")
        return f"Navegou para {self.path}."

    def info(self):
        free_space = self.disk.get_free_space()
        total_space = self.disk.size
        details = f"Tamanho do disco: {total_space}, Espaço livre: {free_space}, Caminho atual: {self.path}."
        self.log_operation("info", "Sucesso", details)
        return details

    def show_log(self):
        return "\n".join(self.log)

    def write(self, path, data):
        """Escreve dados em um arquivo."""
        # Caminho completo dividido
        parts = path.strip("/").split("/")
        file_name = parts[-1]
        dir_path = parts[:-1]

        # Navegar até o diretório que contém o arquivo
        current = self.root
        for part in dir_path:
            if part in current.contents and isinstance(current.contents[part], Directory):
                current = current.contents[part]
            else:
                self.log_operation(f"write {path} {data}", "Erro", "Caminho inválido.")
                return "Erro: Caminho inválido."

        # Verificar se o arquivo existe
        if file_name not in current.contents or not isinstance(current.contents[file_name], File):
            self.log_operation(f"write {path} {data}", "Erro", "Arquivo não encontrado.")
            return "Erro: Arquivo não encontrado."

        # Escrever os dados no arquivo
        current.contents[file_name].data = data
        self.log_operation(f"write {path} {data}", "Sucesso", f"Dados escritos no arquivo: {file_name}.")
        return f"Dados escritos no arquivo '{file_name}'."

    def read(self, path):
        """Lê dados de um arquivo."""
        # Caminho completo dividido
        parts = path.strip("/").split("/")
        file_name = parts[-1]
        dir_path = parts[:-1]

        # Navegar até o diretório que contém o arquivo
        current = self.root
        for part in dir_path:
            if part in current.contents and isinstance(current.contents[part], Directory):
                current = current.contents[part]
            else:
                self.log_operation(f"read {path}", "Erro", "Caminho inválido.")
                return "Erro: Caminho inválido."

        # Verificar se o arquivo existe
        if file_name not in current.contents or not isinstance(current.contents[file_name], File):
            self.log_operation(f"read {path}", "Erro", "Arquivo não encontrado.")
            return "Erro: Arquivo não encontrado."

        # Retornar os dados do arquivo
        data = current.contents[file_name].data
        self.log_operation(f"read {path}", "Sucesso", f"Dados lidos do arquivo: {file_name}.")
        return f"Conteúdo do arquivo '{file_name}': {data}"

    def tree(self, current=None, prefix=""):
        """Exibe a estrutura hierárquica do sistema de arquivos."""
        if current is None:
            current = self.root  # Começa na raiz

        output = ""
        for name, obj in current.contents.items():
            if isinstance(obj, Directory):
                output += f"{prefix}[DIR] {name}\n"
                output += self.tree(obj, prefix + "    ")  # Recurso recursivo para subdiretórios
            elif isinstance(obj, File):
                output += f"{prefix}[FILE] {name} ({obj.size} blocos)\n"

        return output

# Interface CLI
def main():
    fs = FileSystem(disk_size=100)
    print("Simulador de Sistema de Arquivos\n")
    while True:
        command = input(f"{fs.path}> ").strip()
        if command.startswith("mkdir"):
            _, name = command.split(maxsplit=1)
            print(fs.mkdir(name))
        elif command.startswith("create"):
            _, name, size = command.split(maxsplit=2)
            print(fs.create_file(name, int(size)))
        elif command == "ls":
            print(fs.ls())
        elif command.startswith("cd"):
            _, name = command.split(maxsplit=1)
            print(fs.cd(name))
        elif command.startswith("delete"):
            _, name = command.split(maxsplit=1)
            print(fs.delete(name))
        elif command == "info":
            print(fs.info())
        elif command.startswith("write"):
            _, path, data = command.split(maxsplit=2)
            print(fs.write(path, data))
        elif command.startswith("read"):
            _, path = command.split(maxsplit=1)
            print(fs.read(path))
        elif command == "log":
            print(fs.show_log())
        elif command == "tree":
            print(fs.tree())
        elif command == "exit":
            break
        else:
            print("Comando desconhecido.")

if __name__ == "__main__":
    main()
