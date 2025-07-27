#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo Repository - Implementação do repositório VCS

Este módulo define a classe Repository que gerencia todas as
operações do sistema de controle de versões.

O Repository é responsável por:
- Inicializar repositórios
- Criar e gerenciar commits
- Realizar operações de checkout
- Manter histórico de versões
- Gerenciar objetos e metadados
"""

import os
import shutil
import hashlib
import pickle
from .commit import Commit


class Repository:
    """
    Representa um repositório do sistema VCS.
    
    O Repository gerencia todos os aspectos do controle de versões,
    incluindo a criação de commits, checkout de versões anteriores,
    e manutenção do histórico.
    
    Attributes:
        work_dir (str): Diretório de trabalho do repositório
        vcs_dir (str): Diretório .myvcs com metadados
        objects_dir (str): Diretório para objetos (conteúdo dos arquivos)
        commits_dir (str): Diretório para commits
        head_file (str): Arquivo que aponta para o commit atual
    """
    
    def __init__(self, work_dir):
        """
        Inicializa um repositório.
        
        Args:
            work_dir (str): Caminho para o diretório de trabalho
        """
        self.work_dir = os.path.abspath(work_dir)
        self.vcs_dir = os.path.join(self.work_dir, ".myvcs")
        self.objects_dir = os.path.join(self.vcs_dir, "objects")
        self.commits_dir = os.path.join(self.vcs_dir, "commits")
        self.head_file = os.path.join(self.vcs_dir, "HEAD")
    
    def _calculate_hash(self, data):
        """
        Calcula o hash SHA-1 dos dados.
        
        Args:
            data (bytes): Dados para calcular o hash
            
        Returns:
            str: Hash SHA-1 em hexadecimal
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        sha1 = hashlib.sha1()
        sha1.update(data)
        return sha1.hexdigest()
    
    def init(self):
        """
        Inicializa um novo repositório.
        
        Cria a estrutura de diretórios necessária e o commit inicial.
        
        Raises:
            Exception: Se o repositório já existe
        """
        if os.path.exists(self.vcs_dir):
            raise Exception("Repositório já existente.")
        
        # Cria estrutura de diretórios
        os.makedirs(self.objects_dir)
        os.makedirs(self.commits_dir)
        
        # Cria commit inicial
        root_commit = Commit("Commit inicial do repositório", "system")
        commit_data = pickle.dumps(root_commit)
        commit_hash = self._calculate_hash(commit_data)
        
        # Salva o commit inicial
        commit_file = os.path.join(self.commits_dir, commit_hash)
        with open(commit_file, "wb") as f:
            f.write(commit_data)
        
        # Define como HEAD
        with open(self.head_file, "w") as f:
            f.write(commit_hash)
        
        print(f"Repositório inicializado em: {self.work_dir}")
        print(f"Commit inicial criado: {commit_hash[:10]}")
    
    def is_repository(self):
        """
        Verifica se o diretório é um repositório válido.
        
        Returns:
            bool: True se é um repositório, False caso contrário
        """
        return os.path.exists(self.vcs_dir) and os.path.exists(self.head_file)
    
    def get_head_hash(self):
        """
        Obtém o hash do commit atual (HEAD).
        
        Returns:
            str or None: Hash do commit atual ou None se não existe
        """
        if not os.path.exists(self.head_file):
            return None
        
        try:
            with open(self.head_file, "r") as f:
                return f.read().strip()
        except IOError:
            return None
    
    def commit(self, message, author="Default User"):
        """
        Cria um novo commit com o estado atual do diretório.
        
        Args:
            message (str): Mensagem do commit
            author (str): Nome do autor
            
        Returns:
            str: Hash do novo commit
            
        Raises:
            Exception: Se não é um repositório válido
        """
        if not self.is_repository():
            raise Exception("Não é um repositório válido. Use init() primeiro.")
        
        parent_hash = self.get_head_hash()
        new_commit = Commit(message, author, parent_hash)
        
        print(f"Criando commit: {message}")
        files_found = 0
        
        # Percorre todos os arquivos no diretório de trabalho
        for root, dirs, files in os.walk(self.work_dir):
            # Ignora o diretório .myvcs
            if self.vcs_dir in root:
                continue
            
            for file_name in files:
                file_path = os.path.join(root, file_name)
                
                try:
                    # Lê o conteúdo do arquivo
                    with open(file_path, "rb") as f:
                        content = f.read()
                    
                    # Calcula o hash do conteúdo
                    content_hash = self._calculate_hash(content)
                    
                    # Salva o objeto se não existe
                    object_path = os.path.join(self.objects_dir, content_hash)
                    if not os.path.exists(object_path):
                        with open(object_path, "wb") as obj_f:
                            obj_f.write(content)
                        print(f"Novo objeto salvo: {content_hash[:7]} para {file_name}")
                    else:
                        print(f"Objeto já existe: {content_hash[:7]} para {file_name}")
                    
                    # Adiciona à árvore do commit
                    relative_path = os.path.relpath(file_path, self.work_dir)
                    new_commit.file_tree.insert(relative_path, content_hash)
                    files_found += 1
                    print(f"Arquivo adicionado à árvore: {relative_path}")
                
                except IOError as e:
                    print(f"Erro ao ler arquivo {file_path}: {e}")
                    continue
        
        print(f"Total de arquivos no commit: {files_found}")
        
        # Salva o commit
        commit_data = pickle.dumps(new_commit)
        commit_hash = self._calculate_hash(commit_data)
        
        commit_file = os.path.join(self.commits_dir, commit_hash)
        with open(commit_file, "wb") as f:
            f.write(commit_data)
        
        # Atualiza HEAD
        with open(self.head_file, "w") as f:
            f.write(commit_hash)
        
        print(f"Novo commit criado: {commit_hash[:10]} - {message}")
        return commit_hash
    
    def checkout(self, commit_hash):
        """
        Restaura o estado do repositório para um commit específico.
        
        Args:
            commit_hash (str): Hash do commit para restaurar
            
        Raises:
            Exception: Se o commit não existe ou há erro na restauração
        """
        if not self.is_repository():
            raise Exception("Não é um repositório válido.")
        
        commit_path = os.path.join(self.commits_dir, commit_hash)
        if not os.path.exists(commit_path):
            raise Exception("Commit não encontrado.")
        
        print(f"Fazendo checkout para commit: {commit_hash[:10]}")
        
        # Carrega o commit
        try:
            with open(commit_path, "rb") as f:
                commit_obj = pickle.load(f)
        except (IOError, pickle.PickleError) as e:
            raise Exception(f"Erro ao carregar commit: {e}")
        
        print(f"Commit carregado: {commit_obj.message}")
        
        # Lista arquivos antes da limpeza
        files_before = [f for f in os.listdir(self.work_dir) if f != ".myvcs"]
        print(f"Arquivos antes da limpeza: {files_before}")
        
        # Remove todos os arquivos atuais (exceto .myvcs)
        for item in os.listdir(self.work_dir):
            if item == ".myvcs":
                continue
            
            item_path = os.path.join(self.work_dir, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"Removido diretório: {item}")
                else:
                    os.remove(item_path)
                    print(f"Removido arquivo: {item}")
            except OSError as e:
                print(f"Erro ao remover {item}: {e}")
        
        # Reconstrói o estado do commit
        print("Iniciando reconstrução da árvore...")
        self._rebuild_from_tree(commit_obj.file_tree.root, self.work_dir)
        
        # Atualiza HEAD
        with open(self.head_file, "w") as f:
            f.write(commit_hash)
        
        print(f"Checkout para o commit {commit_hash[:10]} concluído.")
    
    def _rebuild_from_tree(self, node, current_path):
        """
        Reconstrói a estrutura de arquivos a partir de um nó da árvore.
        
        Args:
            node: Nó da árvore de arquivos
            current_path (str): Caminho atual no sistema de arquivos
        """
        for child_name, child_node in node.children.items():
            child_path = os.path.join(current_path, child_name)
            
            if child_node.is_file:
                # Restaura arquivo
                content_path = os.path.join(self.objects_dir, child_node.content_hash)
                if os.path.exists(content_path):
                    try:
                        shutil.copy(content_path, child_path)
                        print(f"Restaurado arquivo: {child_path}")
                    except IOError as e:
                        print(f"Erro ao restaurar arquivo {child_path}: {e}")
                else:
                    print(f"ERRO: Objeto não encontrado: {content_path}")
            else:
                # Cria diretório e processa recursivamente
                try:
                    os.makedirs(child_path, exist_ok=True)
                    print(f"Criado diretório: {child_path}")
                    self._rebuild_from_tree(child_node, child_path)
                except OSError as e:
                    print(f"Erro ao criar diretório {child_path}: {e}")
    
    def get_history(self):
        """
        Obtém o histórico de commits.
        
        Returns:
            list: Lista de tuplas (hash, commit_obj) em ordem cronológica reversa
        """
        if not self.is_repository():
            return []
        
        history = []
        current_hash = self.get_head_hash()
        
        while current_hash:
            commit_path = os.path.join(self.commits_dir, current_hash)
            if not os.path.exists(commit_path):
                break
            
            try:
                with open(commit_path, "rb") as f:
                    commit_obj = pickle.load(f)
                history.append((current_hash, commit_obj))
                current_hash = commit_obj.parent_commit_hash
            except (IOError, pickle.PickleError) as e:
                print(f"Erro ao carregar commit {current_hash}: {e}")
                break
        
        return history
    
    def get_commit(self, commit_hash):
        """
        Obtém um commit específico pelo hash.
        
        Args:
            commit_hash (str): Hash do commit
            
        Returns:
            Commit or None: Objeto commit ou None se não encontrado
        """
        commit_path = os.path.join(self.commits_dir, commit_hash)
        if not os.path.exists(commit_path):
            return None
        
        try:
            with open(commit_path, "rb") as f:
                return pickle.load(f)
        except (IOError, pickle.PickleError):
            return None
    
    def get_status(self):
        """
        Obtém informações sobre o estado atual do repositório.
        
        Returns:
            dict: Dicionário com informações de status
        """
        if not self.is_repository():
            return {'is_repository': False}
        
        head_hash = self.get_head_hash()
        head_commit = self.get_commit(head_hash) if head_hash else None
        history = self.get_history()
        
        return {
            'is_repository': True,
            'work_dir': self.work_dir,
            'head_hash': head_hash,
            'head_commit_message': head_commit.message if head_commit else None,
            'total_commits': len(history)
        }
