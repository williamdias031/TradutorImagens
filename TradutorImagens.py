#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import pytesseract
from PIL import Image
import pyautogui
import tkinter as tk
from tkinter import filedialog
from googletrans import Translator
import time
import unicodedata

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 

def normalizar_texto(texto):
 
    texto_normalizado = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto_normalizado

def realizar_ocr(imagem):
    custom_config = r'--oem 3 --psm 6' 
    texto = pytesseract.image_to_string(imagem, lang='por', config=custom_config)
    print("Texto extraído:", texto) 
    return texto

def traduzir_texto(texto, idioma_destino='pt'):
    texto_normalizado = normalizar_texto(texto)
    translator = Translator()
    traducao = translator.translate(texto_normalizado, dest=idioma_destino)
    return traducao.text


def capturar_tela():
   
    screenshot = pyautogui.screenshot()
    screenshot.save("captura.png")  
    imagem = Image.open("captura.png")
    return imagem


def abrir_imagem():
    file_path = filedialog.askopenfilename(title="Selecione uma Imagem")
    if file_path:
        imagem = Image.open(file_path)
        return imagem
    return None


def interface_usuario():
    
    janela = tk.Tk()
    janela.title("Tradutor de Imagens Teste William")
    janela.geometry("400x400")

    
    def capturar_e_traduzir():
        imagem = capturar_tela()
        texto_extraido = realizar_ocr(imagem)
        if texto_extraido.strip():
            texto_traduzido = traduzir_texto(texto_extraido)
            label_resultado.config(text=f"Texto Traduzido: \n{texto_traduzido}")
        else:
            label_resultado.config(text="Nenhum texto encontrado.")

    
    def abrir_e_traduzir():
        imagem = abrir_imagem()
        if imagem:
            texto_extraido = realizar_ocr(imagem)
            if texto_extraido.strip():
                texto_traduzido = traduzir_texto(texto_extraido)
                label_resultado.config(text=f"Texto Traduzido: \n{texto_traduzido}")
            else:
                label_resultado.config(text="Nenhum texto encontrado.")

    # Criar os botões
    botao_capturar_tela = tk.Button(janela, text="Capturar Tela", command=capturar_e_traduzir)
    botao_capturar_tela.pack(pady=20)

    botao_abrir_imagem = tk.Button(janela, text="Abrir Imagem", command=abrir_e_traduzir)
    botao_abrir_imagem.pack(pady=20)

    # Label para mostrar o resultado
    label_resultado = tk.Label(janela, text="", wraplength=350)
    label_resultado.pack(pady=20)

    # Iniciar a interface gráfica
    janela.mainloop()

# Chamar a interface de usuário
if __name__ == "__main__":
    interface_usuario()