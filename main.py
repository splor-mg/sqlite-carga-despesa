import pandas as pd
import glob
import os
import sqlite3

DB_NAME = 'database/dadosmg.db'
DATASETS_DIR = 'despesa/'
DATASET_DIR = 'datasets/'
DATA_DIR = 'data/'
DATA_PATH = DATASET_DIR + DATASETS_DIR + DATA_DIR

# obtem lista de paths para arquivos CSV localizados no caminho DATA_PATH
file_paths = [i.replace('\\', '/') for i in list(glob.iglob(f'{DATA_PATH}*.csv*'))]

# paths de bases csv que sao separadas por anos
file_paths_desp = [x for x in file_paths if "dm_empenho_desp_" in x]
file_paths_ft = [x for x in file_paths if "ft_despesa_" in x]

# paths de bases csv que não são separadas por anos
file_paths = list(set(file_paths) - set(file_paths_desp) - set(file_paths_ft))

# True Dropa todas as tabelas atuais da database
DROP_TABLES = True


def drop_tables(con=None):

    cur = con.cursor()
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    res = cur.fetchall()

    if res:
        for table_name in res:
            con.execute(f"""DROP TABLE '{table_name[0]}' """)
            print(f"Tabela {table_name} apagada.")
    else:
        print(f"Não há tabelas em {DB_NAME}")


def tables_from_csv(file_paths, con):

    for file in file_paths:
        head, tail = os.path.split(file)
        table_name = tail.split('.')[0]

        df = pd.read_csv(file, delimiter=';', decimal='.')

        # if_exists{‘fail’, ‘replace’, ‘append’}, default ‘fail’
        df.to_sql(table_name, con, if_exists='replace', index=False)
        print(f"Arquivo {file} carregado para tabela {table_name}")

    print('-------------------------------------------------------\n')

def append_from_csv(file_paths_append, tbl_agg_name):
    df_agg = pd.DataFrame()
    num_linhas = 0
    exec_error = False
    files_error = []

    for file in file_paths_append:
        _, tail = os.path.split(file)
        table_name, file_extension = os.path.splitext(tail)
        print(f'Lendo:', file)

        df = pd.read_csv(file, delimiter=';', decimal='.')

        try:
            df.to_sql(tbl_agg_name, con, if_exists='append', index=False)  # if_exists{‘fail’, ‘replace’, ‘append’}, default ‘fail’
            print(f"Arquivo {file} concatenado na tabela {tbl_agg_name}\n")
            num_linhas += len(df)
        except:
            print(f"ERRO: Arquivo {file} está vazio ou contém schema divergente dos demais.\n")
            exec_error = True
            files_error.append(file)

    print('-------------------------------------------------------')

    print('Total de linhas das tabelas lidas:', num_linhas)

    # alerta para falha no carregamento de arquivos. Arquivos somente com cabeçalhos geram esse erro.
    if exec_error:
        print(f"ATENÇÃO! os seguintes arquivos não foram carregados para a base de dados:")
        print(files_error, sep='\n')
        print('\n\n')


def show_tables(con=None):

    cur = con.cursor()
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    res = cur.fetchall()

    if res:
        print(res)
    else:
        print(f"Não há tabelas na database {DB_NAME}")


if __name__ == '__main__':
    con = sqlite3.connect(DB_NAME) #Cria se não existe e se conecta à base de dados
    cur = con.cursor() # Cursor para executar queries. Reutilizar cursor otimiza consultas

    show_tables(con)

    if DROP_TABLES:
        drop_tables(con)

    tables_from_csv(file_paths, con)

    append_from_csv(file_paths_desp, 'dm_empenho_desp')
    append_from_csv(file_paths_ft, 'ft_despesa')

    con.commit()
    con.close()

