#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo Commit - Implementação do sistema de commits

Este módulo define a classe Commit que representa um snapshot
do estado do repositório em um momento específico.

Cada commit contém:
- Timestamp da criação
- Mensagem descritiva
- Autor do commit
- Referência ao commit pai (para histórico)
- Árvore de arquivos (FileTree) do estado
"""

import datetime
from .file_tree import FileTree


class Commit:
    """
    Representa um commit no sistema VCS.
    
    Um commit é um snapshot do estado completo do repositório,
    incluindo todos os arquivos e diretórios em um momento específico.
    
    Attributes:
        timestamp (datetime): Data e hora da criação do commit
        message (str): Mensagem descritiva do commit
        author (str): Nome do autor do commit
        parent_commit_hash (str): Hash do commit pai (None para o primeiro commit)
        file_tree (FileTree): Árvore de arquivos deste commit
    """
    
    def __init__(self, message, author, parent_commit_hash=None):
        """
        Inicializa um novo commit.
        
        Args:
            message (str): Mensagem descritiva do commit
            author (str): Nome do autor do commit
            parent_commit_hash (str, optional): Hash do commit pai
        """
        if not message or not message.strip():
            raise ValueError("Mensagem do commit não pode estar vazia")
        
        if not author or not author.strip():
            raise ValueError("Autor do commit não pode estar vazio")
        
        self.timestamp = datetime.datetime.now()
        self.message = message.strip()
        self.author = author.strip()
        self.parent_commit_hash = parent_commit_hash
        self.file_tree = FileTree()
    
    def get_formatted_timestamp(self):
        """
        Retorna o timestamp formatado para exibição.
        
        Returns:
            str: Timestamp formatado como 'YYYY-MM-DD HH:MM:SS'
        """
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_short_message(self, max_length=50):
        """
        Retorna uma versão truncada da mensagem para exibição.
        
        Args:
            max_length (int): Comprimento máximo da mensagem
            
        Returns:
            str: Mensagem truncada se necessário
        """
        if len(self.message) <= max_length:
            return self.message
        return self.message[:max_length-3] + "..."
    
    def has_parent(self):
        """
        Verifica se este commit tem um commit pai.
        
        Returns:
            bool: True se tem pai, False se é o commit inicial
        """
        return self.parent_commit_hash is not None
    
    def get_file_count(self):
        """
        Retorna o número de arquivos neste commit.
        
        Returns:
            int: Número de arquivos no commit
        """
        return len(self.file_tree.get_all_files())
    
    def get_files_summary(self):
        """
        Retorna um resumo dos arquivos no commit.
        
        Returns:
            dict: Dicionário com estatísticas dos arquivos
        """
        files = self.file_tree.get_all_files()
        return {
            'total_files': len(files),
            'file_paths': [path for path, _ in files],
            'content_hashes': [hash_val for _, hash_val in files]
        }
    
    def is_initial_commit(self):
        """
        Verifica se este é o commit inicial (sem pai).
        
        Returns:
            bool: True se é o commit inicial, False caso contrário
        """
        return not self.has_parent()
    
    def get_commit_info(self):
        """
        Retorna informações completas do commit.
        
        Returns:
            dict: Dicionário com todas as informações do commit
        """
        return {
            'timestamp': self.get_formatted_timestamp(),
            'message': self.message,
            'author': self.author,
            'parent_hash': self.parent_commit_hash,
            'file_count': self.get_file_count(),
            'is_initial': self.is_initial_commit()
        }
    
    def __str__(self):
        """
        Representação em string do commit.
        
        Returns:
            str: Descrição do commit
        """
        parent_info = f"parent: {self.parent_commit_hash[:10]}..." if self.parent_commit_hash else "initial commit"
        return (f"Commit(message='{self.get_short_message()}', "
                f"author='{self.author}', "
                f"files={self.get_file_count()}, "
                f"{parent_info})")
    
    def __repr__(self):
        """
        Representação técnica do commit.
        
        Returns:
            str: Representação técnica
        """
        return (f"Commit(message='{self.message}', "
                f"author='{self.author}', "
                f"timestamp={self.timestamp}, "
                f"parent_commit_hash='{self.parent_commit_hash}', "
                f"files={self.get_file_count()})")
