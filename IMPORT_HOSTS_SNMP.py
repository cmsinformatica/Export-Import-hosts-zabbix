# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd  # IMPORTANDO PANDAS PARA LEITURA DE ARQUIVOS EXCEL
import os  # IMPORTANDO OS PARA GERENCIAR CAMINHOS DE ARQUIVOS

# CONFIGURAÇÕES DO ZABBIX
ZABBIX_URL = "http://Seu IP/zabbix/api_jsonrpc.php"
AUTH_TOKEN = "Seu token"

def create_host(auth_token, host_ip, host_name, display_name, group_ids, template_ids, snmp_community):
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        'jsonrpc': '2.0',
        'method': 'host.create',
        'params': {
            'host': host_name,
            'name': display_name,
            'interfaces': [
                {
                    'type': 2,  # 2 PARA SNMP
                    'main': 1,
                    'useip': 1,
                    'ip': host_ip,
                    'dns': '',  # VAZIO QUANDO SNMP USA IP
                    'port': '161',  # PORTA PADRÃO SNMP
                    'details': {
                        'version': 2,  # VERSÃO SNMP 2
                        'bulk': 0,  # DEFININDO BULK PARA 0
                        'community': snmp_community  # COMUNIDADE SNMP DO EXCEL
                    }
                }
            ],
            'groups': [{'groupid': gid} for gid in group_ids],
            'templates': [{'templateid': tid} for tid in template_ids]
        },
        'auth': auth_token,
        'id': 1
    }

    response = requests.post(ZABBIX_URL, headers=headers, data=json.dumps(payload))
    
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")

    if response.headers['Content-Type'].startswith('application/json'):
        try:
            result = response.json()
            return result.get('result')
        except json.JSONDecodeError as e:
            print(f"Erro de decodificação JSON: {e}")
            return None
    else:
        print("Recebendo uma resposta que não é JSON. Verifique a URL e as credenciais.")
        return None

def main():
    # OBTENHA O DIRETÓRIO ATUAL ONDE O SCRIPT ESTÁ SENDO EXECUTADO
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # CONSTRUA O CAMINHO DO ARQUIVO EXCEL
    excel_file = os.path.join(script_dir, 'HOSTS_SNMP.xlsx')
    
    try:
        df = pd.read_excel(excel_file, dtype=str)  # FORÇA LEITURA COMO STRING PARA EVITAR FLOAT
        
        for index, row in df.iterrows():
            host_ip = row['ip']
            host_name = row['host_name']
            display_name = row['display_name']
            
            # GARANTIR QUE group_ids E template_ids SEJAM STRINGS E SEPARAR POR VÍrGULA CORRETAMENTE
            group_ids = [int(gid.strip()) for gid in row['group_ids'].replace('.', ',').split(',') if pd.notna(gid) and gid.strip().isdigit()]
            template_ids = [int(tid.strip()) for tid in row['template_ids'].replace('.', ',').split(',') if pd.notna(tid) and tid.strip().isdigit()]
            
            snmp_community = row['comunity_name']  # COMUNIDADE SNMP DO EXCEL
            
            # CRIA O HOST
            result = create_host(AUTH_TOKEN, host_ip, host_name, display_name, group_ids, template_ids, snmp_community)
            
            if result:
                host_id = result['hostids'][0]
                print(f"Host criado com sucesso. ID do Host: {host_id}")
            else:
                print(f'Falha ao criar host para o IP: {host_ip}')
    except FileNotFoundError:
        print(f"Arquivo {excel_file} não encontrado.")
    except KeyError as e:
        print(f"Coluna necessária ausente no Excel: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        pass

if __name__ == "__main__":
    main()

