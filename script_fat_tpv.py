import configparser
import ftplib
import os
from datetime import date


def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def ftp_acess(host, user, passwd, diretorio):
    ftp = ftplib.FTP_TLS(host, user, passwd)
    # Configurando uma conexão de dados segura, aplicando certificados de segurança
    ftp.prot_p()
    # force UTF-8 encoding
    ftp.encoding = "utf-8"
    # Difinindo diretório a ser lido
    ftp.cwd(diretorio)

    # Função para capturar o nome dos arquivos existentes
    files = ftp.nlst()

    # Função de download do arquivo para o diretorio atual
    download_file(files[0], ftp)
    # Finalizando a conexão
    ftp.quit()
    return files[0]


def create_datafile(filename, ftp):
    info_file = []
    ftp.dir("", info_file.append)
    list_info = info_file[0].split(" ")
    mes = list_info[9]
    dia = list_info[10]
    ano = date.today().year
    time = list_info[11]

    f = open(filename, "w")
    f.write("dia, mes, ano, hora \n")
    f.write(str(dia) + ", ")
    f.write(str(mes) + ", ")
    f.write(str(ano) + ", ")
    f.write(str(time))
    f.close()


def download_file(filename, ftp):
    with open(filename, "wb") as f:
        ftp.retrbinary(f"RETR {filename}", f.write)


def movend_file(filename, dest, source):
    f = open(source+filename, "r")
    file = f.read()
    f.close()

    f = open(dest+filename, "w")
    f.write(file)
    f.close()


def movendBKP_file(filename, dest, source):
    f = open(source+filename, "r")
    file = f.read()
    f.close()

    f = open(dest+"Agenda_Registrada.txt", "w")
    f.write(file)
    f.close()


def ftp_delete(host, user, passwd, filetodelete, diretorio):
    ftp = ftplib.FTP_TLS(host, user, passwd)
    # Configurando uma conexão de dados segura, aplicando certificados de segurança
    ftp.prot_p()
    # force UTF-8 encoding
    ftp.encoding = "utf-8"
    # Difinindo diretório a ser lido
    ftp.cwd(diretorio)

    # Delete file
    ftp.delete(filetodelete)

    # Encerra conexão
    ftp.quit()


def main():
    config = load_config()

    host = config['ftp']['host']
    user = config['ftp']['user']
    passwd = config['ftp']['passwd']
    source = config["path"]["source"]
    dest = config["path"]["destiny"]
    destBKP = config["path"]["destinybkp"]
    directory = config['ftp']['directory']

    filename = ftp_acess(host, user, passwd, directory)

    movendBKP_file(filename, dest, source)
    movend_file(filename, destBKP, source)
    os.remove(source+filename)

    # Depois que todos os passos foram executados com sucesso
    # Abro a conexão novamente para excluir o arquivo utilizado.
    #ftp_delete(host, user, passwd, filename)


main()
