import pandas as pd
import yaml
import logging
import time
import schedule
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Import Google Ads
try:
    from google.ads.googleads.client import GoogleAdsClient
    GOOGLE_ADS_READY = True
except ImportError:
    GOOGLE_ADS_READY = False

# --- Configuração de logging ---
logging.basicConfig(
    filename='logs/reporter.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# --- Carregar configuração ---
def load_config(path='config.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

config = load_config()

def fetch_google_ads_data():
    if not GOOGLE_ADS_READY:
        logging.error("google-ads não está instalado.")
        return pd.DataFrame() # vazio

    try:
        credentials = {
            "developer_token": config['google_ads']['developer_token'],
            "client_id": config['google_ads']['client_id'],
            "client_secret": config['google_ads']['client_secret'],
            "refresh_token": config['google_ads']['refresh_token'],
            "login_customer_id": config['google_ads'].get('login_customer_id', None)
        }
        customer_id = config['google_ads']['customer_id']

        # Cria arquivo temporário de config do Google Ads
        yaml_content = f"""
developer_token: "{credentials['developer_token']}"
client_id: "{credentials['client_id']}"
client_secret: "{credentials['client_secret']}"
refresh_token: "{credentials['refresh_token']}"
"""
        temp_conf_path = "google-ads.yaml"
        with open(temp_conf_path, "w") as f:
            f.write(yaml_content)

        ga_client = GoogleAdsClient.load_from_storage(temp_conf_path)

        query = f"""
            SELECT {', '.join(config['report']['metrics'])}
            FROM campaign
            WHERE segments.date BETWEEN '{config['report']['start_date']}' AND '{config['report']['end_date']}'
            ORDER BY campaign.id
        """

        service = ga_client.get_service("GoogleAdsService")
        response = service.search(customer_id=customer_id, query=query)
        rows = []
        for row in response:
            rows.append({k: getattr(row, k.split(".")[1]) for k in config['report']['metrics']})
        if os.path.exists(temp_conf_path):
            os.remove(temp_conf_path)
        return pd.DataFrame(rows)
    except Exception as e:
        logging.error(f"Erro ao buscar dados do Google Ads: {e}")
        return pd.DataFrame()

def generate_report(df):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    logging.info(f"Relatório gerado: {filename}")
    return filename

def send_email(subject, body, attachment):
    mail_conf = config['email']
    msg = MIMEMultipart()
    msg['From'] = mail_conf['from']
    msg['To'] = mail_conf['to']
    msg['Subject'] = subject

    # Corpo do e-mail
    msg.attach(MIMEBase('text', 'plain'))
    msg.attach(MIMEBase('text', 'plain'))
    msg.attach(MIMEBase('application', 'octet-stream'))

    # Anexo
    with open(attachment, 'rb') as f:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')
        msg.attach(part)
    try:
        server = smtplib.SMTP(mail_conf['smtp_server'], mail_conf['smtp_port'])
        server.starttls()
        server.login(mail_conf['username'], mail_conf['password'])
        server.sendmail(mail_conf['from'], mail_conf['to'], msg.as_string())
        server.quit()
        logging.info("E-mail com relatório enviado.")
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail: {e}")

def workflow():
    print("Executando rotina de relatório de campanhas...")
    df = fetch_google_ads_data()
    if df.empty:
        logging.warning("Sem dados retornados ou erro na API Google Ads.")
        return
    filename = generate_report(df)
    if config['email']['enabled']:
        send_email(
            subject="Relatório Diário de Campanhas",
            body="Segue em anexo o relatório das campanhas.",
            attachment=filename
        )

if __name__ == "__main__":
    schedule.every(config.get("schedule_minutes", 1440)).minutes.do(workflow)
    print("Agendador de relatório iniciado!")
    while True:
        schedule.run_pending()
        time.sleep(10)
