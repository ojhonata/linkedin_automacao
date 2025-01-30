from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

usuario = input('Digite o seu usuário: ')
senha = input('Digite a sua senha: ')
termo = input('Digite o que deseja pesquisar: ')

# função para digitar lentamente
def digitar_devagar(elemento, texto, atraso=0.2):
    for caracter in texto:
        elemento.send_keys(caracter)
        time.sleep(atraso)

# função para fazer login mo linkedin
def login(navegador, username, password):
    usuario = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    digitar_devagar(usuario, username)

    senha = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    digitar_devagar(senha, password)

    botao_entrar = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'btn__primary--large'))
    )
    botao_entrar.click()

# função para buscar pessoas no linkedin
def buscar_pessoas(navegador, termo):
    campo_pesquisa = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'search-global-typeahead__input'))
    )
    digitar_devagar(campo_pesquisa, termo + Keys.RETURN)

    botao_pessoa = WebDriverWait(navegador, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[text()="Pessoas"]'))
    )
    time.sleep(2)
    botao_pessoa.click()

# funçãop que envia solicitações de conexão com pessoas
def conectar_pessoas(navegador):
    time.sleep(3)
    botao_conectar = WebDriverWait(navegador, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//span[text()="Conectar"]'))
    )

    for botao in botao_conectar: # itera sobre todos os botões 'Conectar'
        time.sleep(1)
        navegador.execute_script("arguments[0].scrollIntoView(true);", botao)

        navegador.execute_script("arguments[0].click()", botao)
        time.sleep(1)

        try:
            botao_sem_nota = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Enviar sem nota"]'))
            )
            navegador.execute_script("arguments[0].click();", botao_sem_nota)
        except Exception as e:
            print(f'Erro ao enviar sem nota: {e}')

# função principal para controlar o fluxo do script
def main():
    # configurando o navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    navegador = webdriver.Chrome(options=options)
    navegador.get('https://www.linkedin.com/feed/')

    try:
        # Realiza o login, busca pessoas e envia solicitações de conexão
        login(navegador, usuario, senha)
        buscar_pessoas(navegador, termo)
        conectar_pessoas(navegador)
    finally:
        print('Fechando o navegador')
        navegador.quit()

# Executa a função principal se o script for executado diretamente
if __name__ == '__main__':
    main()