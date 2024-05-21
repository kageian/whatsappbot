import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class Wppbot():
    def __init__(self):
        self.servicos = Service(ChromeDriverManager().install())
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.navegador = webdriver.Chrome(service=self.servicos, options=self.options)
        self.lista_numeros = []

    # Espera do QR code
    async def qrcode(self):
        self.navegador.get('https://web.whatsapp.com')
        while len(self.navegador.find_elements('id', 'side')) < 1:
            print('Esperando QR Code')
            await asyncio.sleep(5)
        await asyncio.sleep(10)

    # Analisando se há notificação
    async def noti(self):
        print(f'Lista atual: {self.lista_numeros}')
        await asyncio.sleep(0.5)
        while True:
            self.notificar = self.navegador.find_elements(By.XPATH, "//div[@class='_ahlk']")
            if len(self.notificar) > 0:
                self.navegador.find_elements(By.XPATH, "//div[@class='_ahlk']")[0].click()
                return await self.verificador()
            else:
                print('Aguardando mensagem')
                await asyncio.sleep(1)

    # Salva o numero do cliente que mandou mensagem em uma array
    async def verificador(self):
        self.numero = self.navegador.find_elements(By.XPATH, "//div[@class='_aou8 _aj_h']")[-1].text
        print(F'numero que mandou mensagem {self.numero}')

        # Verifica se o número ja esta em uma array, se não estiver ele coloca e manda a mensagem de boas vindas.
        if self.numero not in self.lista_numeros:
            self.lista_numeros.append(self.numero)
            self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys("""Mensagem de boas vindas""")
            self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(Keys.ENTER)
            self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(Keys.ESCAPE)
            print(f'numero {self.numero} adcionado na lista dos numeros')
            return await self.noti()

        else:
            await asyncio.sleep(0.5)
            return await self.opcoes()

    # Opções que podem variar de 1 até 5 ou mais depende do que você quiser
    async def opcoes(self):

        await asyncio.sleep(0.5)
        mensagem = self.navegador.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]")[-1].text
        ultima1 = mensagem.split()
        ultima = ultima1[0]
        print(f'Mensagem {ultima} adcionada')
        await asyncio.sleep(0.5)
        while True:
            if ultima == '1':
                self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(
                    '')
                self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(Keys.ENTER)
                break
            elif ultima == '2':
                self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(
                    '')
                self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(Keys.ENTER)
                break
            elif ultima == '3':
                self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(
                    '')
                self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(Keys.ENTER)
                break
            elif ultima == '4':
                self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(
                    '')
                self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(Keys.ENTER)
                break
            else:
                self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(
                    'Opção invalida')
                self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(Keys.ENTER)
                self.numero = self.navegador.find_elements(By.XPATH, "//div[@class='_aou8 _aj_h']")[1].text
                self.lista_numeros.remove(self.numero)
                return await self.verificador()

        self.numero = self.navegador.find_elements(By.XPATH, "//div[@class='_aou8 _aj_h']")[-1].text
        self.lista_numeros.remove(self.numero)
        self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(
            'Encerrar atendimento.')
        self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(Keys.ENTER)
        print(f'Numero {self.numero} removido da lista.')
        self.navegador.find_element(By.XPATH, "//div[@class='_ak1l']").send_keys(Keys.ESCAPE)
        return await self.noti()


async def main():
    bot = Wppbot()
    await bot.qrcode()
    await bot.noti()
    await bot.verificador()
    await bot.opcoes()


if __name__ == "__main__":
    asyncio.run(main())
