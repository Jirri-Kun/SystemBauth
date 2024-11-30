#!/usr/bin/env python3

# by Jirri / https://github.com/Jirri-Kun
# Yo photty haha

from impacket.smbconnection import SMBConnection
from impacket.examples.utils import parse_target
from impacket.examples.smbclient import MiniImpacketShell 
import argparse 
import sys  
import os
import time
import termios
import socket
from tabulate import tabulate 

class SMBclient:
    def __init__(self , domain , username , password , address, port, connect):
        
        self.domain = domain
        self.username = username
        self.password = password
        self.address = address
        self.port = port or 445
        self.connect = connect
        self.resources = None

        self.share_netname = []  
        self.share_remark = []   
        self.share_type = []    
    
    def connect_to_server(self):
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            resultado = sock.connect_ex((self.address, self.port))

            if resultado == 0:
                self.conn = SMBConnection(self.address , self.address, sess_port=self.port) 
                self.conn.login(self.username , self.password , self.domain)
                print(f"[+] Conectado exitosamente a: {self.address}\n")
                self.list_shares()
            else:
                print(f"[!] No se pudo conectar al servidor smb: {self.address}")
                sys.exit(1)
        except Exception as e:
            print(f"[!] Error al entablar la conexion {e}")
            sys.exit(1)
        finally:
            sock.close()

    def list_shares(self):
        
        type_mapping = {
            2147483648: "Disco",
            0x00000000: "Disco",
            0x00000001: "Impresora",
            0x00000002: "Dispositivo de comunicación",
            0x00000003: "Directorio especial",
            2147483651: "IPC",
        }

        try:

            self.share_netname.clear()  
            self.share_remark.clear()
            self.share_type.clear()

            shares = self.conn.listShares() 
            
            for share in shares:
                self.share_netname.append(share['shi1_netname'].rstrip('\x00'))
                self.share_remark.append(share['shi1_remark'])
                self.share_type.append(type_mapping.get(share['shi1_type'], "Desconocido"))
            
        except Exception as b:
            print(f"[!] Error al en listar los recursos {b}")
            sys.exit(1)

    def select_shares(self):
        
        print("")
        while True:
            self.connect = input("Recurso a seleccionar --> ")
            print("\033[A\033[K", end="")

            if self.connect in self.share_netname:
                os.system("clear")
                self.connect_to_share()
                break
            else:
                try:
                    sys.stdout.write("\033[?25l")
                    sys.stdout.flush()
                    os.system('stty -echo -icanon eof undef')
                    print("[!] Error recurso no existente")
                    time.sleep(1)
                finally:
                    termios.tcflush(sys.stdin, termios.TCIFLUSH)
                    os.system('stty sane')
                    print("\033[A\033[K", end="")
                    sys.stdout.write("\033[?25h")
                    sys.stdout.flush()
    
    def connect_to_share(self): 

        shell = MiniImpacketShell(self.conn)
        is_active = shell.onecmd(f"use {self.connect}")

        if is_active is False:
            print("[!] Recurso no encontrado")
            sys.exit(1)

        os.system("clear")
        shell.cmdloop()

    def tabulate_data(self): 
 
        headers = ["Sharename", "Comment", "Type"]

        a = self.share_netname
        b = self.share_remark
        c = self.share_type
        
        data = list(zip(a, b, c))

        print(tabulate(data, headers=headers, tablefmt="heavy_outline"))


def tab_continue(tab):
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    nothing = input(f"\n{tab}\n")
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def parse_arguments():
    parser = argparse.ArgumentParser(add_help=True, description="Cliente de implementación SMB")
    parser.add_argument('-t', '--target', action="store", help="[[domain/]username[:password]@]<targetName or address>")
    parser.add_argument('-p', '--port', action="store", type=int , help="[445 // 139]")
    parser.add_argument('-sr', '--shared_resources', action="store_true", help="Visualizacion de recursos compartidos.")
    parser.add_argument('-ct', '--connect', nargs='?', const=True , help="Conexion a un recurso en especifico.")
    args = parser.parse_args() 
    return parser, args
    
def main():
    parser, args = parse_arguments()

    if len(sys.argv) == 1: 
        parser.print_help()
        sys.exit(1) 

    domain, username, password, address = parse_target(args.target)
    smb_client = SMBclient(domain, username, password, address, args.port, args.connect) 
    
    if len(sys.argv) == 3 and '-t' in sys.argv and args.target:
        smb_client.connect_to_server()
        print("[+] Credenciales validas en el servidor")
    else:
        smb_client.connect_to_server()
    
    if args.shared_resources:

        smb_client.tabulate_data() 

        if args.connect:

            if isinstance(args.connect, str): 

                tab_continue("[!] Presiona enter para entablar la conexion")
                smb_client.connect_to_share()

            elif args.connect is True: 

                smb_client.select_shares()

    elif args.connect:

        if isinstance(args.connect, str): 

            smb_client.connect_to_share()

        elif args.connect is True: 

            smb_client.tabulate_data()
            smb_client.select_shares()

if __name__ == '__main__':
    try:
        print("")
        main()
    except KeyboardInterrupt:
        print("")
        print("[!] Script finalizado")
        

