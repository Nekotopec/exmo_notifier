import logging

import aiogram
from aiogram.dispatcher.webhook import get_new_configured_app


class WebhookBotMixin:
    """Aiogram bot with webhook start."""
    # Webhook settings.
    _webhook_url: str = None
    _webhook_path: str = None

    # SSL cert.
    _webhook_ssl_cert: str = None
    _webhook_ssl_priv: str = None

    # Dispatcher.
    _dp: aiogram.Dispatcher = None

    def prepare_bot(self, webhook_url: str,
                    webhook_path: str,
                    webhook_ssl_cert: str,
                    webhook_ssl_priv: str):
        """
        Prepare bot.
        Set `WEBHOOK_URL`, `WEBHOOK_PATH`, `WEBHOOK_SSL_CERT`,
        `WEBHOOK_SSL_PRIV` and `dp`.
        """

        self._webhook_url = webhook_url
        self._webhook_path = webhook_path
        self._webhook_ssl_cert = webhook_ssl_cert
        self._webhook_ssl_priv = webhook_ssl_priv

    def get_dispatcher(self):
        return self._dp

    async def on_startup(self, app):

        # Get current webhook status
        webhook = await self.get_webhook_info()

        if webhook.url != self._webhook_url:
            # If URL doesnt match current - remove webhook
            if not webhook.url:
                await self.delete_webhook()

            # Set new URL for webhook
            await self.set_webhook(self._webhook_url,
                                   certificate=open(self._webhook_ssl_cert,
                                                    'rb'))

    async def on_shutdown(self, app):
        logging.warning('Shutting down..')

        # insert code here to run it before shutdown

        # Remove webhook (not acceptable in some cases)
        await self.delete_webhook()

        # Close DB connection (if used)
        await self._dp.storage.close()
        await self._dp.storage.wait_closed()

        logging.warning('Webhook have been deleted.')

        # Close bot.

    def check_settings(self):
        """Check for existing settings."""
        return not (self._webhook_url and
                    self._webhook_path and
                    self._webhook_ssl_priv and
                    self._webhook_ssl_cert)

    def init_app(self, dp: aiogram.Dispatcher):
        if self.check_settings():
            raise TypeError('Every webhook setting mast be not blank. '
                            'Use method `prepare_bot` first.')
        self._dp = dp
        app = get_new_configured_app(dispatcher=self._dp,
                                     path=self._webhook_path)
        # Setup event handlers.
        app.on_startup.append(self.on_startup)
        app.on_shutdown.append(self.on_shutdown)

        return app


class WebhookBot(aiogram.Bot, WebhookBotMixin):
    """
    Telegram bot with webhook support.
    Use bot.prepare(**params) and then bot.init_app(dp) where dp
    is dp=Dispatcher(bot).
    """
    pass
