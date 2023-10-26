from fastapi import FastAPI, Form , Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse
from mangum import Mangum
import FetchJob

##database
# import schema
from database import SessionLocal, engine
# import model
##bind our database engine
# model.Base.metadata.create_all(bind=engine)

app = FastAPI()
handler = Mangum(app)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

demand_list = []


@app.get("/" , response_class = HTMLResponse)
async def query_page(request: Request):
    return templates.TemplateResponse('Career.html' , {"request": request , "job_demands": demand_list})



@app.post("/" , response_class= HTMLResponse)
async def career(request: Request , userInput: Annotated[str, Form()]):
    job = FetchJob.JobQuery(userInput)
    job_url = job.scrape()
    demand_list = job.job_detail(job_url)
    return templates.TemplateResponse("Career.html" , {'request':request , "demand_list":demand_list})



# def get_database_session():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()
        
