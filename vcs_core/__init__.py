#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VCS Core Module - Sistema de Controle de Versões

Este módulo implementa um sistema de controle de versões usando árvores N-árias.
Desenvolvido como projeto acadêmico para demonstrar estruturas de dados avançadas.

Autor: Milton
Data: 2025
"""

# Importações das classes principais
from .node import Node
from .file_tree import FileTree
from .commit import Commit
from .repository import Repository

# Exportações públicas do módulo
__all__ = ['Node', 'FileTree', 'Commit', 'Repository']

# Informações do módulo
__version__ = '1.0.0'
__author__ = 'Milton'
__description__ = 'Sistema de Controle de Versões com Árvores N-árias'
