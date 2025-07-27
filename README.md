# IFTSI-Sistema-de-Controle-de-Vers-es-VCS

Um sistema de controle de versões profissional implementado em Python usando árvores N-árias com arquitetura modular.

## Características

- **Arquitetura Modular**: Código organizado em módulos especializados
- **Árvore N-ária**: Estrutura de dados que permite múltiplos filhos por nó
- **Interface Gráfica Avançada**: GUI profissional usando Tkinter
- **Controle de Versões Completo**: Commit, checkout, histórico e status
- **Hash SHA-1**: Para integridade dos dados
- **Serialização Robusta**: Usando pickle com tratamento de erros
- **Documentação Completa**: Docstrings detalhadas em todos os módulos

## Estrutura do Projeto

```
meu_vcs/
├── vcs_core/              # Módulo core do sistema VCS
│   ├── __init__.py        # Configuração do módulo
│   ├── node.py           # Implementação do nó N-ário
│   ├── file_tree.py      # Árvore de arquivos
│   ├── commit.py         # Sistema de commits
│   └── repository.py     # Repositório e operações VCS
├── main_gui.py           # Interface gráfica modular
└── README.md             # Este arquivo
```

## Como usar

### Instalação

1. Certifique-se de ter Python 3.7+ instalado
2. Clone ou baixe este repositório
3. Navegue até a pasta do projeto

### Execução

```bash
python main_gui.py
```

### Funcionalidades

1. **Criar/Abrir Repositório**: Selecione uma pasta para inicializar ou abrir um repositório
2. **Fazer Commit**: Salva o estado atual dos arquivos com autor personalizado
3. **Ver Histórico**: Lista todos os commits com informações detalhadas (hash, autor, data, arquivos)
4. **Fazer Checkout**: Restaura o estado de um commit anterior
5. **Status**: Visualiza informações do repositório atual em tempo real

## Arquitetura Modular

### Módulo `vcs_core`

#### `node.py` - Nó da Árvore N-ária
- Classe `Node`: Representa arquivos e diretórios
- Suporte a múltiplos filhos (estrutura N-ária)
- Métodos para navegação e manipulação

#### `file_tree.py` - Árvore de Arquivos
- Classe `FileTree`: Gerencia estrutura hierárquica
- Inserção inteligente de caminhos
- Navegação e busca na árvore
- Estatísticas e visualização

#### `commit.py` - Sistema de Commits
- Classe `Commit`: Representa snapshots do repositório
- Timestamp automático e metadados
- Histórico com commits pai
- Informações detalhadas

#### `repository.py` - Repositório VCS
- Classe `Repository`: Operações principais do VCS
- Inicialização de repositórios
- Criação e gerenciamento de commits
- Checkout com reconstrução completa
- Histórico e status

### Interface Gráfica

#### `main_gui.py` - GUI Profissional
- Classe `VCSApp`: Interface Tkinter avançada
- Design responsivo e intuitivo com scrollbars
- Tratamento robusto de erros
- Feedback visual para todas as operações
- Exibição detalhada do histórico com autor, data e estatísticas
- Interface limpa e focada na experiência do usuário

## Estrutura Técnica

### Árvore N-ária
Cada nó pode ter múltiplos filhos, permitindo representar:
- Diretórios com vários arquivos
- Estruturas hierárquicas complexas
- Navegação eficiente

### Hash de Conteúdo
- SHA-1 para identificação única de arquivos
- Detecção automática de mudanças
- Integridade dos dados

### Commits
- Snapshots completos da árvore
- Metadados ricos (autor, timestamp, mensagem)
- Histórico linear com commits pai

### Checkout
- Reconstrução completa do estado
- Limpeza segura do diretório
- Restauração precisa dos arquivos

### Interface Gráfica
- **Design Profissional**: Interface limpa com cores e ícones intuitivos
- **Histórico Visual**: Lista detalhada com hash, autor, data e número de arquivos
- **Feedback Interativo**: Confirmações e mensagens de status em tempo real
- **Scrollbars**: Suporte para históricos longos com navegação fluida
- **Autor Personalizado**: Solicitação do nome do autor a cada commit
- **Indicador HEAD**: Marca visual do commit atual no histórico

## Vantagens da Versão Modular

1. **Manutenibilidade**: Código organizado e fácil de manter
2. **Reutilização**: Módulos podem ser usados independentemente
3. **Testabilidade**: Cada módulo pode ser testado isoladamente
4. **Extensibilidade**: Fácil adição de novas funcionalidades
5. **Legibilidade**: Código mais limpo e documentado
6. **Profissionalismo**: Estrutura adequada para projetos reais

## Requisitos

- **Python 3.7+**: Versão mínima recomendada
- **Bibliotecas padrão**: tkinter, os, shutil, hashlib, pickle, datetime
- **Sistema Operacional**: Windows, Linux, macOS
- **Memória**: Mínimo 50MB de RAM disponível
- **Espaço em disco**: Varia conforme o tamanho dos repositórios

### Dependências
Todas as dependências são bibliotecas padrão do Python, não sendo necessário instalar pacotes externos.

## Limitações e Considerações

- **Uso Acadêmico**: Projetado para fins educacionais e demonstração de conceitos
- **Repositórios Locais**: Não suporta repositórios remotos (como Git)
- **Branching**: Implementa histórico linear (sem branches)
- **Tamanho**: Adequado para projetos pequenos a médios
- **Concorrência**: Não suporta múltiplos usuários simultâneos

## Comparação com Versão Monolítica

| Aspecto | Monolítica | Modular |
|---------|------------|---------|
| Linhas de código | ~300 | ~900+ |
| Módulos | 1 arquivo | 5 módulos + GUI |
| Documentação | Básica | Completa com docstrings |
| Manutenibilidade | Média | Alta |
| Testabilidade | Baixa | Alta |
| Interface | Simples | Profissional |
| Funcionalidades | Básicas | Avançadas |
| Autor nos commits | Fixo | Personalizável |
| Profissionalismo | Acadêmico | Industrial |

## Autor

Milton - 2025  
Projeto Acadêmico - IFTSI  
Disciplina: Estruturas de Dados

| Aspecto | Monolítica | Modular |
|---------|------------|---------|
| Linhas de código | ~300 | ~900+ |
| Módulos | 1 arquivo | 5 módulos + GUI |
| Documentação | Básica | Completa com docstrings |
| Manutenibilidade | Média | Alta |
| Testabilidade | Baixa | Alta |
| Interface | Simples | Profissional |
| Funcionalidades | Básicas | Avançadas |
| Autor nos commits | Fixo | Personalizável |
| Profissionalismo | Acadêmico | Industrial |

## Autor

Milton - 2025  
Projeto Acadêmico - IFTSI  
Disciplina: Estruturas de Dados
