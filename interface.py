import tkinter as tk
from tkinter import messagebox, ttk
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import datetime

class Participante:
    def __init__(self, nome, email, sugestoes, valor_min, valor_max):
        self.nome = nome
        self.email = email
        self.sugestoes = sugestoes
        self.valor_min = valor_min
        self.valor_max = valor_max

class AmigoSecreto:
    def __init__(self):
        self.participantes = {}
        
        self.root = tk.Tk()
        self.root.title(" Amigo Secreto")
        self.root.geometry("600x700")
        
        # Definindo cores
        self.bg_color = "#F5F7FA"  # Fundo principal suave
        self.primary_color = "#6C63FF"  # Roxo moderno
        self.secondary_color = "#FF6B6B"  # Vermelho suave
        self.accent_color = "#4ECDC4"  # Verde água
        
        self.root.configure(bg=self.bg_color)
        
        # Título principal
        self.title_label = tk.Label(self.root, 
                                  text=" Amigo Secreto", 
                                  font=("Helvetica", 24, "bold"),
                                  bg=self.bg_color,
                                  fg=self.primary_color)
        self.title_label.pack(pady=20)
        
        # Criar notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Aba de Cadastro
        self.tab_cadastro = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_cadastro, text='Cadastro')
        self.setup_cadastro_tab()
        
        # Aba de Participantes
        self.tab_participantes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_participantes, text='Participantes')
        self.setup_participantes_tab()
        
        # Aba de Sorteio
        self.tab_sorteio = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sorteio, text='Sorteio')
        self.setup_sorteio_tab()
        
        # Configurações de Email
        self.email_config = {
            'sender_email': '',
            'sender_password': ''
        }
        
    def setup_cadastro_tab(self):
        frame = ttk.Frame(self.tab_cadastro, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Campos de cadastro
        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nome_entry = ttk.Entry(frame, width=40)
        self.nome_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(frame, width=40)
        self.email_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Sugestões de Presente:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.sugestoes_text = tk.Text(frame, width=30, height=4)
        self.sugestoes_text.grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Valor Mínimo (R$):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.valor_min_entry = ttk.Entry(frame, width=20)
        self.valor_min_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(frame, text="Valor Máximo (R$):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.valor_max_entry = ttk.Entry(frame, width=20)
        self.valor_max_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(frame, 
                  text="Cadastrar Participante",
                  command=self.cadastrar_participante).grid(row=5, column=0, columnspan=2, pady=20)
        
    def setup_participantes_tab(self):
        frame = ttk.Frame(self.tab_participantes, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Lista de participantes com scrollbar
        self.tree = ttk.Treeview(frame, columns=('Nome', 'Email', 'Valor Min', 'Valor Max'), 
                                show='headings', height=10)
        
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Valor Min', text='Valor Min')
        self.tree.heading('Valor Max', text='Valor Max')
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        ttk.Button(frame, 
                  text="Remover Selecionado",
                  command=self.remover_participante).grid(row=1, column=0, pady=10)
        
    def setup_sorteio_tab(self):
        frame = ttk.Frame(self.tab_sorteio, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Opções de sorteio
        ttk.Label(frame, text="Escolha o tipo de sorteio:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Botão para sorteio local
        ttk.Button(frame, 
                  text="Realizar Sorteio Local",
                  command=self.realizar_sorteio_local).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Separador
        ttk.Separator(frame, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky='ew', pady=15)
        
        # Seção de envio por email
        ttk.Label(frame, text="Sorteio com envio por email:", font=("Helvetica", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="Email Remetente:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.sender_email_entry = ttk.Entry(frame, width=40)
        self.sender_email_entry.grid(row=4, column=1, pady=5)
        
        ttk.Label(frame, text="Senha do App:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.sender_password_entry = ttk.Entry(frame, width=40, show="*")
        self.sender_password_entry.grid(row=5, column=1, pady=5)
        
        ttk.Button(frame, 
                  text="Realizar Sorteio e Enviar Emails",
                  command=self.realizar_sorteio).grid(row=6, column=0, columnspan=2, pady=20)

    def cadastrar_participante(self):
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().strip()
        sugestoes = self.sugestoes_text.get("1.0", tk.END).strip()
        
        try:
            valor_min = float(self.valor_min_entry.get())
            valor_max = float(self.valor_max_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Os valores mínimo e máximo devem ser números!")
            return
            
        if not all([nome, email]):
            messagebox.showerror("Erro", "Nome e email são obrigatórios!")
            return
            
        if nome in self.participantes:
            messagebox.showerror("Erro", "Este participante já está cadastrado!")
            return
            
        self.participantes[nome] = Participante(nome, email, sugestoes, valor_min, valor_max)
        self.atualizar_lista_participantes()
        self.limpar_campos_cadastro()
        messagebox.showinfo("Sucesso", "Participante cadastrado com sucesso!")
        
    def limpar_campos_cadastro(self):
        self.nome_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.sugestoes_text.delete("1.0", tk.END)
        self.valor_min_entry.delete(0, tk.END)
        self.valor_max_entry.delete(0, tk.END)
        
    def atualizar_lista_participantes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for p in self.participantes.values():
            self.tree.insert('', tk.END, values=(p.nome, p.email, f"R$ {p.valor_min:.2f}", f"R$ {p.valor_max:.2f}"))
            
    def remover_participante(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um participante para remover!")
            return
            
        nome = self.tree.item(selected_item)['values'][0]
        del self.participantes[nome]
        self.atualizar_lista_participantes()
        
    def enviar_email(self, destinatario, amigo_secreto, info_amigo):
        if not all([self.email_config['sender_email'], self.email_config['sender_password']]):
            messagebox.showerror("Erro", "Configure o email remetente e senha primeiro!")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = destinatario
            msg['Subject'] = "Seu Amigo Secreto! "
            
            corpo_email = f"""
            Olá!
            
            Seu amigo secreto é: {amigo_secreto}
            
            Informações sobre seu amigo secreto:
            Sugestões de presentes: {info_amigo.sugestoes}
            Faixa de valor: R$ {info_amigo.valor_min:.2f} - R$ {info_amigo.valor_max:.2f}
            
            Feliz Natal! 
            """
            
            msg.attach(MIMEText(corpo_email, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['sender_password'])
            server.send_message(msg)
            server.quit()
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar email: {str(e)}")
            return False
            
    def realizar_sorteio(self):
        if len(self.participantes) < 2:
            messagebox.showwarning("Aviso", "É necessário pelo menos 2 participantes!")
            return
            
        self.email_config['sender_email'] = self.sender_email_entry.get().strip()
        self.email_config['sender_password'] = self.sender_password_entry.get().strip()
        
        if not all([self.email_config['sender_email'], self.email_config['sender_password']]):
            messagebox.showerror("Erro", "Configure o email remetente e senha!")
            return
            
        nomes = list(self.participantes.keys())
        random.shuffle(nomes)
        
        sorteio = {}
        for i in range(len(nomes)):
            sorteio[nomes[i]] = nomes[(i + 1) % len(nomes)]
            
        # Enviar emails
        sucesso = True
        for pessoa, amigo in sorteio.items():
            if not self.enviar_email(
                self.participantes[pessoa].email,
                amigo,
                self.participantes[amigo]
            ):
                sucesso = False
                break
                
        if sucesso:
            messagebox.showinfo("Sucesso", "Sorteio realizado e emails enviados com sucesso!")
        else:
            messagebox.showerror("Erro", "Houve um problema ao enviar os emails. Tente novamente.")
            
    def realizar_sorteio_local(self):
        if len(self.participantes) < 2:
            messagebox.showerror("Erro", "É necessário ter pelo menos 2 participantes para realizar o sorteio!")
            return
            
        # Criar lista de nomes
        nomes = list(self.participantes.keys())
        sorteio = nomes.copy()
        
        # Realizar sorteio
        while any(nomes[i] == sorteio[i] for i in range(len(nomes))):
            random.shuffle(sorteio)
        
        # Criar janela com resultado
        resultado_window = tk.Toplevel(self.root)
        resultado_window.title("Resultado do Sorteio")
        resultado_window.geometry("400x500")
        
        # Criar texto explicativo
        ttk.Label(resultado_window, 
                 text="Clique em cada nome para ver quem tirou:", 
                 font=("Helvetica", 12, "bold")).pack(pady=10)
        
        # Frame para os botões
        button_frame = ttk.Frame(resultado_window)
        button_frame.pack(pady=10, expand=True, fill='both')
        
        # Dicionário para armazenar os resultados
        self.resultados_botoes = {}
        
        # Criar botões para cada participante
        for i, nome in enumerate(nomes):
            amigo = sorteio[i]
            btn = ttk.Button(button_frame, 
                           text=nome,
                           command=lambda n=nome, a=amigo: self.mostrar_amigo_secreto(n, a))
            btn.pack(pady=5)
            self.resultados_botoes[nome] = {'botao': btn, 'amigo': amigo, 'revelado': False}
            
    def mostrar_amigo_secreto(self, nome, amigo):
        if not self.resultados_botoes[nome]['revelado']:
            self.resultados_botoes[nome]['botao'].configure(
                text=f"{nome} → {amigo}")
            self.resultados_botoes[nome]['revelado'] = True
        else:
            self.resultados_botoes[nome]['botao'].configure(
                text=nome)
            self.resultados_botoes[nome]['revelado'] = False
            
    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AmigoSecreto()
    app.iniciar()
