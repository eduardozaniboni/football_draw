import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

websites = [
    # "https://gpi-apresentacao.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://transformacao.dev.el.com.br/ServerExec/acessoBase/",
    "https://gpi01.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi01-b.cloud.el.com.br/ServerExec/acessoBase/",
    "https://gpi02.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi04.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi05.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi06.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi07.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi10.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi11.cloud.el.com.br/ServerExec/acessoBase/",
    "https://gpi12.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi14.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi16.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi17.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi18.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi19.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi20.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi21.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi22.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi23.cloud.el.com.br/ServerExec/acessoBase/",
    # "https://gpi25.cloud.el.com.br/ServerExec/acessoBase/",
    "https://gpi27.cloud.el.com.br/ServerExec/acessoBase/",
]

old_version = "2.0.1.0.1"
new_version = "2.0.1.0.2"
old_version = int(old_version.replace(".", ""))
new_version = int(new_version.replace(".", ""))


gpi_updated = []
gpi_not_updated = []

options = webdriver.EdgeOptions()
options.headless = False

# Inicializar o driver do Microsoft Edge
with webdriver.Edge(options=options) as driver:
    for link in websites:
        try:
            # Acessando o site
            driver.get(link)

            driver.maximize_window()

            # Configuração de espera com WebDriverWait
            wait = WebDriverWait(driver, 20)

            parsed_url = urlparse(link)
            url_system = parsed_url.netloc

            if wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div[2]/button[2]"))):
                cookies = driver.find_element(
                    By.XPATH, "/html/body/div[4]/div/div/div[2]/button[2]")
                cookies.click()

            user = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Usuário']")))

            password = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Senha']")))

            user.send_keys("iasmine.mascarello")
            if link != "https://gpi12.cloud.el.com.br/ServerExec/acessoBase/":
                password.send_keys("123")
            else:
                password.send_keys("Senhanova")

            enter_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Entrar']")))
            enter_button.click()

            search_client = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@tid='login_clientes.list']")))
            search_client.click()

            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='GFICH-FCL']/table/tbody")))

            tbody_client = driver.find_element(
                By.XPATH, "//div[@class='GFICH-FCL']/table/tbody")
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

            search_environment = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//button[@tid='login_ambientes.list']")))
            search_environment.click()

            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='GFICH-FCMH']/div/div[@class='GFICH-FCAI']/div/div/div[@class='GFICH-FCL']/table/tbody")))

            tbody_environment = driver.find_element(
                By.XPATH, "//div[@class='GFICH-FCMH']/div/div[@class='GFICH-FCAI']/div/div/div[@class='GFICH-FCL']/table/tbody")
            tr_environments = tbody_environment.find_elements(
                By.TAG_NAME, "tr")

            for tr in tr_environments:
                span_text_environment = tr.find_element(By.TAG_NAME, "span")
                if "TRB - Administrador Geral" in span_text_environment.text:
                    span_text_environment.click()
                    break
                if "GPI - Administrador Geral" in span_text_environment.text:
                    span_text_environment.click()
                    break

            next_button = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//button[text()='Prosseguir']")))
            next_button.click()

            current_version = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='panelBuildVersion']/div[2]")))
            current_version = int(current_version.text.replace(".", ""))

            if current_version > old_version:
                current_version = ".".join(str(current_version))
                gpi_updated.append(
                    f"GPI: {url_system} - Versão Atual: {current_version}")
            elif current_version == old_version:
                current_version = ".".join(str(current_version))
                gpi_not_updated.append(
                    f"GPI: {url_system} - Versão Atual: {current_version}")

        except Exception as ex:
            print(f"Não foi possível acessar o link: {link}")

    old_version = ".".join(str(old_version))
    new_version = ".".join(str(new_version))

    if len(gpi_updated) > 0:
        print("----------------------------------------------------")
        print("** GPI Atualizados **\n")
        for up in gpi_updated:
            print(up)
        print(f"\nVersão Antiga: {old_version} → Versão Atual: {
            current_version}")
        print("----------------------------------------------------")

    if len(gpi_not_updated) > 0:
        print("----------------------------------------------------")
        print("** GPI *NÃO* Atualizados **\n")
        for not_up in gpi_not_updated:
            print(not_up)
        print(f"\nVersão Antiga: {old_version} → Versão Atual: {
              current_version}")
        print("----------------------------------------------------")

    # Fechando o navegador
    driver.quit()
