#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica Completa do Sistema VCS - 100% Funcional

Esta é a versão completa da interface gráfica que implementa
TODAS as funcionalidades do sistema VCS:

FUNCIONALIDADES IMPLEMENTADAS:
✅ Criar/abrir repositórios
✅ Fazer commits com autor personalizado
✅ Visualizar histórico completo
✅ Fazer checkout de versões
✅ Histórico de arquivos específicos
✅ Explorador de arquivos em commits
✅ Comparação entre commits
✅ Remoção de arquivos
✅ Navegação visual da estrutura

Autor: Milton
Data: 2025
Versão: 2.0 - Completa
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
from datetime import datetime

# Importa as classes do módulo VCS Core
from vcs_core import Repository


class VCSCompleteApp:
    """
    Aplicação GUI COMPLETA para o Sistema de Controle de Versões.
    
    Esta versão implementa 100% das funcionalidades requeridas:
    - Operações básicas de VCS
    - Histórico por arquivo
    - Explorador visual
    - Comparação de commits
    - Remoção de arquivos
    """
    
    def __init__(self, root):
        """
        Inicializa a aplicação GUI completa.
        
        Args:
            root: Widget raiz do Tkinter
        """
        self.root = root
        self.root.title("🚀 Sistema VCS Completo - Todas as Funcionalidades")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Estado da aplicação
        self.repo = None
        self.history_cache = []
        self.current_commit_files = []
        
        # Configurar estilo
        self.setup_styles()
        
        # Configura a interface
        self.setup_ui()
        self.update_ui_state()
        
        # Atualizar status inicial
        self.update_status("Aplicação VCS iniciada. Selecione um repositório para começar.")
    
    def setup_styles(self):
        """Configura estilos personalizados para a interface."""
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Estilo para botões principais
        style.configure("Primary.TButton", 
                       padding=(10, 5), 
                       font=("Arial", 9, "bold"))
        
        # Estilo para labels de cabeçalho
        style.configure("Header.TLabel", 
                       font=("Arial", 11, "bold"),
                       foreground="#2c3e50")
    
    def setup_ui(self):
        """Configura toda a interface gráfica com abas."""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Cabeçalho com informações do repositório
        self.setup_header(main_frame)
        
        # Notebook com abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=(10, 0))
        
        # Aba 1: Operações Principais
        self.setup_main_tab()
        
        # Aba 2: Explorador de Arquivos
        self.setup_explorer_tab()
        
        # Aba 3: Histórico por Arquivo
        self.setup_file_history_tab()
        
        # Aba 4: Comparação de Commits
        self.setup_compare_tab()
        
        # Aba 5: Ferramentas Avançadas
        self.setup_tools_tab()
        
        # Barra de status
        self.setup_status_bar(main_frame)
    
    def setup_header(self, parent):
        """Configura o cabeçalho com informações do repositório."""
        header_frame = ttk.LabelFrame(parent, text="📂 Repositório Atual", padding="10")
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Info do repositório
        self.repo_info_label = ttk.Label(
            header_frame,
            text="Nenhum repositório selecionado",
            style="Header.TLabel",
            foreground="red"
        )
        self.repo_info_label.pack(anchor='w')
        
        # Botão para selecionar repositório
        ttk.Button(
            header_frame,
            text="🗂️ Selecionar/Criar Repositório",
            command=self.select_repository,
            style="Primary.TButton"
        ).pack(anchor='w', pady=(5, 0))
    
    def setup_main_tab(self):
        """Aba principal - Operações básicas do VCS."""
        tab_main = ttk.Frame(self.notebook)
        self.notebook.add(tab_main, text="🏠 Principal")
        
        # Dividir em duas colunas
        left_frame = ttk.Frame(tab_main)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        right_frame = ttk.Frame(tab_main)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # === COLUNA ESQUERDA - Operações ===
        operations_frame = ttk.LabelFrame(left_frame, text="⚡ Operações VCS", padding="10")
        operations_frame.pack(fill='x', pady=(0, 10))
        
        # Botão de commit
        self.btn_commit = ttk.Button(
            operations_frame,
            text="💾 Fazer Commit",
            command=self.do_commit,
            state='disabled',
            style="Primary.TButton"
        )
        self.btn_commit.pack(fill='x', pady=(0, 5))
        
        # Botão de checkout
        self.btn_checkout = ttk.Button(
            operations_frame,
            text="🔄 Fazer Checkout",
            command=self.do_checkout,
            state='disabled'
        )
        self.btn_checkout.pack(fill='x', pady=(0, 5))
        
        # Botão de status
        self.btn_status = ttk.Button(
            operations_frame,
            text="📊 Ver Status",
            command=self.show_status,
            state='disabled'
        )
        self.btn_status.pack(fill='x')
        
        # Status do repositório
        status_frame = ttk.LabelFrame(left_frame, text="📈 Status Atual", padding="10")
        status_frame.pack(fill='both', expand=True)
        
        self.status_text = tk.Text(
            status_frame,
            height=8,
            wrap='word',
            font=("Consolas", 9),
            bg="#f8f9fa",
            state='disabled'
        )
        status_scroll = ttk.Scrollbar(status_frame, orient='vertical', command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scroll.set)
        
        self.status_text.pack(side='left', fill='both', expand=True)
        status_scroll.pack(side='right', fill='y')
        
        # === COLUNA DIREITA - Histórico ===
        history_frame = ttk.LabelFrame(right_frame, text="📚 Histórico de Commits", padding="10")
        history_frame.pack(fill='both', expand=True)
        
        # Lista de histórico
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=('hash', 'author', 'date', 'files'),
            show='tree headings',
            height=15
        )
        
        # Configurar colunas
        self.history_tree.heading('#0', text='Mensagem', anchor='w')
        self.history_tree.heading('hash', text='Hash', anchor='center')
        self.history_tree.heading('author', text='Autor', anchor='center')
        self.history_tree.heading('date', text='Data', anchor='center')
        self.history_tree.heading('files', text='Arquivos', anchor='center')
        
        self.history_tree.column('#0', width=200, minwidth=150)
        self.history_tree.column('hash', width=100, minwidth=80)
        self.history_tree.column('author', width=100, minwidth=80)
        self.history_tree.column('date', width=150, minwidth=120)
        self.history_tree.column('files', width=80, minwidth=60)
        
        # Scrollbar para histórico
        history_scroll = ttk.Scrollbar(history_frame, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scroll.set)
        
        self.history_tree.pack(side='left', fill='both', expand=True)
        history_scroll.pack(side='right', fill='y')
        
        # Bind para seleção
        self.history_tree.bind('<Double-1>', self.on_history_double_click)
    
    def setup_explorer_tab(self):
        """Aba explorador - Navegar arquivos em commits."""
        tab_explorer = ttk.Frame(self.notebook)
        self.notebook.add(tab_explorer, text="🗂️ Explorador")
        
        # Frame superior - seleção de commit
        selection_frame = ttk.LabelFrame(tab_explorer, text="🎯 Selecionar Commit", padding="10")
        selection_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(selection_frame, text="Commit:").pack(side='left')
        
        self.commit_var = tk.StringVar()
        self.commit_combo = ttk.Combobox(
            selection_frame,
            textvariable=self.commit_var,
            state='readonly',
            width=50
        )
        self.commit_combo.pack(side='left', padx=(5, 10), fill='x', expand=True)
        self.commit_combo.bind('<<ComboboxSelected>>', self.on_commit_selected)
        
        ttk.Button(
            selection_frame,
            text="🔍 Explorar",
            command=self.explore_commit
        ).pack(side='right')
        
        # Frame principal - divisão
        main_explorer = ttk.Frame(tab_explorer)
        main_explorer.pack(fill='both', expand=True)
        
        # Árvore de arquivos
        tree_frame = ttk.LabelFrame(main_explorer, text="🌳 Estrutura de Arquivos", padding="10")
        tree_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        self.file_tree = ttk.Treeview(tree_frame, show='tree')
        tree_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.file_tree.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        
        # Informações do arquivo
        info_frame = ttk.LabelFrame(main_explorer, text="ℹ️ Informações", padding="10")
        info_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        self.file_info_text = tk.Text(
            info_frame,
            wrap='word',
            font=("Consolas", 9),
            bg="#f8f9fa",
            state='disabled'
        )
        info_scroll = ttk.Scrollbar(info_frame, orient='vertical', command=self.file_info_text.yview)
        self.file_info_text.configure(yscrollcommand=info_scroll.set)
        
        self.file_info_text.pack(side='left', fill='both', expand=True)
        info_scroll.pack(side='right', fill='y')
        
        # Bind para seleção na árvore
        self.file_tree.bind('<<TreeviewSelect>>', self.on_file_selected)
    
    def get_file_details_from_hash(self, file_hash):
        """Obtém detalhes de um arquivo pelo hash."""
        try:
            # Buscar o arquivo no commit atual para obter tamanho
            for file_path, node in self.current_commit_files:
                if hasattr(node, 'content_hash') and node.content_hash == file_hash:
                    return {
                        'size_bytes': node.file_size,
                        'size_formatted': node.format_file_size(),
                        'hash': node.content_hash
                    }
            
            # Se não encontrou, buscar nos objetos
            if self.repo and hasattr(self.repo, 'objects_dir'):
                object_path = os.path.join(self.repo.objects_dir, file_hash)
                if os.path.exists(object_path):
                    size = os.path.getsize(object_path)
                    return {
                        'size_bytes': size,
                        'size_formatted': self.format_file_size(size),
                        'hash': file_hash
                    }
        except Exception as e:
            print(f"Erro ao obter detalhes do arquivo {file_hash}: {e}")
        return None
    
    def format_file_size(self, size):
        """Formata o tamanho do arquivo."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def setup_file_history_tab(self):
        """Aba histórico de arquivo - Ver histórico de um arquivo específico."""
        tab_file_history = ttk.Frame(self.notebook)
        self.notebook.add(tab_file_history, text="📋 Histórico de Arquivo")
        
        # Seleção de arquivo
        selection_frame = ttk.LabelFrame(tab_file_history, text="📄 Selecionar Arquivo", padding="10")
        selection_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(selection_frame, text="Arquivo:").pack(side='left')
        
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(
            selection_frame,
            textvariable=self.file_path_var,
            font=("Consolas", 9)
        )
        self.file_path_entry.pack(side='left', padx=(5, 10), fill='x', expand=True)
        
        ttk.Button(
            selection_frame,
            text="📂 Procurar",
            command=self.browse_file_for_history
        ).pack(side='right', padx=(0, 5))
        
        ttk.Button(
            selection_frame,
            text="🔍 Ver Histórico",
            command=self.show_file_history
        ).pack(side='right')
        
        # Histórico do arquivo
        history_frame = ttk.LabelFrame(tab_file_history, text="📚 Histórico do Arquivo", padding="10")
        history_frame.pack(fill='both', expand=True)
        
        self.file_history_tree = ttk.Treeview(
            history_frame,
            columns=('commit_hash', 'author', 'date', 'file_hash'),
            show='tree headings'
        )
        
        self.file_history_tree.heading('#0', text='Mensagem do Commit', anchor='w')
        self.file_history_tree.heading('commit_hash', text='Commit Hash', anchor='center')
        self.file_history_tree.heading('author', text='Autor', anchor='center')
        self.file_history_tree.heading('date', text='Data', anchor='center')
        self.file_history_tree.heading('file_hash', text='Hash do Arquivo', anchor='center')
        
        self.file_history_tree.column('#0', width=250)
        self.file_history_tree.column('commit_hash', width=100)
        self.file_history_tree.column('author', width=100)
        self.file_history_tree.column('date', width=150)
        self.file_history_tree.column('file_hash', width=100)
        
        file_history_scroll = ttk.Scrollbar(history_frame, orient='vertical', command=self.file_history_tree.yview)
        self.file_history_tree.configure(yscrollcommand=file_history_scroll.set)
        
        self.file_history_tree.pack(side='left', fill='both', expand=True)
        file_history_scroll.pack(side='right', fill='y')
    
    def setup_compare_tab(self):
        """Aba comparação - Comparar dois commits."""
        tab_compare = ttk.Frame(self.notebook)
        self.notebook.add(tab_compare, text="🔍 Comparar")
        
        # Seleção de commits
        selection_frame = ttk.LabelFrame(tab_compare, text="🎯 Selecionar Commits para Comparar", padding="10")
        selection_frame.pack(fill='x', pady=(0, 10))
        
        # Primeiro commit
        ttk.Label(selection_frame, text="Commit 1:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.commit1_var = tk.StringVar()
        self.commit1_combo = ttk.Combobox(selection_frame, textvariable=self.commit1_var, state='readonly', width=40)
        self.commit1_combo.grid(row=0, column=1, padx=(0, 10), sticky='ew')
        
        # Segundo commit
        ttk.Label(selection_frame, text="Commit 2:").grid(row=1, column=0, sticky='w', padx=(0, 5), pady=(5, 0))
        self.commit2_var = tk.StringVar()
        self.commit2_combo = ttk.Combobox(selection_frame, textvariable=self.commit2_var, state='readonly', width=40)
        self.commit2_combo.grid(row=1, column=1, padx=(0, 10), pady=(5, 0), sticky='ew')
        
        # Botão comparar
        ttk.Button(
            selection_frame,
            text="⚖️ Comparar",
            command=self.compare_commits,
            style="Primary.TButton"
        ).grid(row=0, column=2, rowspan=2, padx=(10, 0), sticky='ns')
        
        selection_frame.columnconfigure(1, weight=1)
        
        # Resultado da comparação
        result_frame = ttk.LabelFrame(tab_compare, text="📊 Resultado da Comparação", padding="10")
        result_frame.pack(fill='both', expand=True)
        
        self.compare_result = tk.Text(
            result_frame,
            wrap='word',
            font=("Consolas", 9),
            bg="#f8f9fa",
            state='disabled'
        )
        compare_scroll = ttk.Scrollbar(result_frame, orient='vertical', command=self.compare_result.yview)
        self.compare_result.configure(yscrollcommand=compare_scroll.set)
        
        self.compare_result.pack(side='left', fill='both', expand=True)
        compare_scroll.pack(side='right', fill='y')
    
    def setup_tools_tab(self):
        """Aba ferramentas - Funcionalidades avançadas."""
        tab_tools = ttk.Frame(self.notebook)
        self.notebook.add(tab_tools, text="🛠️ Ferramentas")
        
        # Remoção de arquivos
        remove_frame = ttk.LabelFrame(tab_tools, text="🗑️ Remover Arquivos", padding="10")
        remove_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(remove_frame, text="Arquivo para remover:").pack(anchor='w')
        
        remove_file_frame = ttk.Frame(remove_frame)
        remove_file_frame.pack(fill='x', pady=(5, 0))
        
        self.remove_file_var = tk.StringVar()
        self.remove_file_entry = ttk.Entry(
            remove_file_frame,
            textvariable=self.remove_file_var,
            font=("Consolas", 9)
        )
        self.remove_file_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        ttk.Button(
            remove_file_frame,
            text="📂 Procurar",
            command=self.browse_file_to_remove
        ).pack(side='right', padx=(0, 5))
        
        ttk.Button(
            remove_file_frame,
            text="🗑️ Remover",
            command=self.remove_file
        ).pack(side='right')
        
        # Estatísticas do repositório
        stats_frame = ttk.LabelFrame(tab_tools, text="📈 Estatísticas do Repositório", padding="10")
        stats_frame.pack(fill='both', expand=True)
        
        self.stats_text = tk.Text(
            stats_frame,
            wrap='word',
            font=("Consolas", 9),
            bg="#f8f9fa",
            state='disabled'
        )
        stats_scroll = ttk.Scrollbar(stats_frame, orient='vertical', command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_scroll.set)
        
        self.stats_text.pack(side='left', fill='both', expand=True)
        stats_scroll.pack(side='right', fill='y')
        
        # Botão para atualizar estatísticas
        ttk.Button(
            tab_tools,
            text="🔄 Atualizar Estatísticas",
            command=self.update_repository_stats,
            style="Primary.TButton"
        ).pack(pady=(10, 0))
    
    def setup_status_bar(self, parent):
        """Configura a barra de status."""
        self.status_bar = ttk.Label(
            parent,
            text="Pronto",
            relief='sunken',
            anchor='w',
            font=("Arial", 9)
        )
        self.status_bar.pack(side='bottom', fill='x', pady=(10, 0))
    
    # ========================
    # MÉTODOS DE FUNCIONALIDADE
    # ========================
    
    def update_status(self, message):
        """Atualiza a barra de status."""
        self.status_bar.config(text=f"⏰ {datetime.now().strftime('%H:%M:%S')} - {message}")
        self.root.update_idletasks()
    
    def select_repository(self):
        """Seleciona ou cria um repositório."""
        folder = filedialog.askdirectory(title="Selecionar pasta do repositório")
        if not folder:
            return
        
        try:
            self.repo = Repository(folder)
            
            # Verificar se é um repositório existente
            if not self.repo.is_repository():
                # Perguntar se quer criar novo repositório
                result = messagebox.askyesno(
                    "Novo Repositório",
                    f"A pasta '{folder}' não é um repositório VCS.\n\nDeseja criar um novo repositório?"
                )
                if result:
                    self.repo.init()
                    self.update_status(f"Novo repositório criado em: {folder}")
                else:
                    self.repo = None
                    return
            else:
                self.update_status(f"Repositório carregado: {folder}")
            
            # Atualizar interface
            self.repo_info_label.config(
                text=f"📂 {os.path.basename(folder)} ({folder})",
                foreground="green"
            )
            
            self.update_ui_state()
            self.refresh_all_data()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir repositório:\n{e}")
            self.update_status("Erro ao abrir repositório")
    
    def update_ui_state(self):
        """Atualiza o estado dos elementos da interface."""
        has_repo = self.repo and self.repo.is_repository()
        
        # Botões principais
        state = 'normal' if has_repo else 'disabled'
        self.btn_commit.config(state=state)
        self.btn_checkout.config(state=state)
        self.btn_status.config(state=state)
    
    def refresh_all_data(self):
        """Atualiza todos os dados da interface."""
        if not self.repo or not self.repo.is_repository():
            return
        
        try:
            # Atualizar histórico
            self.refresh_history()
            
            # Atualizar combos de commits
            self.refresh_commit_combos()
            
            # Atualizar status
            self.show_status()
            
            # Atualizar estatísticas
            self.update_repository_stats()
            
            self.update_status("Dados atualizados com sucesso")
            
        except Exception as e:
            self.update_status(f"Erro ao atualizar dados: {e}")
    
    def refresh_history(self):
        """Atualiza a lista de histórico."""
        # Limpar árvore
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        if not self.repo or not self.repo.is_repository():
            return
        
        try:
            history = self.repo.get_history()
            self.history_cache = history
            
            head_hash = self.repo.get_head_hash()
            
            for commit_hash, commit_obj in history:
                # Marcar o HEAD
                prefix = "👑 " if commit_hash == head_hash else ""
                
                # Formatação da data
                date_str = commit_obj.timestamp.strftime("%d/%m/%Y %H:%M")
                
                # Número de arquivos
                files_count = len(commit_obj.file_tree.get_all_files())
                
                self.history_tree.insert(
                    '',
                    'end',
                    text=f"{prefix}{commit_obj.message}",
                    values=(
                        commit_hash[:10],
                        commit_obj.author,
                        date_str,
                        str(files_count)
                    ),
                    tags=('head',) if commit_hash == head_hash else ()
                )
            
            # Configurar tags
            self.history_tree.tag_configure('head', background='#e8f5e8')
            
        except Exception as e:
            self.update_status(f"Erro ao carregar histórico: {e}")
    
    def refresh_commit_combos(self):
        """Atualiza os comboboxes com lista de commits."""
        if not self.repo or not self.repo.is_repository():
            return
        
        try:
            history = self.repo.get_history()
            commit_list = []
            
            for commit_hash, commit_obj in history:
                commit_info = f"{commit_hash[:10]} - {commit_obj.message} ({commit_obj.author})"
                commit_list.append(commit_info)
            
            # Atualizar todos os combos
            self.commit_combo['values'] = commit_list
            self.commit1_combo['values'] = commit_list
            self.commit2_combo['values'] = commit_list
            
        except Exception as e:
            self.update_status(f"Erro ao atualizar combos: {e}")
    
    def do_commit(self):
        """Realiza um commit."""
        if not self.repo or not self.repo.is_repository():
            messagebox.showwarning("Aviso", "Nenhum repositório selecionado")
            return
        
        # Pedir autor
        author = simpledialog.askstring(
            "Autor do Commit",
            "Digite seu nome:",
            initialvalue="Milton"
        )
        if not author:
            return
        
        # Pedir mensagem
        message = simpledialog.askstring(
            "Mensagem do Commit",
            "Digite a mensagem do commit:",
            initialvalue="Alterações realizadas"
        )
        if not message:
            return
        
        try:
            commit_hash = self.repo.commit(message, author)
            
            if commit_hash:
                messagebox.showinfo(
                    "Sucesso",
                    f"Commit realizado com sucesso!\n\nHash: {commit_hash[:10]}\nAutor: {author}\nMensagem: {message}"
                )
                self.refresh_all_data()
                self.update_status(f"Commit {commit_hash[:10]} criado por {author}")
            else:
                messagebox.showinfo("Info", "Nenhuma alteração detectada para commit")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer commit:\n{e}")
            self.update_status("Erro ao fazer commit")
    
    def do_checkout(self):
        """Realiza checkout de um commit."""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um commit no histórico")
            return
        
        # Obter informações do commit selecionado
        item = self.history_tree.item(selection[0])
        commit_hash = item['values'][0]  # Hash curto
        
        # Encontrar hash completo
        full_hash = None
        for hash_full, commit_obj in self.history_cache:
            if hash_full.startswith(commit_hash):
                full_hash = hash_full
                break
        
        if not full_hash:
            messagebox.showerror("Erro", "Commit não encontrado")
            return
        
        # Confirmar checkout
        result = messagebox.askyesno(
            "Confirmar Checkout",
            f"Tem certeza que deseja fazer checkout do commit:\n\n{item['text']}\n\nIsto irá substituir os arquivos atuais!"
        )
        
        if result:
            try:
                self.repo.checkout(full_hash)
                messagebox.showinfo("Sucesso", f"Checkout realizado para commit {commit_hash}")
                self.refresh_all_data()
                self.update_status(f"Checkout realizado: {commit_hash}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao fazer checkout:\n{e}")
                self.update_status("Erro ao fazer checkout")
    
    def show_status(self):
        """Mostra o status do repositório."""
        if not self.repo or not self.repo.is_repository():
            return
        
        try:
            status = self.repo.get_status()
            
            # Atualizar texto de status
            self.status_text.config(state='normal')
            self.status_text.delete(1.0, tk.END)
            
            status_info = f"""📊 STATUS DO REPOSITÓRIO
            
