# Automatic Campaign Report Generator

Automation that connects to the Google Ads API, generates campaign reports in Excel, and emails them automatically on a schedule.

## Features
- Pulls data from the Google Ads API via configurable parameters
- Generates an Excel report
- Sends it automatically by email
- Scheduled runs (e.g. daily)
- YAML-based configuration
- Automatic operation logs

## Usage
```bash
git clone https://github.com/ThzxD1/campaign_reporter.git
cd campaign_reporter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python reporter.py
```

## Example Configuration (`config.yaml`)
```yaml
google_ads:
  developer_token: "YOUR_DEVELOPER_TOKEN"
  client_id: "YOUR_CLIENT_ID"
  client_secret: "YOUR_CLIENT_SECRET"
  refresh_token: "YOUR_REFRESH_TOKEN"
  customer_id: "YOUR_CUSTOMER_ID"
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
  username: your_email@gmail.com
  password: your_app_password
  from: your_email@gmail.com
  to: recipient@gmail.com
schedule_minutes: 1440   # once per day
```

## Notes
- Google Ads credentials can be obtained in the Google Cloud Console.
- Use app passwords for email.
- Logs are saved in `logs/reporter.log`; reports in the `reports/` folder.
