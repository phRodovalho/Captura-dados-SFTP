import configparser
import ftplib
import os


def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def open_connection(host, user, passwd, directory, port=21):
    ftp = ftplib.FTP_TLS(host, user, passwd)
    # Configurando uma conexão de dados segura, aplicando certificados de segurança
    ftp.prot_p()
    # force UTF-8 encoding
    ftp.encoding = "utf-8"
    # Difinindo diretório a ser lido
    ftp.cwd(directory)
    return ftp


def download_allfiles(ftp, destiny):
    filename = ftp.nlst()
    for file in filename:
        with open(destiny + file, "wb") as f:
            ftp.retrbinary(f"RETR {file}", f.write)


def download_lastfile(ftp, destinybkp, destiny):
    filename = ftp.nlst()[-1]
    with open(destinybkp + filename, "wb") as f:
        ftp.retrbinary(f"RETR {filename}", f.write)
    with open(destiny + filename, "wb") as f:
        ftp.retrbinary(f"RETR {filename}", f.write)


def main():
    config = load_config()
    host = config['ftp']['host']
    user = config['ftp']['user']
    passwd = config['ftp']['passwd']
    directory = config['ftp']['directory']
    destinybkp = config['path']['destinybkp']
    destiny = config['path']['destiny']

    ftp = open_connection(host, user, passwd, directory)

    listbkp = os.listdir(destinybkp)
    if len(listbkp) == 0:  # Verifica se existe algum arquivo no diretório de backup
        download_allfiles(ftp, destinybkp)
        print("Arquivos baixados com sucesso!")
    else:
        download_lastfile(ftp, destinybkp, destiny)
        print("Arquivo baixado com sucesso!")


main()
