#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo FileTree - Implementação da árvore de arquivos

Este módulo define a classe FileTree que gerencia a estrutura
hierárquica de arquivos e diretórios usando uma árvore N-ária.

A FileTree é responsável por:
- Manter a estrutura de diretórios e arquivos
- Inserir novos caminhos na árvore
- Navegar pela estrutura hierárquica
- Suportar múltiplos filhos por nó (N-ário)
"""

import os
from .node import Node


class FileTree:
    """
    Representa a árvore de arquivos do sistema VCS.
    
    A FileTree usa uma estrutura de árvore N-ária onde cada nó pode
    ter múltiplos filhos, permitindo representar diretórios com
    múltiplos arquivos e subdiretórios.
    
    Attributes:
        root (Node): Nó raiz da árvore
    """
    
    def __init__(self):
        """
        Inicializa uma nova árvore de arquivos.
        
        Cria o nó raiz que representa o diretório base.
        """
        self.root = Node("/", is_file=False)
    
    def insert(self, path, content_hash=None, file_size=0):
        """
        Insere um caminho na árvore de arquivos.
        
        Percorre o caminho criando nós intermediários conforme necessário.
        O último elemento do caminho será marcado como arquivo se
        content_hash for fornecido, caso contrário será um diretório.
        
        Args:
            path (str): Caminho do arquivo/diretório a ser inserido
            content_hash (str, optional): Hash do conteúdo para arquivos
            file_size (int): Tamanho do arquivo em bytes
        """
        if not path or path == "/":
            return
        
        # Normaliza o caminho removendo separadores duplos e vazios
        parts = [part for part in path.split(os.sep) if part]
        if not parts:
            return
        
        current_node = self.root
        
        # Percorre cada parte do caminho
        for i, part in enumerate(parts):
            is_last_part = (i == len(parts) - 1)
            
            # Verifica se o nó filho já existe
            if not current_node.has_child(part):
                # Determina se é arquivo ou diretório
                is_file = is_last_part and content_hash is not None
                new_node = Node(part, is_file=is_file, content_hash=content_hash if is_file else None, file_size=file_size if is_file else 0)
                current_node.add_child(new_node)
            
            # Move para o próximo nó
            current_node = current_node.get_child(part)
            
            # Se é a última parte e temos hash, atualiza o nó existente
            if is_last_part and content_hash is not None:
                current_node.is_file = True
                current_node.content_hash = content_hash
                current_node.file_size = file_size
    
    def find_node(self, path):
        """
        Encontra um nó específico pelo caminho.
        
        Args:
            path (str): Caminho para o nó desejado
            
        Returns:
            Node or None: O nó encontrado ou None se não existe
        """
        if not path or path == "/":
            return self.root
        
        parts = [part for part in path.split(os.sep) if part]
        current_node = self.root
        
        for part in parts:
            if not current_node.has_child(part):
                return None
            current_node = current_node.get_child(part)
        
        return current_node
    
    def get_all_files(self):
        """
        Retorna todos os arquivos da árvore com seus caminhos e nós.
        
        Returns:
            list: Lista de tuplas (caminho, node)
        """
        files = []
        self._collect_files(self.root, "", files)
        return files
    
    def _collect_files(self, node, current_path, files):
        """
        Método auxiliar recursivo para coletar todos os arquivos.
        
        Args:
            node (Node): Nó atual
            current_path (str): Caminho atual
            files (list): Lista para armazenar os arquivos encontrados
        """
        for child_name, child_node in node.children.items():
            child_path = os.path.join(current_path, child_name) if current_path else child_name
            
            if child_node.is_file:
                files.append((child_path, child_node))
            else:
                self._collect_files(child_node, child_path, files)
    
    def get_directory_structure(self):
        """
        Retorna a estrutura de diretórios como uma lista hierárquica.
        
        Returns:
            list: Estrutura hierárquica de diretórios e arquivos
        """
        structure = []
        self._build_structure(self.root, "", structure, 0)
        return structure
    
    def _build_structure(self, node, current_path, structure, level):
        """
        Método auxiliar recursivo para construir a estrutura hierárquica.
        
        Args:
            node (Node): Nó atual
            current_path (str): Caminho atual
            structure (list): Lista para armazenar a estrutura
            level (int): Nível de indentação
        """
        for child_name, child_node in sorted(node.children.items()):
            indent = "  " * level
            node_type = "📄" if child_node.is_file else "📁"
            child_path = os.path.join(current_path, child_name) if current_path else child_name
            
            structure.append(f"{indent}{node_type} {child_name}")
            
            if not child_node.is_file:
                self._build_structure(child_node, child_path, structure, level + 1)
    
    def is_empty(self):
        """
        Verifica se a árvore está vazia.
        
        Returns:
            bool: True se a árvore não tem filhos, False caso contrário
        """
        return self.root.get_children_count() == 0
    
    def __str__(self):
        """
        Representação em string da árvore.
        
        Returns:
            str: Estrutura da árvore formatada
        """
        if self.is_empty():
            return "FileTree(empty)"
        
        structure = self.get_directory_structure()
        return f"FileTree:\n" + "\n".join(structure)
    
    def find_node(self, path):
        """
        Encontra um nó específico pelo caminho.
        
        Args:
            path (str): Caminho do arquivo/diretório
            
        Returns:
            Node ou None: O nó encontrado ou None se não existir
        """
        if not path or path == ".":
            return self.root
        
        # Normalizar o caminho
        path = path.replace('\\', '/')
        parts = [p for p in path.split('/') if p]
        
        current_node = self.root
        for part in parts:
            if part in current_node.children:
                current_node = current_node.children[part]
            else:
                return None
        
        return current_node
    
    def get_tree_visualization(self, node=None, prefix="", is_last=True):
        """
        Retorna uma visualização em árvore ASCII.
        
        Args:
            node (Node): Nó inicial (padrão: root)
            prefix (str): Prefixo para indentação
            is_last (bool): Se é o último filho
            
        Returns:
            str: Visualização em ASCII
        """
        if node is None:
            node = self.root
        
        result = ""
        connector = "└── " if is_last else "├── "
        icon = "📄 " if node.is_file else "📁 "
        
        if node != self.root:
            result += prefix + connector + icon + node.name + "\n"
        
        children = list(node.children.items())
        for i, (child_name, child_node) in enumerate(children):
            is_child_last = (i == len(children) - 1)
            extension = "    " if is_last else "│   "
            result += self.get_tree_visualization(
                child_node, 
                prefix + extension, 
                is_child_last
            )
        
        return result
    
    def print_tree(self):
        """
        Imprime a árvore de arquivos de forma visual.
        """
        print(self.get_tree_visualization(self.root))
