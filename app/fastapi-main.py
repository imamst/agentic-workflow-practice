from fastapi import FastAPI
from dotenv import load_dotenv

from app.modules.research.schema import ResearchInput
from scalar_fastapi import get_scalar_api_reference

load_dotenv()

app = FastAPI()


@app.post("/research")
def do_research(body: ResearchInput):
    return {}


@app.get("/scalar")
def get_scalar_api_reference_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
