from fastapi import FastAPI
from dotenv import load_dotenv

from app.modules.research.schema import ResearchInput
from scalar_fastapi import get_scalar_api_reference

from app.modules.research.tasks import research_task

load_dotenv()

app = FastAPI()


@app.post("/research")
def do_research(body: ResearchInput):
    research_task.delay(strategy=body.strategy)


@app.get("/scalar")
def get_scalar_api_reference_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
