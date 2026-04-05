import json
import logging
import asyncio

import websockets

logger = logging.getLogger(__name__)

RECONNECT_DELAY = 1
RECONNECT_DELAY_MAX = 60

class WSConnection:    
    def __init__(self, url: str):
        self.url = url

    async def connect(self, subscriptions: list[dict]):
        delay = RECONNECT_DELAY
        while True:
            try:
                async with websockets.connect(self.url) as websocket:
                    self.ws = websocket
                    for subscription in subscriptions:
                        await self.send(subscription)
                    logger.info(f"Connected to {self.url} with subscriptions: {subscriptions}")
                    
                    async for message in websocket:
                        data = json.loads(message)
                        yield data
            except (websockets.ConnectionClosed, OSError) as e:
                logger.error(f"Websocket Disconnected: {e}, reconnecting in {delay} seconds...")
            except Exception as e:
                logger.error(f"Unexpected error in Websocket loop: {e}, reconnecting in {delay} seconds...")
            finally:
                self.ws = None
                await asyncio.sleep(delay)
                delay = min(delay * 2, RECONNECT_DELAY_MAX)  # Exponential backoff with a max delay of 60 seconds

    async def send(self, message: dict):
        if self.ws is not None:
            await self.ws.send(json.dumps(message))
        else:
            logger.warning("Websocket is not connected. Cannot send message.")