# Zabbix Host Management

Este repositório foi desenvolvido para facilitar a exportação, manipulação e importação de hosts no Zabbix, utilizando scripts Python e a API do Zabbix.

## Estrutura do Repositório

- **`HOSTS_SNMP.xlsx`**: Planilha que contém as informações dos hosts configurados para serem importados no Zabbix via SNMP.
- **`IMPORT_HOSTS_SNMP.py`**: Script Python responsável por importar os hosts presentes na planilha `HOSTS_SNMP.xlsx` para o Zabbix usando a API.
- **`README.md`**: Este arquivo, com informações detalhadas sobre o projeto.
- **`export001.py`**: Script Python para exportar os hosts do Zabbix em formato JSON, que posteriormente pode ser transformado em uma planilha Excel.

## Fluxo de Trabalho

### 1. Exportação de Hosts do Zabbix
1. Execute o script `export001.py` para exportar os hosts do Zabbix em formato JSON.
   ```bash
   python export001.py
   ```
2. O arquivo JSON gerado pode ser convertido em uma planilha Excel para facilitar a análise e manipulação dos dados.

### 2. Preenchimento da Planilha `HOSTS_SNMP.xlsx`
- Abra a planilha gerada a partir do arquivo JSON e extraia as informações necessárias para preencher o arquivo `HOSTS_SNMP.xlsx`.
- Certifique-se de preencher corretamente todos os campos exigidos para os hosts.

### 3. Importação de Hosts para o Zabbix
1. Execute o script `IMPORT_HOSTS_SNMP.py` para importar os hosts preenchidos na planilha `HOSTS_SNMP.xlsx` para o Zabbix.
   ```bash
   python IMPORT_HOSTS_SNMP.py
   ```
2. Verifique os logs e o Zabbix para garantir que os hosts foram importados com sucesso.

## Configuração dos Scripts

### Configuração da API do Zabbix
Certifique-se de configurar as credenciais de acesso à API do Zabbix no(s) script(s):

```python
# Exemplo de configuração
api_url = "http://seu-zabbix-url/zabbix/api_jsonrpc.php"
username = "apiadmin"
password = "Cris1570@#"
group_name = "0-GERAL-PI-LEGADO-821"
```
> **Nota:** Atualize `api_url`, `username`, `password` e `group_name` de acordo com o seu ambiente Zabbix.

### Dependências
Certifique-se de instalar todas as dependências antes de executar os scripts. Use o seguinte comando para instalar os pacotes Python necessários:

```bash
pip install -r requirements.txt
```
> Caso o arquivo `requirements.txt` não esteja presente, você pode incluir as dependências principais como `requests` e `pandas`.

## Requisitos

- Python 3.7 ou superior
- Biblioteca `requests` para integração com a API do Zabbix
- Biblioteca `pandas` para manipulação de dados em planilhas

## Exemplos de Uso

### Exportar Hosts
```bash
python export001.py
```
Resultado: Um arquivo JSON contendo os hosts exportados.

### Importar Hosts
```bash
python IMPORT_HOSTS_SNMP.py
```
Resultado: Hosts adicionados ao grupo especificado no Zabbix.

## Contribuição

1. Fork este repositório.
2. Crie um branch para suas modificações:
   ```bash
   git checkout -b minha-melhoria
   ```
3. Commit suas alterações:
   ```bash
   git commit -m "Minha melhoria"
   ```
4. Envie para o branch principal:
   ```bash
   git push origin minha-melhoria
   ```
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contato

Para mais informações ou suporte, entre em contato:

- **E-mail:** suporte@seu-email.com
- **GitHub:** [SeuPerfil](https://github.com/SeuPerfil)

---

<p align="center">Feito com ❤þ para gerenciar seus hosts no Zabbix de forma eficiente!</p>

