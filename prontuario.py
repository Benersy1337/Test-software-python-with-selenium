from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
#options.add_argument("--window-size=1980,1020")
options.add_argument("--log-level=3")
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

login_url = 'https://suascanoinhas.pmc.sc.gov.br/'

print('Passo 1: Acessar o site do Prontuário')
try:
    driver.get(login_url)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.save_screenshot('tela01.png')
    time.sleep(2)
except:
    driver.quit()
    print('Erro ao acessar o site do Prontuário')
    quit()
    
print('Passo 2: Envia os dados para o login')

username = ''
password = ''

try:
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div/div/div/form/div[1]/div/input').send_keys(username)
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div/div/div/form/div[2]/div/input').send_keys(password, Keys.ENTER)
except:
        driver.quit()
        print('Erro ao enviar dados para o login')
        
print('Passo 3: Clica em Minhas Ações')
try:
    driver.find_element(By.XPATH,'//*[@id="sidenav-collapse-main"]/ul/li[4]/a/span').click()
except:
    driver.quit()
    print('Erro ao localizar link sair')


print('Passo 4: Acessa o filtro e escolhe a ordem por atendimentos mais antigos')
try:
   
    driver.find_element(By.XPATH,'//*[@id="id_ordenar"]').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,'option[value="data_atendimento"]').click()
    # //*[@id="id_ordenar"]/option[3]
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="panel"]/div[2]/div/div/div/div/div[3]/div/div[1]/div/form/div/div[3]/button').click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="panel"]/div[2]/div/div/div/div/div[3]/div/div[2]/div[1]/div/div[3]/a').click()
    

    driver.save_screenshot('tela02.png')
    time.sleep(2)
except:
    driver.quit()
    print('Erro ao acessar o menu...')
    quit()

print('Passo 5: Capturar os detalhes do atendimento')
try:
    tabela = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="panel"]/div[2]/div/div/div/div')))
    conteudo_html = tabela.get_attribute('outerHTML')
    lista = BeautifulSoup(conteudo_html,'html.parser')

    with open('lista_produtos.csv','w') as arquivo:
        for produto in lista.find_all('div',{'class':'card-body border-0'}):
            linha = ''
            for nome in produto.find_all('p'):
                linha +=nome.text
                print(linha)
           
            arquivo.write(linha)
    arquivo.close

    
    with open('lista_produtos.html','w') as arquivo:
        arquivo.write(str(conteudo_html))
    arquivo.close()
    
except:
    driver.quit()
    print('Erro ao salvar lista de produtos')
    quit()

print('Teste realizado com sucesso')
driver.quit()