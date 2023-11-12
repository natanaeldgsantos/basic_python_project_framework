
import os
import subprocess
import platform
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PythonProject(object):
    """ Responsável por criar uma estrutura de pastas e arquivos básicos
        pra um projeto Python
    """

    def __init__(self, nome_projeto: str):
        self.nome_projeto = nome_projeto
        self.sistema_operacional = platform.system()

        # O caminho até os arquivos de configuração mudam entre Window w Linux no venv.
        self.scripts_folder = 'Scripts' if self.sistema_operacional == "Windows" else "bin"


    def validar_sistema_operacional(self, sistema_operacional: str) -> str:
        """ Verifica, valida e retorna o sistema operacional 
            para que o script funcione considere apenas sistemas Linux e Windows
        """

        if sistema_operacional in ['Linux', 'Windows']:
            logging.info(f'> Sistema operacional suportado: <"{sistema_operacional}"> ')
            return True
        else:
            logging.error(f'> Sistema operacional não suportado: <"{sistema_operacional}"> ')
            return False

         
    def criar_pasta(self, path:str) -> None:
        """ Gera pastas no local especificado """

        try:
            os.makedirs(path)
            logging.info(f'Pasta criada em : {path}')
        except FileExistsError:
            logging.warning(f"Pasta já existe no caminho: {path}")


    def cria_arquivo(self, path:str, conteudo='') -> None:
        """ Gera e grava linhas no arquivo criado """

        with open (path, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
            logging.info(f'Arquivo criado: {path}')


    def criar_venv(self, nome_venv= 'venv') -> None:
        """ Instala e ativa o ambiente virtual (venv) """

        # 01. Cria ambiente virtual
        subprocess.run(['python', '-m', 'venv', nome_venv])

        logging.info(f'> Ambiente virtual gerado com sucesso: {nome_venv}')        

        # 02. Ativa o sistema operacional 
        if self.sistema_operacional == "Windows":

            ativar_venv = os.path.join(os.getcwd(), 'venv', 'Scripts', 'activate')        
            subprocess.run(f"call {ativar_venv}", shell=True)
            logging.info(f'> Ambiente virtual ativado com sucesso: {nome_venv}')

        elif self.sistema_operacional == 'Linux':

            ativar_venv = os.path.join(os.getcwd(), 'venv', 'bin', 'activate')
            subprocess.run(f"source {ativar_venv}", shell=True)
            logging.info(f'> Ambiente virtual ativado com sucesso: {nome_venv}')
        
    
    def instalar_bibliotecas(self, venv) -> None:
        """ Instala bibliotecas básicas/iniciais para um projeto padrão """

        # Conjunto de bibliotecas padrão
        bibliotecas = ['pandas', 'pytest']        

        logging.info('> Atualizando a versão do pip')
        subprocess.run([os.path.join(venv, self.scripts_folder, 'python'), '-m', 'pip', 'install', '--upgrade', 'pip'])

        logging.info('> Instalando bibliotecas:')
        subprocess.run([os.path.join(venv, self.scripts_folder, 'pip'), 'install'] + bibliotecas)

        logging.info(f'Bibliotecas instaladas: {", ".join(bibliotecas)}')


    def criar_requirements_file(self, venv, output_file= "requirements.txt"):
        """ Gera arquivo de requirements.txt """

        subprocess.run([os.path.join(venv, self.scripts_folder, 'pip'), 'freeze', '>', output_file], shell= True)

        logging.info(f'Arquivo de requirements gerado com sucesso: {output_file}')


    def criar_projeto(self) -> None:
        """ Método principal, orquesta e executa toda a lógica da solução """    

        logging.info(f'Iniciando a construção do projeto {self.nome_projeto}')
        logging.info(f'Sistema operacional:  {self.sistema_operacional}')

        # Verifica se o sistema operacional(OS) é válido

        is_os_valid = self.validar_sistema_operacional(self.sistema_operacional)

        if not is_os_valid:
            raise ValueError('Sistema Operacional não suportado')

        self.criar_pasta(self.nome_projeto)
        os.chdir(self.nome_projeto)    

        # Criar pastas
        self.criar_pasta(self.nome_projeto)
        self.criar_pasta("docs")
        self.criar_pasta("tests")

        # Cria arquivos
        self.cria_arquivo(f"{self.nome_projeto}/__init__.py", "# main package" )
        self.cria_arquivo(f"{self.nome_projeto}/main.py", "print('Olá Mundo')")    

        self.cria_arquivo("tests/test_base.py", "# testes unitários \nimport pytest" )
        self.cria_arquivo("tests/__init__.py", "# pytest package" )    

        self.cria_arquivo('README.md', f"# Documentação do Projeto {self.nome_projeto}")
        self.cria_arquivo('.gitignore', 'venv/*')    

        # Cria ambiente virtual e instala as bibliotecas
        self.criar_venv()
        self.instalar_bibliotecas('venv')

        self.criar_requirements_file('venv')


if __name__ == "__main__":
    nome_do_projeto = input('Digite o nome do projeto: ')

    PythonProject(nome_do_projeto).criar_projeto()

    print('Projeto criado com Sucesso!')
