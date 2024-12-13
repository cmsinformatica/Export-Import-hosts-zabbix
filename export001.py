import requests
import json

# Configurações do Zabbix
zabbix_url = "http://SEU IP/zabbix/api_jsonrpc.php"  # Substitua pela URL do seu Zabbix
headers = {"Content-Type": "application/json"}
zabbix_user = "SEU USUARIO"  # Usuário atualizado
zabbix_password = "SUA SENHA"  # Senha atualizada
group_name = "NOME DO SEU GRUPO"  # Grupo informado

def authenticate():
    """Autentica no Zabbix e retorna o token."""
    auth_payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": zabbix_user,
            "password": zabbix_password,
        },
        "id": 1,
    }
    response = requests.post(zabbix_url, json=auth_payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    if "error" in result:
        raise ValueError(f"Erro de autenticação: {result['error']}")
    return result["result"]

def get_group_id(auth_token, group_name):
    """Obtém o ID do grupo com base no nome."""
    group_payload = {
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "filter": {"name": group_name},
            "output": "extend",
        },
        "auth": auth_token,
        "id": 2,
    }
    response = requests.post(zabbix_url, json=group_payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    if not result["result"]:
        raise ValueError(f"Grupo '{group_name}' não encontrado.")
    return result["result"][0]["groupid"]

def get_hosts(auth_token, group_id):
    """Obtém os hosts do grupo especificado."""
    hosts_payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "groupids": group_id,
            "output": "extend",
            "selectInterfaces": "extend",
            "selectMacros": "extend",
            "selectTags": "extend",
            "selectInventory": "extend",
            "selectGroups": "extend",
            "selectParentTemplates": "extend",
        },
        "auth": auth_token,
        "id": 3,
    }
    response = requests.post(zabbix_url, json=hosts_payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    if "error" in result:
        raise ValueError(f"Erro ao obter hosts: {result['error']}")
    return result["result"]

def export_to_json(data, filename):
    """Exporta os dados para um arquivo JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Hosts exportados com sucesso para {filename}")

def main():
    try:
        auth_token = authenticate()
        group_id = get_group_id(auth_token, group_name)
        hosts = get_hosts(auth_token, group_id)
        export_to_json(hosts, "hosts_zabbix_export.json")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
