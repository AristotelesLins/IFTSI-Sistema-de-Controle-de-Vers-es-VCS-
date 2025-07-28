#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica do Sistema VCS - Versão Modular

Este módulo implementa a interface gráfica usando Tkinter para
interagir com o sistema de controle de versões modular.

A interface permite:
- Criar/abrir repositórios
- Fazer commits
- Visualizar histórico
- Realizar checkout de versões anteriores

Autor: Milton
Data: 2025
"""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

# Importa as classes do módulo VCS Core
from vcs_core import Repository


class VCSApp:
    """
    Aplicação GUI para o Sistema de Controle de Versões.
    
    Interface gráfica completa para interagir com o sistema VCS,
    oferecendo todas as funcionalidades através de uma interface
    amigável usando Tkinter.
    """
    
    def __init__(self, root):
        """
        Inicializa a aplicação GUI.
        
        Args:
            root: Widget raiz do Tkinter
        """
        self.root = root
        self.root.title("Sistema de Controle de Versões - VCS Modular")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Estado da aplicação
        self.repo = None
        self.history_cache = []
        
        # Configura a interface
        self._setup_ui()
        self._update_ui_state()
    
    def _setup_ui(self):
        """
        Configura todos os elementos da interface gráfica.
        """
        # Frame superior - controles principais
        top_frame = tk.Frame(self.root, pady=15, padx=10)
        top_frame.pack(fill=tk.X)
        
        # Label de status do repositório
        self.repo_path_label = tk.Label(
            top_frame, 
            text="Repositório: Nenhum selecionado",
            font=("Arial", 10, "bold"),
            fg="red"
        )
        self.repo_path_label.pack(pady=(0, 10))
        
        # Frame para botões principais
        buttons_frame = tk.Frame(top_frame)
        buttons_frame.pack()
        
        # Botão para selecionar/criar repositório
        self.btn_select_repo = tk.Button(
            buttons_frame,
            text="📁 Abrir/Criar Repositório",
            command=self.select_repo,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        )
        self.btn_select_repo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão de commit
        self.btn_commit = tk.Button(
            buttons_frame,
            text="💾 Fazer Commit",
            command=self.do_commit,
            state=tk.DISABLED,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=5
        )
        self.btn_commit.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão de checkout
        self.btn_checkout = tk.Button(
            buttons_frame,
            text="🔄 Fazer Checkout",
            command=self.do_checkout,
            state=tk.DISABLED,
            font=("Arial", 10),
            bg="#FF9800",
            fg="white",
            padx=20,
            pady=5
        )
        self.btn_checkout.pack(side=tk.LEFT)
        
        # Frame do histórico
        history_frame = tk.Frame(self.root, padx=10, pady=5)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label do histórico
        history_label = tk.Label(
            history_frame,
            text="📋 Histórico de Commits",
            font=("Arial", 12, "bold")
        )
        history_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Frame para listbox e scrollbar
        list_frame = tk.Frame(history_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox para histórico com scrollbar
        self.history_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.SINGLE,
            font=("Courier", 10),
            bg="#f8f9fa",
            selectbackground="#007acc",
            selectforeground="white"
        )
        
        # Scrollbar vertical
        scrollbar_y = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox.config(yscrollcommand=scrollbar_y.set)
        scrollbar_y.config(command=self.history_listbox.yview)
        
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar horizontal
        scrollbar_x = tk.Scrollbar(history_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(fill=tk.X)
        
        self.history_listbox.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.config(command=self.history_listbox.xview)
        
        # Frame de informações
        info_frame = tk.Frame(self.root, padx=10, pady=5)
        info_frame.pack(fill=tk.X)
        
        self.info_label = tk.Label(
            info_frame,
            text="Selecione um repositório para começar",
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT
        )
        self.info_label.pack(anchor=tk.W)
    
    def _update_ui_state(self):
        """
        Atualiza o estado dos elementos da interface baseado no repositório atual.
        """
        has_repo = self.repo is not None and self.repo.is_repository()
        
        # Atualiza botões
        state = tk.NORMAL if has_repo else tk.DISABLED
        self.btn_commit.config(state=state)
        self.btn_checkout.config(state=state)
        
        # Atualiza label do repositório
        if has_repo:
            self.repo_path_label.config(
                text=f"Repositório: {self.repo.work_dir}",
                fg="green"
            )
            status = self.repo.get_status()
            commits_count = status.get('total_commits', 0)
            head_msg = status.get('head_commit_message', 'N/A')
            self.info_label.config(
                text=f"Total de commits: {commits_count} | HEAD: {head_msg}"
            )
        else:
            self.repo_path_label.config(
                text="Repositório: Nenhum selecionado",
                fg="red"
            )
            self.info_label.config(text="Selecione um repositório para começar")
    
    def select_repo(self):
        """
        Permite ao usuário selecionar ou criar um repositório.
        """
        path = filedialog.askdirectory(title="Selecione a pasta do repositório")
        if not path:
            return
        
        try:
            # Verifica se já é um repositório
            temp_repo = Repository(path)
            
            if not temp_repo.is_repository():
                # Não é um repositório, pergunta se quer criar
                if messagebox.askyesno(
                    "Criar Repositório?",
                    f"A pasta '{path}' não contém um repositório VCS.\\n\\n"
                    f"Deseja inicializar um novo repositório?"
                ):
                    temp_repo.init()
                    messagebox.showinfo(
                        "Sucesso",
                        "Repositório criado com sucesso!"
                    )
                else:
                    return
            
            # Define o repositório atual
            self.repo = temp_repo
            self._update_ui_state()
            self.refresh_history()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir repositório:\\n{str(e)}")
    
    def refresh_history(self):
        """
        Atualiza a lista de histórico de commits.
        """
        # Limpa a lista atual
        self.history_listbox.delete(0, tk.END)
        self.history_cache = []
        
        if not self.repo or not self.repo.is_repository():
            return
        
        try:
            # Obtém o histórico
            self.history_cache = self.repo.get_history()
            
            if not self.history_cache:
                self.history_listbox.insert(tk.END, "Nenhum commit encontrado")
                return
            
            # Popula a lista
            for i, (commit_hash, commit_obj) in enumerate(self.history_cache):
                date_str = commit_obj.get_formatted_timestamp()
                short_hash = commit_hash[:10]
                short_message = commit_obj.get_short_message(30)  # Reduzido para caber o autor
                files_count = commit_obj.get_file_count()
                author = commit_obj.author[:15]  # Limita o nome do autor
                
                # Marca o commit atual (HEAD)
                marker = "👑" if i == 0 else "  "
                
                display_text = (f"{marker} {short_hash} | {date_str} | "
                              f"👤{author} | {files_count:2d} arquivos | {short_message}")
                
                self.history_listbox.insert(tk.END, display_text)
            
            # Seleciona o primeiro item (HEAD)
            if self.history_cache:
                self.history_listbox.selection_set(0)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar histórico:\\n{str(e)}")
    
    def do_commit(self):
        """
        Realiza um novo commit.
        """
        if not self.repo or not self.repo.is_repository():
            messagebox.showwarning("Aviso", "Nenhum repositório selecionado.")
            return
        
        # Solicita a mensagem do commit
        message = simpledialog.askstring(
            "Novo Commit",
            "Digite a mensagem do commit:",
            initialvalue=""
        )
        
        if not message or not message.strip():
            return
        
        # Solicita o nome do autor
        author = simpledialog.askstring(
            "Autor do Commit",
            "Digite o nome do autor:",
            initialvalue="Default User"
        )
        
        if not author or not author.strip():
            author = "Default User"
        
        try:
            # Realiza o commit
            commit_hash = self.repo.commit(message.strip(), author.strip())
            
            messagebox.showinfo(
                "Sucesso",
                f"Commit realizado com sucesso!\\n\\n"
                f"Hash: {commit_hash[:10]}\\n"
                f"Autor: {author}\\n"
                f"Mensagem: {message}"
            )
            
            # Atualiza a interface
            self.refresh_history()
            self._update_ui_state()
            
        except Exception as e:
            messagebox.showerror("Erro no Commit", f"Erro ao fazer commit:\\n{str(e)}")
    
    def do_checkout(self):
        """
        Realiza o checkout para um commit selecionado.
        """
        # Verifica se há seleção
        selection_index = self.history_listbox.curselection()
        if not selection_index:
            messagebox.showwarning(
                "Aviso",
                "Selecione um commit da lista para fazer o checkout."
            )
            return
        
        if not self.history_cache:
            return
        
        selected_index = selection_index[0]
        if selected_index >= len(self.history_cache):
            return
        
        commit_hash, commit_obj = self.history_cache[selected_index]
        
        # Confirmação
        if not messagebox.askyesno(
            "Confirmar Checkout",
            f"Tem certeza que deseja restaurar o estado do commit?\\n\\n"
            f"Hash: {commit_hash[:10]}\\n"
            f"Autor: {commit_obj.author}\\n"
            f"Mensagem: {commit_obj.message}\\n"
            f"Data: {commit_obj.get_formatted_timestamp()}\\n\\n"
            f"⚠️ ATENÇÃO: Todas as alterações não salvas no diretório "
            f"de trabalho serão perdidas!"
        ):
            return
        
        try:
            # Realiza o checkout
            self.repo.checkout(commit_hash)
            
            messagebox.showinfo(
                "Sucesso",
                f"Checkout concluído!\\n\\n"
                f"O diretório foi restaurado para o estado do commit:\\n"
                f"{commit_hash[:10]} por {commit_obj.author}\\n"
                f"Mensagem: {commit_obj.message}"
            )
            
            # Atualiza a interface
            self.refresh_history()
            self._update_ui_state()
            
        except Exception as e:
            messagebox.showerror("Erro no Checkout", f"Erro ao fazer checkout:\\n{str(e)}")


def main():
    """
    Função principal para executar a aplicação.
    """
    try:
        root = tk.Tk()
        app = VCSApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
