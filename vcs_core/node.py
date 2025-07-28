#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo Node - Implementação do nó da árvore N-ária

Este módulo define a classe Node que representa um nó na estrutura
de árvore N-ária usada para organizar arquivos e diretórios no VCS.

Características:
- Suporta tanto arquivos quanto diretórios
- Estrutura N-ária (cada nó pode ter múltiplos filhos)
- Armazena hash do conteúdo para arquivos
- Permite navegação hierárquica
"""


class Node:
    """
    Representa um nó na árvore de arquivos (FileTree).
    
    Um nó pode representar tanto um arquivo quanto um diretório.
    Para diretórios, o nó contém uma coleção de nós filhos.
    Para arquivos, o nó armazena o hash do conteúdo.
    
    Attributes:
        name (str): Nome do arquivo ou diretório
        is_file (bool): True se é um arquivo, False se é um diretório
        content_hash (str): Hash SHA-1 do conteúdo (apenas para arquivos)
        file_size (int): Tamanho do arquivo em bytes (apenas para arquivos)
        children (dict): Dicionário de nós filhos {nome: Node}
    """
    
    def __init__(self, name, is_file=False, content_hash=None, file_size=0):
        """
        Inicializa um novo nó.
        
        Args:
            name (str): Nome do arquivo ou diretório
            is_file (bool): True se é um arquivo, False se é um diretório
            content_hash (str, optional): Hash do conteúdo para arquivos
            file_size (int): Tamanho do arquivo em bytes (apenas para arquivos)
        """
        self.name = name
        self.is_file = is_file
        self.content_hash = content_hash
        self.file_size = file_size if is_file else 0
        self.children = {}  # Dicionário para estrutura N-ária
    
    def add_child(self, child_node):
        """
        Adiciona um nó filho a este nó.
        
        Args:
            child_node (Node): O nó filho a ser adicionado
        """
        if not isinstance(child_node, Node):
            raise TypeError("child_node deve ser uma instância de Node")
        
        self.children[child_node.name] = child_node
    
    def get_child(self, name):
        """
        Obtém um nó filho pelo nome.
        
        Args:
            name (str): Nome do nó filho
            
        Returns:
            Node or None: O nó filho ou None se não encontrado
        """
        return self.children.get(name)
    
    def has_child(self, name):
        """
        Verifica se este nó tem um filho com o nome especificado.
        
        Args:
            name (str): Nome do nó filho
            
        Returns:
            bool: True se o filho existe, False caso contrário
        """
        return name in self.children
    
    def is_directory(self):
        """
        Verifica se este nó representa um diretório.
        
        Returns:
            bool: True se é um diretório, False se é um arquivo
        """
        return not self.is_file
    
    def get_children_count(self):
        """
        Retorna o número de filhos deste nó.
        
        Returns:
            int: Número de nós filhos
        """
        return len(self.children)
    
    def get_file_info(self):
        """
        Retorna informações detalhadas do arquivo.
        
        Returns:
            dict: Dicionário com informações do arquivo
        """
        return {
            'name': self.name,
            'is_file': self.is_file,
            'size': self.file_size,
            'hash': self.content_hash,
            'children_count': len(self.children)
        }
    
    def format_file_size(self):
        """
        Formata o tamanho do arquivo para exibição.
        
        Returns:
            str: Tamanho formatado (ex: "1.2 KB", "3.4 MB")
        """
        if not self.is_file:
            return "N/A"
        
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def __str__(self):
        """
        Representação em string do nó.
        
        Returns:
            str: Descrição do nó
        """
        node_type = "arquivo" if self.is_file else "diretório"
        return f"Node(name='{self.name}', type={node_type}, children={len(self.children)})"
    
    def __repr__(self):
        """
        Representação técnica do nó.
        
        Returns:
            str: Representação técnica
        """
        return (f"Node(name='{self.name}', is_file={self.is_file}, "
                f"content_hash='{self.content_hash}', children={len(self.children)})")
