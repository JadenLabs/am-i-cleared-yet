import requests
import pdfplumber
import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.blocking import BlockingScheduler
from utils import Config, Details, notify

config = Config.from_yaml("config.yml")

CLIENT_HEADERS = {"User-Agent": "am-i-cleared-yet/1.0"}

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/am-i-cleared-yet.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def find_badge_numbers(pdf_path: str, badge_numbers: list[str]) -> list[Details]:
    matches = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue

            for row in table:
                if not row or len(row) < 4:
                    continue

                badge_cell = (row[2] or "").strip()
                if badge_cell in badge_numbers:
                    matches.append(
                        Details(
                            sponsor=row[0],
                            company=row[1],
                            badge_number=row[2],
                            notify_date=row[3],
                        )
                    )

    return matches


def build_file_name() -> str:
    fmt = "%Y-%m-%d"
    return f"cleared-{datetime.now().strftime(fmt)}.pdf"


def get_cleared_pdf(pdf_url: str) -> str:
    res = requests.get(headers=CLIENT_HEADERS, url=pdf_url)
    res.raise_for_status()

    file_name = build_file_name()
    with open(file_name, "wb") as f:
        f.write(res.content)

    return file_name


def run_check():
    log.info("Starting badge check")
    try:
        pdf_path = get_cleared_pdf(config.url)
        results = find_badge_numbers(pdf_path, config.badge_numbers)

        if results:
            log.info(f"Found {len(results)} badge(s) in cleared list")
            for result in results:
                log.info(f"Match: {result}")
                notify(result, config.user_mention, config.webhook_url)
        else:
            log.info("No badge numbers found in cleared list")
    except Exception as e:
        log.error(f"Check failed: {e}")


if __name__ == "__main__":
    run_check()  # Run immediately on startup

    scheduler = BlockingScheduler(timezone=ZoneInfo("America/Denver"))
    for hour, minute in ((6, 0), (7, 0), (7, 10), (8, 0)):
        scheduler.add_job(run_check, "cron", hour=hour, minute=minute)

    log.info("Scheduler started — checks at 06:00, 07:00, 07:10, 08:00 America/Denver")
    scheduler.start()
