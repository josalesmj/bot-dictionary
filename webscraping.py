# Para instalar automaticamente o chromedriver
from webdriver_manager.chrome import ChromeDriverManager

#driver do selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

#para modificar as opcoes de webdriver em chrome
from selenium.webdriver.chrome.options import Options

#para definir o time de busca do elemento
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException


class Webscraping:
  
  def __init__(self):
    options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4754.102 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    
    # Não abrir o browser
    options.add_argument("headless")
    
    # Abrir o browser maximizado
    #options.add_argument("--start-maximized")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level-3")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    #parametros para omitir o inicio do chromedriver
    exp_opt = [
      'enable-automation',
      'ignore-certificate-errors',
      'enable-logging'
    ]
    options.add_experimental_option("excludeSwitches", exp_opt)

    #parametros que definem as preferencias no chromedriver    
    prefs = {
      "profile.default_content_setting_values.notifications": 2,
      "intl.accept_languagens": ["pt-BR", "BR"],
      "crendentials_enable_service": False
    }
    options.add_experimental_option("prefs", prefs)
    
    try:
      s = Service(ChromeDriverManager(
          path="./chromedriver", log_level=0).install())
    finally:
      try:
        self.driver = webdriver.Chrome(service=s, options=options)
      except Exception as e:
        if isinstance(e, WebDriverException):
          self.driver = None
        print(e)   

  def GetWordMeans(self, word):
    url = "https://dictionary.cambridge.org/pt/dicionario/ingles/"
    self.driver.get(url + word)
    
    #####################################################################################
    #Caso a box de políticas de cookie estiver atrapalhando, descomentar as linhas abaixo
    #time.sleep(3)
    #driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    #time.sleep(2)
    #####################################################################################
    
    means = []
    
    means_box = self.driver.find_elements(By.XPATH, value=f"//div[@class='def ddef_d db']")
    if (len(means_box) > 0):
      for mean in means_box:
        means.append(mean.text)
      
    elements = self.driver.find_elements(By.XPATH, value=f"//source[@type='audio/ogg']")
    audioLink = elements[1].get_attribute("src")
    
    examples_list = []
    try:
      examples_box = self.driver.find_element(By.XPATH, value=f"//div[@class='def-body ddef_b']")
      examples_list = self._getListOfStrFromWebElement('div', 'examp dexamp', examples_box)
    except NoSuchElementException:
        print('Element not found')
      
    if len(examples_list) < 1:
      try:
        examples_box = self.driver.find_element(By.XPATH, value=f"//div[@class='daccord']")
        examples_list = self._getListOfStrFromWebElement('li', 'eg dexamp hax', examples_box)
      except NoSuchElementException:
        print('Element not found')  
      
    if __name__ != '__main__':
      return means[0:3], audioLink, examples_list[0:4]
    print(f'Palavra: {means}')

  def DestructorWebDriver(self):
    self.driver.quit()
    
  def _getListOfStrFromWebElement(self, htmlElement, className, WebElement):
    listOfStr = []
    for element in WebElement.find_elements(By.XPATH, value=f".//{htmlElement}[@class='{className}']"):
      listOfStr.append(element.text)
    return listOfStr

if __name__ == '__main__':
  wp = Webscraping()
  if not wp.driver == None:
    word = input("Digite a palavra: ")
    wp.GetWordMeans(word)
    wp.DestructorWebDriver()
  else:
    print('Something went wrong during WebDriver loading.')
