from fastapi import FastAPI, Form , Request
from typing import Annotated
from fastapi.templating import Jinja2Templates

from fastapi.responses import HTMLResponse
from mangum import Mangum
import FetchJob

app = FastAPI()
handler = Mangum(app)

templates = Jinja2Templates(directory='templates')
demand_list = []


@app.get("/" , response_class = HTMLResponse)
async def query_page(request: Request):
    return templates.TemplateResponse('Career.html' , {"request": request , "job_demands": demand_list})



@app.post("/" , response_class= HTMLResponse)
async def career(request: Request , userInput: Annotated[str, Form()]):
    job = FetchJob.JobQuery(userInput, 1)
    job_url = job.scrape()
    demand_list = job.job_detail(job_url)
    return templates.TemplateResponse("Career.html" , {'request':request , "demand_list":demand_list})