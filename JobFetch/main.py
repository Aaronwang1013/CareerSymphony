from fastapi import FastAPI, Form , Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse
from mangum import Mangum
import FetchJob
import matplotlib.pyplot as plt
##database
# import schema
from database import SessionLocal, engine

## show image on page
from io import BytesIO
import base64
# import model 
##bind our database engine
# model.Base.metadata.create_all(bind=engine)

app = FastAPI()
handler = Mangum(app)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

demand_list = []

def tool_bar(demand_list , user_input):
    tools = list(demand_list.keys())
    counts = list(demand_list.values())
    plt.figure(figsize=(15, 6)) 
    plt.bar(tools, counts)
    plt.xlabel('tools')
    plt.ylabel('times')
    plt.title(f"{user_input}")
    plt.xticks(rotation=90)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    chart_data = base64.b64encode(buffer.read()).decode("utf-8")
    return chart_data

    
@app.get("/" , response_class = HTMLResponse)
async def query_page(request: Request):
    return templates.TemplateResponse('Career.html' , {"request": request , "job_demands": demand_list})



@app.post("/" , response_class= HTMLResponse)
async def career(request: Request , userInput: Annotated[str, Form()]):
    job = FetchJob.JobQuery(userInput)
    job_url = job.scrape()
    demand_list = job.job_detail(job_url)
    # print(demand_list)
    tool_count = {}
    for tool_set in demand_list:
        for tool in tool_set:
            if tool in tool_count:
                tool_count[tool] += 1
            else:
                tool_count[tool] = 1
    barChart = tool_bar(tool_count , userInput)
    return templates.TemplateResponse("Career.html" , {'request':request , "demand_list":demand_list , "tool_chart":barChart , "char_title" : f'{userInput}'})





# def get_database_session():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()
        
