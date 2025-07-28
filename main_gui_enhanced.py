#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica APRIMORADA do Sistema VCS
Todas as funcionalidades solicitadas implementadas visualmente

FUNCIONALIDADES GARANTIDAS:
✅ Organização hierárquica - Árvore visual completa
✅ Nome dos arquivos - Exibido em todas as listas
✅ Caminho (estrutura) - Exibido com caminho completo
✅ Tamanho dos arquivos - Exibido em bytes e formatado
✅ Histórico por arquivo - Interface dedicada
✅ Criar versões - Commits funcionais
✅ Recuperar determinada versão - Checkout completo
✅ Remover apenas determinado arquivo - Funcional
✅ Navegar pela estrutura hierárquica - Árvore interativa
✅ Visualizar estatísticas - Dashboard completo

Autor: Milton
Data: 2025
Versão: 3.0 - Aprimorada
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
from datetime import datetime

# Importa as classes do módulo VCS Core
from vcs_core import Repository


class VCSEnhancedApp:
    """
    Interface VCS APRIMORADA - Todas as funcionalidades solicitadas.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Sistema VCS - TODAS as Funcionalidades Implementadas")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Estado da aplicação
        self.repo = None
        self.history_cache = []
        self.current_commit_files = []
        
        # Configurar interface
        self.setup_ui()
        self.update_ui_state()
        self.update_status("✅ Interface VCS carregada - Todas as funcionalidades disponíveis")
    
    def setup_ui(self):
        """Configura a interface com TODAS as funcionalidades."""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Cabeçalho
        self.setup_header(main_frame)
        
        # Notebook com abas especializadas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=(10, 0))
        
        # 1. Aba Principal - Operações básicas
        self.setup_main_tab()
        
        # 2. Aba Navegação - Estrutura hierárquica com tamanhos
        self.setup_navigation_tab()
        
        # 3. Aba Histórico por Arquivo - Funcionalidade específica
        self.setup_file_history_tab()
        
        # 4. Aba Remoção - Remover arquivos específicos
        self.setup_removal_tab()
        
        # 5. Aba Estatísticas - Dashboard completo
        self.setup_stats_tab()
        
        # Barra de status
        self.setup_status_bar(main_frame)
    
    def setup_header(self, parent):
        """Cabeçalho com informações do repositório."""
        header_frame = ttk.LabelFrame(parent, text="📂 Repositório Atual", padding="10")
        header_frame.pack(fill='x', pady=(0, 10))
        
        self.repo_info_label = ttk.Label(
            header_frame,
            text="❌ Nenhum repositório selecionado",
            font=("Arial", 11, "bold"),
            foreground="red"
        )
        self.repo_info_label.pack(anchor='w')
        
        ttk.Button(
            header_frame,
            text="🗂️ Selecionar/Criar Repositório",
            command=self.select_repository
        ).pack(anchor='w', pady=(5, 0))
    
    def setup_main_tab(self):
        """Aba principal - Operações VCS básicas."""
        tab_main = ttk.Frame(self.notebook)
        self.notebook.add(tab_main, text="🏠 Principal")
        
        # Dividir em colunas
        left_frame = ttk.Frame(tab_main)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        right_frame = ttk.Frame(tab_main)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # === OPERAÇÕES ===
        ops_frame = ttk.LabelFrame(left_frame, text="⚡ Operações VCS", padding="10")
        ops_frame.pack(fill='x', pady=(0, 10))
        
        self.btn_commit = ttk.Button(ops_frame, text="💾 Criar Nova Versão (Commit)", command=self.do_commit, state='disabled')
        self.btn_commit.pack(fill='x', pady=(0, 5))
        
        self.btn_checkout = ttk.Button(ops_frame, text="🔄 Recuperar Versão Anterior (Checkout)", command=self.do_checkout, state='disabled')
        self.btn_checkout.pack(fill='x', pady=(0, 5))
        
        ttk.Button(ops_frame, text="📊 Ver Status do Repositório", command=self.show_status, state='disabled').pack(fill='x')
        
        # === STATUS ===
        status_frame = ttk.LabelFrame(left_frame, text="📈 Status e Informações", padding="10")
        status_frame.pack(fill='both', expand=True)
        
        self.status_text = tk.Text(status_frame, height=10, wrap='word', font=("Consolas", 9), bg="#f8f9fa", state='disabled')
        status_scroll = ttk.Scrollbar(status_frame, orient='vertical', command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scroll.set)
        
        self.status_text.pack(side='left', fill='both', expand=True)
        status_scroll.pack(side='right', fill='y')
        
        # === HISTÓRICO COM DETALHES ===
        history_frame = ttk.LabelFrame(right_frame, text="📚 Histórico de Versões", padding="10")
        history_frame.pack(fill='both', expand=True)
        
        # TreeView com colunas detalhadas
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=('hash', 'author', 'date', 'files', 'size'),
            show='tree headings'
        )
        
        self.history_tree.heading('#0', text='Mensagem', anchor='w')
        self.history_tree.heading('hash', text='Hash', anchor='center')
        self.history_tree.heading('author', text='Autor', anchor='center')
        self.history_tree.heading('date', text='Data/Hora', anchor='center')
        self.history_tree.heading('files', text='Arquivos', anchor='center')
        self.history_tree.heading('size', text='Tamanho Total', anchor='center')
        
        self.history_tree.column('#0', width=200)
        self.history_tree.column('hash', width=80)
        self.history_tree.column('author', width=100)
        self.history_tree.column('date', width=130)
        self.history_tree.column('files', width=70)
        self.history_tree.column('size', width=100)
        
        history_scroll = ttk.Scrollbar(history_frame, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scroll.set)
        
        self.history_tree.pack(side='left', fill='both', expand=True)
        history_scroll.pack(side='right', fill='y')
        
        self.history_tree.bind('<Double-1>', self.on_history_double_click)
    
    def setup_navigation_tab(self):
        """Aba navegação - Estrutura hierárquica com tamanhos de arquivos."""
        tab_nav = ttk.Frame(self.notebook)
        self.notebook.add(tab_nav, text="🗂️ Navegar Estrutura")
        
        # Seleção de versão
        select_frame = ttk.LabelFrame(tab_nav, text="📍 Selecionar Versão para Navegar", padding="10")
        select_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(select_frame, text="Versão (Commit):").pack(side='left')
        self.nav_commit_var = tk.StringVar()
        self.nav_commit_combo = ttk.Combobox(select_frame, textvariable=self.nav_commit_var, state='readonly', width=60)
        self.nav_commit_combo.pack(side='left', padx=(5, 10), fill='x', expand=True)
        self.nav_commit_combo.bind('<<ComboboxSelected>>', self.on_nav_commit_selected)
        
        ttk.Button(select_frame, text="🔍 Explorar Estrutura", command=self.explore_structure).pack(side='right')
        
        # Dividir visualização
        nav_content = ttk.Frame(tab_nav)
        nav_content.pack(fill='both', expand=True)
        
        # === ÁRVORE HIERÁRQUICA ===
        tree_frame = ttk.LabelFrame(nav_content, text="🌳 Organização Hierárquica", padding="10")
        tree_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        self.nav_tree = ttk.Treeview(tree_frame, columns=('type', 'size', 'hash'), show='tree headings')
        
        self.nav_tree.heading('#0', text='Nome (Caminho)', anchor='w')
        self.nav_tree.heading('type', text='Tipo', anchor='center')
        self.nav_tree.heading('size', text='Tamanho', anchor='center')
        self.nav_tree.heading('hash', text='Hash', anchor='center')
        
        self.nav_tree.column('#0', width=300)
        self.nav_tree.column('type', width=70)
        self.nav_tree.column('size', width=80)
        self.nav_tree.column('hash', width=100)
        
        nav_tree_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.nav_tree.yview)
        self.nav_tree.configure(yscrollcommand=nav_tree_scroll.set)
        
        self.nav_tree.pack(side='left', fill='both', expand=True)
        nav_tree_scroll.pack(side='right', fill='y')
        
        # === DETALHES DO ITEM ===
        detail_frame = ttk.LabelFrame(nav_content, text="ℹ️ Detalhes do Item Selecionado", padding="10")
        detail_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        self.detail_text = tk.Text(detail_frame, wrap='word', font=("Consolas", 9), bg="#f8f9fa", state='disabled')
        detail_scroll = ttk.Scrollbar(detail_frame, orient='vertical', command=self.detail_text.yview)
        self.detail_text.configure(yscrollcommand=detail_scroll.set)
        
        self.detail_text.pack(side='left', fill='both', expand=True)
        detail_scroll.pack(side='right', fill='y')
        
        self.nav_tree.bind('<<TreeviewSelect>>', self.on_nav_item_selected)
    
    def setup_file_history_tab(self):
        """Aba histórico por arquivo específico."""
        tab_file = ttk.Frame(self.notebook)
        self.notebook.add(tab_file, text="📋 Histórico por Arquivo")
        
        # Seleção de arquivo
        file_select_frame = ttk.LabelFrame(tab_file, text="📄 Selecionar Arquivo para Ver Histórico", padding="10")
        file_select_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(file_select_frame, text="Caminho do arquivo:").pack(anchor='w')
        
        entry_frame = ttk.Frame(file_select_frame)
        entry_frame.pack(fill='x', pady=(5, 0))
        
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(entry_frame, textvariable=self.file_path_var, font=("Consolas", 9))
        self.file_path_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        ttk.Button(entry_frame, text="📂 Procurar", command=self.browse_file_for_history).pack(side='right', padx=(0, 5))
        ttk.Button(entry_frame, text="🔍 Ver Histórico", command=self.show_file_history).pack(side='right')
        
        # Resultado do histórico
        history_result_frame = ttk.LabelFrame(tab_file, text="📚 Histórico de Versões do Arquivo", padding="10")
        history_result_frame.pack(fill='both', expand=True)
        
        self.file_history_tree = ttk.Treeview(
            history_result_frame,
            columns=('commit_hash', 'author', 'date', 'file_size', 'file_hash'),
            show='tree headings'
        )
        
        self.file_history_tree.heading('#0', text='Mensagem do Commit', anchor='w')
        self.file_history_tree.heading('commit_hash', text='Commit', anchor='center')
        self.file_history_tree.heading('author', text='Autor', anchor='center')
        self.file_history_tree.heading('date', text='Data', anchor='center')
        self.file_history_tree.heading('file_size', text='Tamanho', anchor='center')
        self.file_history_tree.heading('file_hash', text='Hash do Arquivo', anchor='center')
        
        self.file_history_tree.column('#0', width=250)
        self.file_history_tree.column('commit_hash', width=80)
        self.file_history_tree.column('author', width=100)
        self.file_history_tree.column('date', width=130)
        self.file_history_tree.column('file_size', width=80)
        self.file_history_tree.column('file_hash', width=100)
        
        file_hist_scroll = ttk.Scrollbar(history_result_frame, orient='vertical', command=self.file_history_tree.yview)
        self.file_history_tree.configure(yscrollcommand=file_hist_scroll.set)
        
        self.file_history_tree.pack(side='left', fill='both', expand=True)
        file_hist_scroll.pack(side='right', fill='y')
    
    def setup_removal_tab(self):
        """Aba para remoção de arquivos específicos."""
        tab_remove = ttk.Frame(self.notebook)
        self.notebook.add(tab_remove, text="🗑️ Remover Arquivo")
        
        # Informações sobre remoção
        info_frame = ttk.LabelFrame(tab_remove, text="ℹ️ Informações sobre Remoção", padding="10")
        info_frame.pack(fill='x', pady=(0, 10))
        
        info_text = """⚠️ COMO FUNCIONA A REMOÇÃO:

