# Gerador Automático de Relatórios de Campanhas

Projeto de automação que conecta à API do Google Ads, gera relatórios de campanhas em Excel e envia por e-mail automaticamente.

## Funcionalidades

- Busca de dados da API Google Ads via parâmetros configuráveis
- Geração de relatório em Excel
- Envio automático por e-mail
- Agendamento de execução (ex: diário)
- Configuração via arquivo YAML
- Logs automáticos das operações

## Como usar

1. Clone o repositório
2. Instale as dependências
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Configure o arquivo `config.yaml` com suas credenciais e parâmetros de relatório.
```yaml
    google_ads:
  developer_token: "SUA_DEVELOPER_TOKEN"
  client_id: "SEU_CLIENT_ID"
  client_secret: "SEU_CLIENT_SECRET"
  refresh_token: "SEU_REFRESH_TOKEN"
  customer_id: "SUA_CUSTOMER_ID"
report:
  start_date: "2024-06-01"
  end_date: "2024-06-15"
  metrics:
    - campaign.id
    - campaign.name
    - metrics.impressions
    - metrics.clicks
    - metrics.cost_micros
email:
  enabled: true
  smtp_server: smtp.gmail.com
  smtp_port: 587
  username: seu_email@gmail.com
  password: sua_senha_de_app
  from: seu_email@gmail.com
  to: destinatario@gmail.com
schedule_minutes: 1440 # 1 vez por dia

```
4. Execute o script:
    ```bash
    python reporter.py
    ```

## Observações

- As credenciais do Google Ads podem ser obtidas em [Google Cloud Console](https://console.cloud.google.com/).
- Use senhas de app para o e-mail.
- Logs em `logs/reporter.log`.
- Relatórios gerados na pasta `reports/`.

## Referências

- [Google Ads Python Client](https://developers.google.com/google-ads/api/docs/client-libs/python)
- [Automação de e-mail com Python](https://realpython.com/python-send-email/)
- [Agendando tarefas com schedule](https://realpython.com/python-schedule/)
