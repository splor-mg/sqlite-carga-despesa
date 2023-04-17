# SQLite

## Instalação no Windows

Após clonar o projeto, seguir as etapas a seguir.


### Criar ambiente virtual do projeto
```python
cd diretorio/do/projeto
python -m venv venv
```

### Ativar ambiente virtual do projeto

Linha de comando no Windows:
```cmd
cd diretorio/do/projeto
venv\Scripts\activate
```

Git bash:
```gitbash
cd diretorio/do/projeto
source venv\Scripts\activate
```

### Instalar requerimentos
```python
pip install -r requirements.txt
```

### Instalar Jupyter Notebook (opcional)
```python
pip install notebook
```

## Execução no Python

### Ativar o ambiente virtual

Linha de comando no Windows:
```cmd
cd diretorio/do/projeto
venv\Scripts\activate
```

Git bash:
```gitbash
cd diretorio/do/projeto
source venv\Scripts\activate
```

### Executar makefile

Baixar arquivos tar.gz do portal dadosmg:  
```python
make download
```

Executar script de carga de dados:  
```python
make run
```

Fazer download dos arquivos e executar o script de carga de dados:
```python
make all
```

## Execução no Jupyter Notebook

Ativar o ambiente virtual:
```gitbash
cd diretorio/do/projeto
source venv\Scripts\activate
```

Baixar os arquivos csv.gz do portal [dadosmg](https://dados.mg.gov.br/dataset/despesa), salvá-los na pasta \datasets e extrair todos os arquivos csv. Após isso abrir o notebook 'dadosmg_basics.ipynb' no jupyter e executar.  

**NOTA**: Durante os testes realizados o kernel do Jupyter se mostrou instável, não conseguindo importar os dados corretamente e reiniciando durante o processo. Logo é recomendado utilizá-lo para consultas e análises, mas no momento não mais para realizar as cargas de dados. O arquivo 'dadosmg_basics.ipynb' contém snippets de manipulações básicas utilizando o DuckDB em python.


## Visualização de Dados

A ferramenta open source [DB Browser for SQLite](https://sqlitebrowser.org/) pode ser utilizada para visualizar a base de dados do SQLite.

![imagem](images/db-browser-sqlite-home.png)
