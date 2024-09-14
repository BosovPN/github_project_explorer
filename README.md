# Github_project_explorer

<details>
<summary><b>Show input and output data</b></summary>

```plaintext
Enter your GitHub username: BosovPN
Enter your repository name: cryptocurrency_tracker
Enter your GitHub token (optional): 

Result:
Repository Structure:
├── README.md
├── backend/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src/
│   │   ├── config.py
│   │   ├── http_client.py
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── router.py
├── frontend/
│   ├── .dockerignore
│   ├── .eslintrc.cjs
│   ├── Dockerfile
│   ├── README.md
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.cjs
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── CryptocurrencyCard.jsx
│   │   ├── index.css
│   │   ├── main.jsx
│   ├── tailwind.config.js
│   ├── vite.config.js
```

```bash
backend/src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    CMC_API_KEY: str
    model_config = SettingsConfigDict(env_file='.env')
settings = Settings()
```

```bash
backend/src/http_client.py
from aiohttp import ClientSession
from async_lru import alru_cache
class HttpClient:
    def __init__(self, base_url: str, service: str, api_key: str):
        self._session = ClientSession(
            base_url=base_url,
            headers={
                service: api_key,
            }
        )
class CMCHttpClient(HttpClient):
    @alru_cache(ttl=300)
    async def get_listings(self):
        async with self._session.get('/v1/cryptocurrency/listings/latest') as resp:
            result = await resp.json()
            return result["data"]
    @alru_cache(ttl=300)
    async def get_currency(self, currency_id: int):
        async with self._session.get(
            '/v2/cryptocurrency/quotes/latest',
            params={'id': currency_id}
        ) as resp:
            result = await resp.json()
            return result["data"][str(currency_id)]
```

```bash
Other files
```
</details>

### Cloning the repository

Clone the repository using the command below :
```bash
git clone https://github.com/BosovPN/github_project_explorer.git
```

### Running app in console

Move into directory where we have the project file : 
```bash
cd github_project_explorer
```

Run python script : 
```bash
python script.py
```

Remember about the request limit.
