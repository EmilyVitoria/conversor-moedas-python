import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Lista de moedas suportadas
MOEDAS = {
    "Dólar Americano (USD)": "USD",
    "Euro (EUR)": "EUR",
    "Bitcoin (BTC)": "BTC",
    "Peso Argentino (ARS)": "ARS"
}

def obter_cotacao(moeda_destino):
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda_destino}-BRL"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()
        chave = f"{moeda_destino}BRL"
        return float(dados[chave]['bid'])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao obter cotação da API:\n{e}")
        return None

def converter():
    try:
        valor_reais = float(entrada_valor.get().replace(",", "."))
        moeda_escolhida = combo_moedas.get()
        codigo_moeda = MOEDAS.get(moeda_escolhida)

        if not codigo_moeda:
            messagebox.showwarning("Aviso", "Selecione uma moeda válida.")
            return

        cotacao = obter_cotacao(codigo_moeda)
        if cotacao:
            valor_convertido = valor_reais / cotacao
            resultado.set(f"R$ {valor_reais:.2f} = {valor_convertido:.2f} {codigo_moeda}")
    except ValueError:
        messagebox.showwarning("Entrada inválida", "Digite um valor numérico válido.")

# Interface Gráfica
janela = tk.Tk()
janela.title("💸 Conversor de Moedas")
janela.geometry("400x300")
janela.resizable(False, False)
janela.configure(bg="#1e1e2f")

# Estilos
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("TLabel", background="#1e1e2f", foreground="#ffffff", font=("Segoe UI", 10))
estilo.configure("TButton", font=("Segoe UI", 10, "bold"))
estilo.configure("TCombobox", fieldbackground="#ffffff", background="#ffffff")

# Widgets
ttk.Label(janela, text="Valor em Reais (R$):").pack(pady=10)
entrada_valor = ttk.Entry(janela, width=20, justify="center")
entrada_valor.pack()

ttk.Label(janela, text="Converter para:").pack(pady=10)
combo_moedas = ttk.Combobox(janela, values=list(MOEDAS.keys()), state="readonly")
combo_moedas.pack()
combo_moedas.set("Dólar Americano (USD)")

ttk.Button(janela, text="Converter", command=converter).pack(pady=20)

resultado = tk.StringVar()
ttk.Label(janela, textvariable=resultado, font=("Segoe UI", 12, "bold")).pack(pady=10)

ttk.Label(janela, text="Feito por Emi 💚", font=("Segoe UI", 8)).pack(side="bottom", pady=5)

janela.mainloop()
