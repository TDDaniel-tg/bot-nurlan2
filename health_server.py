import asyncio
import logging
from aiohttp import web
import threading
import time

logger = logging.getLogger(__name__)

class HealthServer:
    def __init__(self, port=8080):
        self.port = port
        self.app = web.Application()
        self.setup_routes()
        self.start_time = time.time()
        
    def setup_routes(self):
        """Настройка маршрутов для health check"""
        self.app.router.add_get('/health', self.health_check)
        self.app.router.add_get('/status', self.status_check)
        self.app.router.add_get('/', self.root_check)
        
    async def health_check(self, request):
        """Простой health check endpoint"""
        return web.json_response({
            'status': 'healthy',
            'uptime': time.time() - self.start_time,
            'service': 'telegram-pdf-converter-bot'
        })
        
    async def status_check(self, request):
        """Детальный статус сервиса"""
        return web.json_response({
            'status': 'running',
            'uptime_seconds': time.time() - self.start_time,
            'service': 'telegram-pdf-converter-bot',
            'version': '1.0.0'
        })
        
    async def root_check(self, request):
        """Корневой endpoint"""
        return web.Response(text="Telegram PDF to XLSX Converter Bot is running!")
        
    def start_server(self):
        """Запуск сервера в отдельном потоке"""
        def run_server():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def start():
                runner = web.AppRunner(self.app)
                await runner.setup()
                site = web.TCPSite(runner, '0.0.0.0', self.port)
                await site.start()
                logger.info(f"Health server started on port {self.port}")
                
                # Держим сервер запущенным
                while True:
                    await asyncio.sleep(1)
            
            try:
                loop.run_until_complete(start())
            except Exception as e:
                logger.error(f"Health server error: {e}")
        
        # Запуск в отдельном потоке
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        logger.info("Health server thread started")
        
        return thread 