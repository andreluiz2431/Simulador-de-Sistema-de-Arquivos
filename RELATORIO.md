# Relatório: Simulador de Sistema de Arquivos

---

## Arquitetura da Simulação

A simulação implementada é baseada em uma abstração de um sistema de arquivos, com três principais componentes que interagem para emular operações comuns de sistemas reais:

### 1. Disco Virtual
- O disco é representado como uma matriz de blocos (`blocks`), onde cada elemento pode estar livre (`0`) ou ocupado (`1`).
- Gerencia a alocação e liberação de espaço por meio de métodos:
  - `allocate(size)`: Aloca blocos contíguos necessários para armazenar um arquivo.
  - `free(blocks)`: Libera blocos ocupados para arquivos ou diretórios removidos.
  - `get_free_space()`: Calcula o espaço disponível no disco.

### 2. Sistema de Arquivos Hierárquico
- Diretórios e arquivos são representados como classes (`Directory` e `File`) com propriedades distintas:
  - **Diretórios**:
    - Contêm outros diretórios e arquivos em uma estrutura hierárquica.
  - **Arquivos**:
    - Associados a dados, tamanho (em blocos), e os blocos ocupados no disco.
- O diretório raiz (`RAIZ`) serve como o ponto de partida para todas as operações de navegação.

### 3. Interface e Comandos
- Comandos simulam operações reais, incluindo:
  - Criação de arquivos e diretórios (`create`, `mkdir`).
  - Navegação (`cd`).
  - Listagem (`ls`).
  - Escrita e leitura de arquivos (`write`, `read`).
  - Exclusão (`delete`).
  - Estrutura hierárquica (`tree`).
- Todas as operações são registradas em um log detalhado.

---

## Justificativa: Uso da Alocação Contígua

A alocação contígua foi escolhida como estratégia de armazenamento devido aos seguintes fatores:

### 1. Vantagens
- **Desempenho**:
  - Blocos armazenados sequencialmente permitem leitura e gravação mais rápidas, uma vez que as operações podem ser realizadas sem buscar blocos dispersos no disco.
- **Simplicidade**:
  - É simples de implementar e fácil de gerenciar, ideal para simulações educacionais ou de análise.
- **Uso Eficiente do Disco**:
  - Garante que não haja fragmentação interna dentro de arquivos, pois os blocos alocados são contíguos.

### 2. Desvantagens e Soluções na Simulação
- **Fragmentação Externa**:
  - Com o tempo, pode ser difícil alocar grandes arquivos devido à fragmentação externa (blocos livres não contíguos).
  - A simulação demonstra esses casos, exibindo erros de "espaço insuficiente" mesmo quando há blocos livres, o que ajuda a entender os desafios práticos dessa abordagem.
- **Redimensionamento**:
  - Arquivos que precisam crescer não podem expandir facilmente, exigindo realocação completa.
  - Essa limitação foi mantida para ilustrar o comportamento real da alocação contígua.

---

## Cenários de Testes

Aqui estão alguns cenários de testes para analisar e validar o comportamento do projeto:

### 1. Teste de Alocação Básica
- **Objetivo**: Validar a alocação e liberação de blocos no disco.
- **Cenário**:
  - Criar vários arquivos pequenos.
  - Remover alguns arquivos e tentar alocar um arquivo grande.
  - Verificar fragmentação externa.
- **Métricas**: 
  - Espaço total ocupado.
  - Espaço não utilizável devido à fragmentação externa.

### 2. Teste de Navegação e Hierarquia
- **Objetivo**: Testar operações de criação, navegação e listagem em uma estrutura de diretórios complexa.
- **Cenário**:
  - Criar diretórios aninhados e arquivos em diferentes níveis.
  - Navegar para subdiretórios e listar os conteúdos.
  - Verificar a consistência da hierarquia com o comando `tree`.
- **Métricas**:
  - Estrutura exibida pelo `tree`.
  - Consistência com os comandos executados.

### 3. Teste de Limite de Espaço
- **Objetivo**: Avaliar o comportamento quando o disco virtual está quase cheio.
- **Cenário**:
  - Preencher o disco com arquivos.
  - Criar e excluir arquivos para liberar espaço.
  - Tentar criar novos arquivos que excedam o espaço livre disponível.
- **Métricas**:
  - Erros gerados por espaço insuficiente.
  - Espaço recuperado após exclusões.

### 4. Teste de Operações em Arquivos
- **Objetivo**: Validar operações de leitura e escrita.
- **Cenário**:
  - Criar arquivos e escrever dados variados.
  - Ler os dados escritos para verificar a consistência.
  - Tentar ler arquivos inexistentes.
- **Métricas**:
  - Consistência entre os dados escritos e lidos.
  - Mensagens de erro ao acessar arquivos inexistentes.

### 5. Teste de Desempenho
- **Objetivo**: Comparar o tempo de execução entre cenários simples e complexos.
- **Cenário**:
  - Criar muitos arquivos pequenos em diretórios diferentes.
  - Comparar o tempo total de execução com arquivos maiores em um único diretório.
- **Métricas**:
  - Tempo total de execução.
  - Número de operações concluídas por segundo.

---

## Conexão com o Mundo Real

A simulação reflete desafios práticos enfrentados por sistemas de arquivos reais:
- **Fragmentação**: A fragmentação externa é um problema crítico em discos rígidos e sistemas que utilizam alocação contígua.
- **Gerenciamento Hierárquico**: A criação e navegação em diretórios refletem a necessidade de organizar dados eficientemente.
- **Limitação de Recursos**: O teste de limites do disco simula condições de sistemas sobrecarregados.

---

Com esses testes, o projeto oferece uma compreensão prática e detalhada de sistemas de arquivos, ajudando a explorar os prós e contras da alocação contígua e outros desafios.
