"""
Telegram bot for sending SEO reports and alerts.
Bot name: SEO Reports Bot
"""
from typing import List, Dict
from pathlib import Path
from telegram import Bot
from telegram.constants import ParseMode
from src.config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TelegramReporter:
    """Telegram reporter for SEO reports."""

    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHAT_ID

    async def send_report(self, pdf_path: str, week_label: str, summary: str = None):
        """Send PDF report to Telegram."""
        try:
            caption = f"📊 <b>SEO Report</b>\n📅 {week_label}"
            if summary:
                caption += f"\n\n{summary}"

            with open(pdf_path, 'rb') as pdf_file:
                await self.bot.send_document(
                    chat_id=self.chat_id,
                    document=pdf_file,
                    caption=caption,
                    parse_mode=ParseMode.HTML
                )

            logger.info(f"Report sent to Telegram: {pdf_path}")

        except Exception as e:
            logger.error(f"Failed to send report to Telegram: {e}")
            raise

    async def send_alerts(self, alerts: List[Dict]):
        """Send alert summary to Telegram."""
        if not alerts:
            return

        critical = [a for a in alerts if a.get('severity') == 'critical']
        warnings = [a for a in alerts if a.get('severity') == 'warning']

        message = f"🚨 <b>SEO Alerts</b>\n\n"
        message += f"🔴 Critical: {len(critical)}\n"
        message += f"🟡 Warnings: {len(warnings)}\n\n"

        for alert in critical[:5]:  # Show top 5 critical
            message += f"🔴 {alert['message']}\n"

        if len(critical) > 5:
            message += f"\n...and {len(critical) - 5} more critical alerts"

        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.HTML
            )
            logger.info(f"Sent {len(alerts)} alerts to Telegram")

        except Exception as e:
            logger.error(f"Failed to send alerts: {e}")
            raise

    async def send_text_message(self, text: str):
        """Send simple text message."""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise


if __name__ == '__main__':
    import asyncio
    reporter = TelegramReporter()
    print("TelegramReporter initialized")
