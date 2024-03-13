import re
import sys
import os
import tkinter as tk
from tkinter import messagebox, filedialog, Label, Frame, Scrollbar, Entry, Button, Listbox
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import threading

# Variáveis globais para armazenar os links e os resultados
websites = []
gpi_updated = []
gpi_not_updated = []


def import_links():
    global websites
    file_types = [('Text files', '*.txt')]
    file_path = filedialog.askopenfilename(filetypes=file_types)

    if file_path:
        try:
            with open(file_path, 'r') as file:
                websites = file.read().strip().split('\n')
            messagebox.showinfo("Importação bem-sucedida", f"{len(websites)} links importados!")
            imported_links_listbox.delete(0, tk.END)
            for link in websites:
                imported_links_listbox.insert(tk.END, link)
        except Exception as e:
            messagebox.showerror("Erro de Importação", f"Não foi possível importar os links: {e}")
    else:
        messagebox.showwarning("Importação Cancelada", "Nenhum arquivo foi selecionado para importação.")


def clear_lists():
    updated_links_listbox.delete(0, tk.END)
    not_updated_links_listbox.delete(0, tk.END)


def execute_verification():
    clear_lists()
    new_version = new_version_entry.get()

    version_pattern = r"^\d+(\.\d+)+$"

    if not websites:
        messagebox.showwarning("Aviso", "Nenhum arquivo de links foi importado. Por favor, importe um arquivo antes de continuar.")
        return

    if re.match(version_pattern, new_version):
        try:
            new_version_int = int(new_version.replace(".", ""))
            threading.Thread(target=verify_links, args=[new_version_int]).start()
        except ValueError:
            messagebox.showerror("Erro", "Formato de versão inválido. Certifique-se de usar apenas números e pontos.")
    else:
        messagebox.showerror("Erro de Validação", "Os campos de versão devem seguir o padrão numérico (Ex: 2.0.1.0.1).")


