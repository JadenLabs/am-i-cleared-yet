# am-i-cleared-yet

Monitors the SLC Airport badging cleared list and sends a Discord notification when your badge number appears.

## What it does

Every 6 hours (08:00, 14:00, 20:00, 02:00), the script:
1. Downloads the current cleared PDF from the airport badging office
2. Searches for your badge number(s) in the table
3. Sends a Discord embed notification if a match is found
4. Logs all results to `logs/am-i-cleared-yet.log`

## Setup

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.yml`:

```yaml
url: https://slcairport.com/badging/assets/pdfDocuments/cleared.pdf
badge_numbers:
  - "your_badge_number"
user_mention: <@YOUR_DISCORD_USER_ID>
webhook_url: https://discord.com/api/webhooks/...
```

To find your Discord user ID: enable Developer Mode in Discord settings, then right-click your username and select **Copy User ID**.

## Running

```bash
python main.py
```

The process runs continuously and checks on schedule. Keep it alive with a process manager like `nssm` (Windows service) or just leave the terminal open.

## Logs

Results are written to `logs/am-i-cleared-yet.log` and also printed to stdout.
