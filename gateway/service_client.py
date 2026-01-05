import httpx
import itertools
from tenacity import retry, stop_after_attempt, wait_exponential

class ServiceClient:
    def __init__(self, instances):
        self.instances = itertools.cycle(instances)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=4)
    )
    async def get(self, path: str):
        base_url = next(self.instances)
        url = f"{base_url}{path}"

        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()

        except Exception as e:
            print(f"[CIRCUIT BREAKER] Service failed: {e}")
            return {
                "status": "fallback",
                "message": "Service temporarily unavailable"
            }