def create_scrolled_listbox(frame, label_text, row, height=10, width=75):
    Label(frame, text=label_text).grid(row=row, column=0, sticky='w', columnspan=2)
    scrollbar = Scrollbar(frame, orient="vertical")
    listbox = Listbox(frame, height=height, width=width, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    listbox.grid(row=row + 1, column=0, sticky='ew')
    scrollbar.grid(row=row + 1, column=1, sticky='ns')
    return listbox


def verify_links(new_version):
    global gpi_updated, gpi_not_updated
    gpi_updated = []
    gpi_not_updated = []

    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    driver_path = os.path.join(base_path, "msedgedriver.exe")

    service = Service(executable_path=driver_path)
    # service = Service(executable_path="./edgedriver_win64/msedgedriver.exe")

    options = webdriver.EdgeOptions()
    options.headless = True

    with webdriver.Edge(service=service, options=options) as driver:
        total_links = len(websites)
        for index, link in enumerate(websites, start=1):
            try:
                current_status = f"Verificação {index} de {total_links}"
                root.after(0, lambda: status_label.config(text=current_status))

                # Acessando o site
                driver.get(link)

                driver.maximize_window()

                # Configuração de espera com WebDriverWait
                wait = WebDriverWait(driver, 20)

                parsed_url = urlparse(link)
                url_system = parsed_url.netloc

                if wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div[2]/button[2]"))):
                    cookies = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/button[2]")
                    cookies.click()

                user = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Usuário']")))

                password = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Senha']")))

                user.send_keys("iasmine.mascarello")
                if link != "https://gpi12.cloud.el.com.br/ServerExec/acessoBase/":
                    password.send_keys("123")
                else:
                    password.send_keys("Senhanova")

                enter_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Entrar']")))
                enter_button.click()

                search_client = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@tid='login_clientes.list']")))
                search_client.click()

                wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='GFICH-FCL']/table/tbody")))

                tbody_client = driver.find_element(By.XPATH, "//div[@class='GFICH-FCL']/table/tbody")
                tr_clients = tbody_client.find_elements(By.TAG_NAME, "tr")

                for tr in tr_clients:
                    span_text_client = tr.find_element(By.TAG_NAME, "span")
                    if "PREFEITURA" in span_text_client.text.upper():
                        span_text_client.click()
                        break
                    if "MUNICIPIO" in span_text_client.text.upper():
                        span_text_client.click()
                        break
                    if "GPI - Gestão Pública Integrada" in span_text_client.text:
                        span_text_client.click()
                        break

                search_environment = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@tid='login_ambientes.list']")))
                search_environment.click()

                wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='GFICH-FCMH']/div/div[@class='GFICH-FCAI']/div/div/div[@class='GFICH-FCL']/table/tbody")))

                tbody_environment = driver.find_element(By.XPATH, "//div[@class='GFICH-FCMH']/div/div[@class='GFICH-FCAI']/div/div/div[@class='GFICH-FCL']/table/tbody")
                tr_environments = tbody_environment.find_elements(By.TAG_NAME, "tr")

                for tr in tr_environments:
                    span_text_environment = tr.find_element(By.TAG_NAME, "span")
                    if "TRB - Administrador Geral" in span_text_environment.text:
                        span_text_environment.click()
                        break
                    if "GPI - Administrador Geral" in span_text_environment.text:
                        span_text_environment.click()
                        break

                next_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Prosseguir']")))
                next_button.click()

                current_version = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='panelBuildVersion']/div[2]")))
                current_version = int(current_version.text.replace(".", ""))

                if current_version <= new_version:
                    current_version = ".".join(str(current_version))
                    gpi_updated.append(f"{url_system} - Versão Atual: {current_version}")
                else:
                    current_version = ".".join(str(current_version))
                    gpi_not_updated.append(f"{url_system} - Versão Atual: {current_version}")
            except Exception as ex:
                messagebox.showerror("Erro", f"Não foi possível acessar o link: {link}")

    # Após a execução, atualize as listas na interface gráfica
    for item in gpi_updated:
        updated_links_listbox.insert(tk.END, item)
    for item in gpi_not_updated:
        not_updated_links_listbox.insert(tk.END, item)


# GUI setup
root = tk.Tk()
root.title("Verificador de Versão GPI")

# Divisão em frames
frame_top = Frame(root)
frame_top.grid(row=0, column=0, padx=10, pady=5, sticky='ew', columnspan=2)

frame_middle = Frame(root)
frame_middle.grid(row=1, column=0, padx=10, pady=5, sticky='ew', columnspan=2)

frame_bottom = Frame(root)
frame_bottom.grid(row=2, column=0, padx=10, pady=5, sticky='ew', columnspan=2)

# Widgets no frame_top
Label(frame_top, text="Nova Versão:").grid(row=1, column=0, sticky='w')
new_version_entry = Entry(frame_top)
new_version_entry.grid(row=1, column=1, sticky='ew')

# Botões no frame_middle
import_button = Button(frame_middle, text="Importar Links", command=import_links)
import_button.grid(row=0, column=0, pady=5, sticky='ew')

execute_button = Button(frame_middle, text="Executar Verificação", command=execute_verification)
execute_button.grid(row=0, column=1, pady=5, sticky='ew')

# Criando Listbox e Scrollbar para cada categoria
imported_links_listbox = create_scrolled_listbox(frame_bottom, "Links Importados:", 0)
updated_links_listbox = create_scrolled_listbox(frame_bottom, "Links Atualizados (GPI):", 2)
not_updated_links_listbox = create_scrolled_listbox(frame_bottom, "Links Não Atualizados (GPI):", 4)

# Status label
status_label = Label(root, text="Status: Aguardando a inicialização...")
status_label.grid(row=3, column=0, columnspan=2, padx=10)

root.columnconfigure(0, weight=1)  # Faz com que a coluna esquerda expanda
root.rowconfigure(2, weight=1)  # Permite que o frame_bottom expanda verticalmente

root.mainloop()