1. Selecione o arquivo que deseja remover
2. Confirme a remoção (arquivo será deletado do disco)
3. Faça um commit para registrar a remoção no histórico
4. A remoção será permanente após o commit
"""
        ttk.Label(info_frame, text=info_text, font=("Arial", 9), foreground="#666").pack(anchor='w')
        
        # Seleção de arquivo para remover
        remove_frame = ttk.LabelFrame(tab_remove, text="🎯 Selecionar Arquivo para Remover", padding="10")
        remove_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(remove_frame, text="Arquivo para remover:").pack(anchor='w')
        
        remove_entry_frame = ttk.Frame(remove_frame)
        remove_entry_frame.pack(fill='x', pady=(5, 10))
        
        self.remove_file_var = tk.StringVar()
        self.remove_entry = ttk.Entry(remove_entry_frame, textvariable=self.remove_file_var, font=("Consolas", 9))
        self.remove_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        ttk.Button(remove_entry_frame, text="📂 Procurar", command=self.browse_file_to_remove).pack(side='right', padx=(0, 10))
        ttk.Button(remove_entry_frame, text="🗑️ REMOVER", command=self.remove_file).pack(side='right')
        
        # Lista de arquivos no repositório
        list_frame = ttk.LabelFrame(tab_remove, text="📋 Arquivos no Repositório Atual", padding="10")
        list_frame.pack(fill='both', expand=True)
        
        self.files_tree = ttk.Treeview(list_frame, columns=('path', 'size'), show='tree headings')
        
        self.files_tree.heading('#0', text='Nome', anchor='w')
        self.files_tree.heading('path', text='Caminho Completo', anchor='w')
        self.files_tree.heading('size', text='Tamanho', anchor='center')
        
        self.files_tree.column('#0', width=200)
        self.files_tree.column('path', width=400)
        self.files_tree.column('size', width=100)
        
        files_scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.files_tree.yview)
        self.files_tree.configure(yscrollcommand=files_scroll.set)
        
        self.files_tree.pack(side='left', fill='both', expand=True)
        files_scroll.pack(side='right', fill='y')
        
        self.files_tree.bind('<Double-1>', self.on_file_double_click)
    
    def setup_stats_tab(self):
        """Aba de estatísticas completas."""
        tab_stats = ttk.Frame(self.notebook)
        self.notebook.add(tab_stats, text="📊 Estatísticas")
        
        # Botão para atualizar
        ttk.Button(tab_stats, text="🔄 Atualizar Estatísticas", command=self.update_repository_stats).pack(pady=(0, 10))
        
        # Área de estatísticas
        stats_frame = ttk.LabelFrame(tab_stats, text="📈 Dashboard do Repositório", padding="10")
        stats_frame.pack(fill='both', expand=True)
        
        self.stats_text = tk.Text(stats_frame, wrap='word', font=("Consolas", 10), bg="#f8f9fa", state='disabled')
        stats_scroll = ttk.Scrollbar(stats_frame, orient='vertical', command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_scroll.set)
        
        self.stats_text.pack(side='left', fill='both', expand=True)
        stats_scroll.pack(side='right', fill='y')
    
    def setup_status_bar(self, parent):
        """Barra de status."""
        self.status_bar = ttk.Label(parent, text="Pronto", relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x', pady=(10, 0))
    
    # ========================
    # MÉTODOS FUNCIONAIS
    # ========================
    
    def update_status(self, message):
        """Atualiza barra de status."""
        self.status_bar.config(text=f"⏰ {datetime.now().strftime('%H:%M:%S')} - {message}")
        self.root.update_idletasks()
    
    def select_repository(self):
        """Seleciona ou cria repositório."""
        folder = filedialog.askdirectory(title="Selecionar pasta do repositório")
        if not folder:
            return
        
        try:
            self.repo = Repository(folder)
            
            if not self.repo.is_repository():
                result = messagebox.askyesno(
                    "Novo Repositório",
                    f"A pasta '{folder}' não é um repositório VCS.\n\nDeseja criar um novo repositório?"
                )
                if result:
                    self.repo.init()
                    self.update_status(f"✅ Novo repositório criado em: {folder}")
                else:
                    self.repo = None
                    return
            else:
                self.update_status(f"✅ Repositório carregado: {folder}")
            
            # Atualizar interface
            self.repo_info_label.config(
                text=f"✅ {os.path.basename(folder)} ({folder})",
                foreground="green"
            )
            
            self.update_ui_state()
            self.refresh_all_data()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir repositório:\n{e}")
            self.update_status("❌ Erro ao abrir repositório")
    
    def update_ui_state(self):
        """Atualiza estado dos elementos."""
        has_repo = self.repo and self.repo.is_repository()
        state = 'normal' if has_repo else 'disabled'
        
        self.btn_commit.config(state=state)
        self.btn_checkout.config(state=state)
    
    def refresh_all_data(self):
        """Atualiza todos os dados."""
        if not self.repo or not self.repo.is_repository():
            return
        
        try:
            self.refresh_history()
            self.refresh_combos()
            self.refresh_files_list()
            self.show_status()
            self.update_repository_stats()
            self.update_status("✅ Dados atualizados")
        except Exception as e:
            self.update_status(f"❌ Erro ao atualizar: {e}")
    
    def refresh_history(self):
        """Atualiza histórico com tamanhos."""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        if not self.repo:
            return
        
        try:
            history = self.repo.get_history()
            self.history_cache = history
            head_hash = self.repo.get_head_hash()
            
            for commit_hash, commit_obj in history:
                prefix = "👑 " if commit_hash == head_hash else ""
                date_str = commit_obj.timestamp.strftime("%d/%m/%Y %H:%M")
                
                files = commit_obj.file_tree.get_all_files()
                total_size = sum(getattr(node, 'file_size', 0) for _, node in files)
                size_str = self.format_file_size(total_size)
                
                self.history_tree.insert(
                    '',
                    'end',
                    text=f"{prefix}{commit_obj.message}",
                    values=(
                        commit_hash[:10],
                        commit_obj.author,
                        date_str,
                        str(len(files)),
                        size_str
                    ),
                    tags=('head',) if commit_hash == head_hash else ()
                )
            
            self.history_tree.tag_configure('head', background='#e8f5e8')
            
        except Exception as e:
            self.update_status(f"❌ Erro no histórico: {e}")
    
    def refresh_combos(self):
        """Atualiza comboboxes."""
        if not self.repo:
            return
        
        try:
            history = self.repo.get_history()
            commit_list = []
            
            for commit_hash, commit_obj in history:
                commit_info = f"{commit_hash[:10]} - {commit_obj.message} ({commit_obj.author})"
                commit_list.append(commit_info)
            
            self.nav_commit_combo['values'] = commit_list
            
        except Exception as e:
            self.update_status(f"❌ Erro nos combos: {e}")
    
    def refresh_files_list(self):
        """Atualiza lista de arquivos atuais."""
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
        
        if not self.repo:
            return
        
        try:
            # Listar arquivos no diretório atual
            for root, dirs, files in os.walk(self.repo.work_dir):
                if '.myvcs' in root:
                    continue
                
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    rel_path = os.path.relpath(file_path, self.repo.work_dir)
                    size = os.path.getsize(file_path)
                    size_str = self.format_file_size(size)
                    
                    self.files_tree.insert(
                        '',
                        'end',
                        text=file_name,
                        values=(rel_path, size_str)
                    )
                    
        except Exception as e:
            self.update_status(f"❌ Erro na lista: {e}")
    
    def format_file_size(self, size):
        """Formata tamanho do arquivo."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    # === MÉTODOS DE AÇÃO ===
    
    def do_commit(self):
        """Cria nova versão (commit)."""
        if not self.repo:
            messagebox.showwarning("Aviso", "Nenhum repositório selecionado")
            return
        
        author = simpledialog.askstring("Autor", "Digite seu nome:", initialvalue="Milton")
        if not author:
            return
        
        message = simpledialog.askstring("Mensagem", "Descreva as alterações:")
        if not message:
            return
        
        try:
            commit_hash = self.repo.commit(message, author)
            if commit_hash:
                messagebox.showinfo("Sucesso", f"✅ Nova versão criada!\n\nHash: {commit_hash[:10]}\nAutor: {author}")
                self.refresh_all_data()
                self.update_status(f"✅ Commit {commit_hash[:10]} criado")
            else:
                messagebox.showinfo("Info", "ℹ️ Nenhuma alteração para commit")
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro ao criar commit:\n{e}")
    
    def do_checkout(self):
        """Recupera versão anterior."""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um commit no histórico")
            return
        
        item = self.history_tree.item(selection[0])
        commit_hash = item['values'][0]
        
        # Encontrar hash completo
        full_hash = None
        for hash_full, commit_obj in self.history_cache:
            if hash_full.startswith(commit_hash):
                full_hash = hash_full
                break
        
        if not full_hash:
            messagebox.showerror("Erro", "Commit não encontrado")
            return
        
        result = messagebox.askyesno(
            "Confirmar Checkout",
            f"🔄 Recuperar versão:\n\n{item['text']}\n\n⚠️ Isto substituirá os arquivos atuais!"
        )
        
        if result:
            try:
                self.repo.checkout(full_hash)
                messagebox.showinfo("Sucesso", f"✅ Versão {commit_hash} recuperada")
                self.refresh_all_data()
                self.update_status(f"✅ Checkout: {commit_hash}")
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro no checkout:\n{e}")
    
    def show_status(self):
        """Mostra status do repositório."""
        if not self.repo:
            return
        
        try:
            status = self.repo.get_status()
            
            self.status_text.config(state='normal')
            self.status_text.delete(1.0, tk.END)
            
            status_info = f"""📊 STATUS DO REPOSITÓRIO VCS

📂 Diretório: {status['work_dir']}
🆔 HEAD (Versão Atual): {status['head_hash'][:10] if status['head_hash'] else 'Nenhum'}
💬 Última Mensagem: {status['head_commit_message'] or 'N/A'}
📈 Total de Versões: {status['total_commits']}

✅ Repositório Válido: Sim
⏰ Última Atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

💡 DICA: Use as abas para explorar todas as funcionalidades!
"""
            
            self.status_text.insert(1.0, status_info)
            self.status_text.config(state='disabled')
            
        except Exception as e:
            self.update_status(f"❌ Erro no status: {e}")
    
    def on_history_double_click(self, event):
        """Duplo clique no histórico faz checkout."""
        self.do_checkout()
    
    def on_nav_commit_selected(self, event):
        """Seleção de commit na navegação."""
        self.explore_structure()
    
    def explore_structure(self):
        """Explora estrutura hierárquica."""
        commit_info = self.nav_commit_var.get()
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
            
            # Limpar árvore
            for item in self.nav_tree.get_children():
                self.nav_tree.delete(item)
            
            # Obter arquivos
            files = self.repo.get_all_files_in_commit(full_hash)
            self.current_commit_files = files
            
            # Construir árvore hierárquica
            self.build_navigation_tree(files)
            
            self.update_status(f"✅ Estrutura de {commit_hash}: {len(files)} arquivos")
            
        except Exception as e:
            self.update_status(f"❌ Erro na exploração: {e}")
    
    def build_navigation_tree(self, files):
        """Constrói árvore de navegação com tamanhos."""
        # Organizar por hierarquia
        tree_structure = {}
        
        for file_path, file_hash in files:
            parts = file_path.split(os.sep)
            current = tree_structure
            
            # Criar estrutura de diretórios
            for i, part in enumerate(parts[:-1]):
                if part not in current:
                    current[part] = {'type': 'dir', 'children': {}}
                current = current[part]['children']
            
            # Adicionar arquivo
            filename = parts[-1]
            
            # Buscar informações do arquivo
            file_info = self.get_file_info_from_files(file_path, file_hash)
            
            current[filename] = {
                'type': 'file',
                'hash': file_hash,
                'size': file_info['size'] if file_info else 0,
                'size_str': file_info['size_str'] if file_info else 'N/A'
            }
        
        # Inserir na árvore
        self.insert_nav_items('', tree_structure, '')
    
    def get_file_info_from_files(self, file_path, file_hash):
        """Busca informações de arquivo nos dados atuais."""
        for path, node in self.current_commit_files:
            if path == file_path and hasattr(node, 'content_hash') and node.content_hash == file_hash:
                return {
                    'size': getattr(node, 'file_size', 0),
                    'size_str': getattr(node, 'format_file_size', lambda: 'N/A')()
                }
        return None
    
    def insert_nav_items(self, parent, items_dict, path_prefix):
        """Insere items na árvore de navegação."""
        for name, content in sorted(items_dict.items()):
            current_path = f"{path_prefix}/{name}" if path_prefix else name
            
            if content['type'] == 'dir':
                # Diretório
                item_id = self.nav_tree.insert(
                    parent, 'end',
                    text=f"📁 {name}",
                    values=('Diretório', '-', '-'),
                    open=True
                )
                self.insert_nav_items(item_id, content['children'], current_path)
            else:
                # Arquivo
                self.nav_tree.insert(
                    parent, 'end',
                    text=f"📄 {name}",
                    values=('Arquivo', content['size_str'], content['hash'][:10])
                )
    
    def on_nav_item_selected(self, event):
        """Seleção de item na navegação."""
        selection = self.nav_tree.selection()
        if not selection:
            return
        
        item = self.nav_tree.item(selection[0])
        name = item['text']
        values = item['values']
        
        # Obter caminho completo
        path = self.get_nav_path(selection[0])
        
        self.detail_text.config(state='normal')
        self.detail_text.delete(1.0, tk.END)
        
        if values[0] == 'Arquivo':
            detail_info = f"""📄 DETALHES DO ARQUIVO

📛 Nome: {name[2:]}
📁 Caminho Completo: {path}
📊 Tamanho: {values[1]}
🔑 Hash: {values[2]}
📂 Tipo: Arquivo

⏰ Visualizado em: {datetime.now().strftime('%H:%M:%S')}
"""
        else:
            detail_info = f"""📁 DETALHES DO DIRETÓRIO

📛 Nome: {name[2:]}
📁 Caminho Completo: {path}
📂 Tipo: Diretório

⏰ Visualizado em: {datetime.now().strftime('%H:%M:%S')}
"""
        
        self.detail_text.insert(1.0, detail_info)
        self.detail_text.config(state='disabled')
    
    def get_nav_path(self, item_id):
        """Obtém caminho completo na navegação."""
        path_parts = []
        current = item_id
        
        while current:
            item = self.nav_tree.item(current)
            name = item['text']
            
            if name.startswith('📄') or name.startswith('📁'):
                clean_name = name[2:]
            else:
                clean_name = name
            
            path_parts.insert(0, clean_name)
            current = self.nav_tree.parent(current)
        
        return '/'.join(path_parts)
    
    def browse_file_for_history(self):
        """Procura arquivo para histórico."""
        if not self.repo:
            return
        
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo para ver histórico",
            initialdir=self.repo.work_dir
        )
        
        if file_path:
            rel_path = os.path.relpath(file_path, self.repo.work_dir)
            self.file_path_var.set(rel_path)
    
    def show_file_history(self):
        """Mostra histórico do arquivo."""
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showwarning("Aviso", "Digite o caminho do arquivo")
            return
        
        if not self.repo:
            return
        
        try:
            # Limpar árvore
            for item in self.file_history_tree.get_children():
                self.file_history_tree.delete(item)
            
            # Obter histórico
            file_history = self.repo.get_file_history(file_path)
            
            if not file_history:
                messagebox.showinfo("Info", f"❌ Nenhum histórico encontrado para: {file_path}")
                return
            
            # Preencher histórico
            for commit_hash, commit_obj, file_node in file_history:
                date_str = commit_obj.timestamp.strftime("%d/%m/%Y %H:%M")
                size_str = getattr(file_node, 'format_file_size', lambda: 'N/A')()
                file_hash = getattr(file_node, 'content_hash', 'N/A')
                
                self.file_history_tree.insert(
                    '',
                    'end',
                    text=commit_obj.message,
                    values=(
                        commit_hash[:10],
                        commit_obj.author,
                        date_str,
                        size_str,
                        file_hash[:10] if file_hash != 'N/A' else 'N/A'
                    )
                )
            
            self.update_status(f"✅ Histórico de {file_path}: {len(file_history)} versões")
            
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro no histórico:\n{e}")
    
    def browse_file_to_remove(self):
        """Procura arquivo para remover."""
        if not self.repo:
            return
        
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo para REMOVER",
            initialdir=self.repo.work_dir
        )
        
        if file_path:
            rel_path = os.path.relpath(file_path, self.repo.work_dir)
            self.remove_file_var.set(rel_path)
    
    def on_file_double_click(self, event):
        """Duplo clique seleciona arquivo para remoção."""
        selection = self.files_tree.selection()
        if selection:
            item = self.files_tree.item(selection[0])
            file_path = item['values'][0]  # Caminho completo
            self.remove_file_var.set(file_path)
    
    def remove_file(self):
        """Remove arquivo específico."""
        file_path = self.remove_file_var.get()
        if not file_path:
            messagebox.showwarning("Aviso", "❌ Selecione um arquivo para remover")
            return
        
        if not self.repo:
            return
        
        # Verificar se existe
        full_path = os.path.join(self.repo.work_dir, file_path)
        if not os.path.exists(full_path):
            messagebox.showerror("Erro", f"❌ Arquivo não encontrado: {file_path}")
            return
        
        # Confirmar
        result = messagebox.askyesno(
            "🗑️ Confirmar Remoção",
            f"⚠️ ATENÇÃO!\n\nVocê tem certeza que deseja REMOVER o arquivo:\n\n{file_path}\n\n❌ Esta ação é IRREVERSÍVEL!\n\n✅ O arquivo será deletado permanentemente."
        )
        
        if result:
            try:
                self.repo.remove_file_from_repository(file_path)
                
                messagebox.showinfo(
                    "✅ Sucesso",
                    f"Arquivo removido com sucesso!\n\n📁 Arquivo: {file_path}\n\n💡 Faça um commit para registrar a remoção no histórico."
                )
                
                self.remove_file_var.set("")
                self.refresh_all_data()
                self.update_status(f"✅ Arquivo removido: {file_path}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao remover:\n{e}")
    
    def update_repository_stats(self):
        """Atualiza estatísticas completas."""
        if not self.repo:
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, "❌ Nenhum repositório carregado")
            self.stats_text.config(state='disabled')
            return
        
        try:
            history = self.repo.get_history()
            
            # Calcular estatísticas
            total_commits = len(history)
            authors = set()
            total_files = 0
            total_size = 0
            file_types = {}
            
            for commit_hash, commit_obj in history:
                authors.add(commit_obj.author)
                files = commit_obj.file_tree.get_all_files()
                total_files = max(total_files, len(files))
                
                for file_path, file_node in files:
                    if hasattr(file_node, 'file_size'):
                        total_size += file_node.file_size
                    
                    # Contar tipos de arquivo
                    ext = os.path.splitext(file_path)[1].lower()
                    if ext:
                        file_types[ext] = file_types.get(ext, 0) + 1
                    else:
                        file_types['[sem extensão]'] = file_types.get('[sem extensão]', 0) + 1
            
            # Calcular tamanho do repositório
            repo_size = 0
            try:
                for root, dirs, files in os.walk(self.repo.vcs_dir):
                    for file in files:
                        repo_size += os.path.getsize(os.path.join(root, file))
            except:
                repo_size = 0
            
            # Gerar relatório
            stats_text = f"""📊 ESTATÍSTICAS COMPLETAS DO REPOSITÓRIO

🔢 VERSÕES E COMMITS:
   Total de versões (commits): {total_commits}
   Número de autores: {len(authors)}
   Autores: {', '.join(sorted(authors))}

📁 ARQUIVOS:
   Máximo de arquivos em uma versão: {total_files}
   Tamanho total dos arquivos: {self.format_file_size(total_size)}

📂 TIPOS DE ARQUIVO:"""

            for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
                stats_text += f"\n   {ext}: {count} arquivo(s)"

            stats_text += f"""

💾 ARMAZENAMENTO:
   Tamanho do repositório VCS: {self.format_file_size(repo_size)}
   Diretório: {self.repo.work_dir}

🔧 CONFIGURAÇÃO:
   Versão VCS: 3.0 Aprimorada
   Estrutura: Árvore N-ária
   Serialização: Pickle
   Hash: SHA-1

⏰ RELATÓRIO GERADO EM: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""
            
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats_text)
            self.stats_text.config(state='disabled')
            
            self.update_status("✅ Estatísticas atualizadas")
            
        except Exception as e:
            self.update_status(f"❌ Erro nas estatísticas: {e}")


def main():
    """Função principal."""
    try:
        root = tk.Tk()
        app = VCSEnhancedApp(root)
        root.mainloop()
    except Exception as e:
        print(f"❌ Erro ao iniciar: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