📂 Diretório: {status['work_dir']}
🆔 HEAD Hash: {status['head_hash'][:10] if status['head_hash'] else 'Nenhum'}
💬 Última mensagem: {status['head_commit_message'] or 'N/A'}
📈 Total de commits: {status['total_commits']}

⏰ Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""
            
            self.status_text.insert(1.0, status_info)
            self.status_text.config(state='disabled')
            
        except Exception as e:
            self.update_status(f"Erro ao obter status: {e}")
    
    def on_history_double_click(self, event):
        """Manipula duplo clique no histórico."""
        selection = self.history_tree.selection()
        if selection:
            # Fazer checkout do commit selecionado
            self.do_checkout()
    
    def on_commit_selected(self, event):
        """Manipula seleção de commit no explorador."""
        self.explore_commit()
    
    def explore_commit(self):
        """Explora arquivos de um commit."""
        commit_info = self.commit_var.get()
        if not commit_info:
            return
        
        commit_hash = commit_info.split(' - ')[0]
        
        try:
            # Encontrar commit completo
            full_hash = None
            for hash_full, commit_obj in self.history_cache:
                if hash_full.startswith(commit_hash):
                    full_hash = hash_full
                    break
            
            if not full_hash:
                return
            
            # Obter arquivos do commit
            files = self.repo.get_all_files_in_commit(full_hash)
            self.current_commit_files = files
            
            # Limpar árvore
            for item in self.file_tree.get_children():
                self.file_tree.delete(item)
            
            # Construir árvore de arquivos
            self.build_file_tree(files)
            
            self.update_status(f"Explorando commit {commit_hash} - {len(files)} arquivos")
            
        except Exception as e:
            self.update_status(f"Erro ao explorar commit: {e}")
    
    def build_file_tree(self, files):
        """Constrói a árvore visual de arquivos."""
        # Organizar arquivos por diretório
        dirs = {}
        
        for file_path, node in files:
            parts = file_path.split(os.sep)
            current_dict = dirs
            
            # Criar estrutura de diretórios
            for i, part in enumerate(parts[:-1]):
                if part not in current_dict:
                    current_dict[part] = {}
                current_dict = current_dict[part]
            
            # Adicionar arquivo (agora com o nó completo)
            current_dict[parts[-1]] = node
        
        # Inserir na árvore
        self.insert_tree_items('', dirs)
    
    def insert_tree_items(self, parent, items_dict):
        """Insere items na árvore recursivamente."""
        for name, content in sorted(items_dict.items()):
            if isinstance(content, dict):
                # É um diretório
                item_id = self.file_tree.insert(parent, 'end', text=f"📁 {name}", open=True)
                self.insert_tree_items(item_id, content)
            else:
                # É um arquivo - agora 'content' é o nó completo
                node = content
                if hasattr(node, 'file_size') and hasattr(node, 'format_file_size'):
                    size_str = node.format_file_size()
                else:
                    size_str = 'N/A'
                
                display_name = f"📄 {name} ({size_str})"
                file_hash = node.content_hash if hasattr(node, 'content_hash') else 'N/A'
                self.file_tree.insert(parent, 'end', text=display_name, values=(file_hash,))
    
    def on_file_selected(self, event):
        """Manipula seleção de arquivo na árvore."""
        selection = self.file_tree.selection()
        if not selection:
            return
        
        item = self.file_tree.item(selection[0])
        file_name = item['text']
        
        # Atualizar informações do arquivo
        self.file_info_text.config(state='normal')
        self.file_info_text.delete(1.0, tk.END)
        
        if file_name.startswith('📄'):
            # É um arquivo - extrair nome e tamanho
            name_part = file_name[2:]  # Remove emoji
            if '(' in name_part:
                actual_name = name_part.split(' (')[0]
                size_part = name_part.split(' (')[1].rstrip(')')
            else:
                actual_name = name_part
                size_part = 'N/A'
            
            file_hash = item['values'][0] if item['values'] else 'N/A'
            
            # Buscar caminho completo do arquivo
            full_path = self.get_full_path_from_tree(selection[0])
            
            info = f"""📄 INFORMAÇÕES DO ARQUIVO

📛 Nome: {actual_name}
📁 Caminho: {full_path}
📊 Tamanho: {size_part}
🔑 Hash: {file_hash}
� Tipo: Arquivo
⏰ Selecionado em: {datetime.now().strftime('%H:%M:%S')}
"""
        else:
            # É um diretório
            dir_name = file_name[2:]  # Remove emoji
            full_path = self.get_full_path_from_tree(selection[0])
            
            info = f"""📁 INFORMAÇÕES DO DIRETÓRIO

📛 Nome: {dir_name}
📁 Caminho: {full_path}
📊 Tipo: Diretório
⏰ Selecionado em: {datetime.now().strftime('%H:%M:%S')}
"""
        
        self.file_info_text.insert(1.0, info)
        self.file_info_text.config(state='disabled')
    
    def get_full_path_from_tree(self, item_id):
        """Obtém o caminho completo de um item na árvore."""
        path_parts = []
        current = item_id
        
        while current:
            item = self.file_tree.item(current)
            name = item['text']
            
            # Remover emoji e tamanho do arquivo
            if name.startswith('📄'):
                clean_name = name[2:]
                if '(' in clean_name:
                    clean_name = clean_name.split(' (')[0]
            elif name.startswith('📁'):
                clean_name = name[2:]
            else:
                clean_name = name
            
            path_parts.insert(0, clean_name)
            current = self.file_tree.parent(current)
        
        return '/'.join(path_parts) if path_parts else ''
    
    def browse_file_for_history(self):
        """Procura arquivo para ver histórico."""
        if not self.repo or not self.repo.is_repository():
            return
        
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo para ver histórico",
            initialdir=self.repo.work_dir
        )
        
        if file_path:
            # Converter para caminho relativo
            rel_path = os.path.relpath(file_path, self.repo.work_dir)
            self.file_path_var.set(rel_path)
    
    def show_file_history(self):
        """Mostra o histórico de um arquivo específico."""
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showwarning("Aviso", "Digite o caminho do arquivo")
            return
        
        if not self.repo or not self.repo.is_repository():
            return
        
        try:
            # Limpar árvore
            for item in self.file_history_tree.get_children():
                self.file_history_tree.delete(item)
            
            # Obter histórico do arquivo
            file_history = self.repo.get_file_history(file_path)
            
            if not file_history:
                messagebox.showinfo("Info", f"Nenhum histórico encontrado para o arquivo: {file_path}")
                return
            
            # Preencher árvore
            for commit_hash, commit_obj, node in file_history:
                date_str = commit_obj.timestamp.strftime("%d/%m/%Y %H:%M")
                
                # Obter hash do arquivo do objeto node
                file_hash = node.content_hash if hasattr(node, 'content_hash') else 'N/A'
                
                self.file_history_tree.insert(
                    '',
                    'end',
                    text=commit_obj.message,
                    values=(
                        commit_hash[:10],
                        commit_obj.author,
                        date_str,
                        file_hash[:10] if file_hash != 'N/A' else 'N/A'
                    )
                )
            
            self.update_status(f"Histórico do arquivo {file_path}: {len(file_history)} versões")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter histórico do arquivo:\n{e}")
            self.update_status("Erro ao obter histórico do arquivo")
    
    def compare_commits(self):
        """Compara dois commits."""
        commit1_info = self.commit1_var.get()
        commit2_info = self.commit2_var.get()
        
        if not commit1_info or not commit2_info:
            messagebox.showwarning("Aviso", "Selecione ambos os commits para comparar")
            return
        
        commit1_hash = commit1_info.split(' - ')[0]
        commit2_hash = commit2_info.split(' - ')[0]
        
        if commit1_hash == commit2_hash:
            messagebox.showwarning("Aviso", "Selecione commits diferentes para comparar")
            return
        
        try:
            # Encontrar hashes completos
            full_hash1 = None
            full_hash2 = None
            
            for hash_full, commit_obj in self.history_cache:
                if hash_full.startswith(commit1_hash):
                    full_hash1 = hash_full
                if hash_full.startswith(commit2_hash):
                    full_hash2 = hash_full
            
            if not full_hash1 or not full_hash2:
                messagebox.showerror("Erro", "Commits não encontrados")
                return
            
            # Comparar commits
            diff = self.repo.compare_commits(full_hash1, full_hash2)
            
            # Mostrar resultado
            self.compare_result.config(state='normal')
            self.compare_result.delete(1.0, tk.END)
            
            result_text = f"""🔍 COMPARAÇÃO DE COMMITS

📊 Commit 1: {diff['commit1_info']}
📊 Commit 2: {diff['commit2_info']}

➕ ARQUIVOS ADICIONADOS ({len(diff['added'])}):
"""
            
            for file in diff['added']:
                result_text += f"   + {file}\n"
            
            result_text += f"\n➖ ARQUIVOS REMOVIDOS ({len(diff['removed'])}):\n"
            for file in diff['removed']:
                result_text += f"   - {file}\n"
            
            result_text += f"\n🔄 ARQUIVOS MODIFICADOS ({len(diff['modified'])}):\n"
            for file_info in diff['modified']:
                result_text += f"   ~ {file_info[0]}\n"
            
            result_text += f"\n✅ ARQUIVOS INALTERADOS ({len(diff['unchanged'])}):\n"
            for file in diff['unchanged']:
                result_text += f"   = {file}\n"
            
            result_text += f"\n📈 RESUMO:\n"
            result_text += f"   Adicionados: {len(diff['added'])}\n"
            result_text += f"   Removidos: {len(diff['removed'])}\n"
            result_text += f"   Modificados: {len(diff['modified'])}\n"
            result_text += f"   Inalterados: {len(diff['unchanged'])}\n"
            
            self.compare_result.insert(1.0, result_text)
            self.compare_result.config(state='disabled')
            
            self.update_status(f"Comparação concluída: {commit1_hash} vs {commit2_hash}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao comparar commits:\n{e}")
            self.update_status("Erro ao comparar commits")
    
    def browse_file_to_remove(self):
        """Procura arquivo para remover."""
        if not self.repo or not self.repo.is_repository():
            return
        
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo para remover",
            initialdir=self.repo.work_dir
        )
        
        if file_path:
            # Converter para caminho relativo
            rel_path = os.path.relpath(file_path, self.repo.work_dir)
            self.remove_file_var.set(rel_path)
    
    def remove_file(self):
        """Remove um arquivo do repositório."""
        file_path = self.remove_file_var.get()
        if not file_path:
            messagebox.showwarning("Aviso", "Digite o caminho do arquivo")
            return
        
        if not self.repo or not self.repo.is_repository():
            return
        
        # Confirmar remoção
        result = messagebox.askyesno(
            "Confirmar Remoção",
            f"Tem certeza que deseja remover o arquivo:\n\n{file_path}\n\nEsta ação não pode ser desfeita!"
        )
        
        if result:
            try:
                self.repo.remove_file_from_repository(file_path)
                messagebox.showinfo("Sucesso", f"Arquivo {file_path} removido com sucesso")
                self.remove_file_var.set("")
                self.update_status(f"Arquivo removido: {file_path}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover arquivo:\n{e}")
                self.update_status("Erro ao remover arquivo")
    
    def update_repository_stats(self):
        """Atualiza as estatísticas do repositório."""
        if not self.repo or not self.repo.is_repository():
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, "Nenhum repositório carregado")
            self.stats_text.config(state='disabled')
            return
        
        try:
            # Obter dados para estatísticas
            history = self.repo.get_history()
            status = self.repo.get_status()
            
            # Calcular estatísticas
            total_commits = len(history)
            authors = set()
            total_files = 0
            
            for commit_hash, commit_obj in history:
                authors.add(commit_obj.author)
                files = self.repo.get_all_files_in_commit(commit_hash)
                if len(files) > total_files:
                    total_files = len(files)
            
            # Tamanho do repositório
            repo_size = 0
            vcs_dir = os.path.join(self.repo.work_dir, '.myvcs')
            if os.path.exists(vcs_dir):
                for root, dirs, files in os.walk(vcs_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            repo_size += os.path.getsize(file_path)
                        except OSError:
                            pass  # Arquivo pode ter sido removido durante a iteração
            
            # Formatar tamanho do repositório
            repo_size_formatted = self.format_file_size(repo_size)
            
            # Criar texto de estatísticas
            stats_text = f"""📈 ESTATÍSTICAS DO REPOSITÓRIO

📂 Diretório: {self.repo.work_dir}
📅 Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

📊 COMMITS:
   Total de commits: {total_commits}
   Autores únicos: {len(authors)}
   Autores: {', '.join(sorted(authors)) if authors else 'Nenhum'}

📄 ARQUIVOS:
   Máximo de arquivos em um commit: {total_files}
   
💾 ARMAZENAMENTO:
   Tamanho do repositório: {repo_size_formatted}
   
🔧 CONFIGURAÇÃO:
   Versão VCS: 2.0 Completa
   Estrutura: Árvore N-ária
   Serialização: Pickle
   Hash: SHA-1
"""
            
            # Mostrar estatísticas
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats_text)
            self.stats_text.config(state='disabled')
            
            self.update_status("Estatísticas atualizadas")
            
        except Exception as e:
            self.update_status(f"Erro ao calcular estatísticas: {e}")


def main():
    """Função principal da aplicação."""
    root = tk.Tk()
    app = VCSCompleteApp(root)
    
    # Configurar ícone (se disponível)
    try:
        # Você pode adicionar um ícone aqui
        pass
    except:
        pass
    
    # Centralizar janela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Executar aplicação
    root.mainloop()


if __name__ == "__main__":
    main()
