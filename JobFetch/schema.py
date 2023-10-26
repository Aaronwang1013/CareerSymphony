from datetime import date
from pydantic import BaseModel

class Job(BaseModel):
    id = int
    name = str
    tool = str
    demand = str
    url = str
    
    class Config:
        orm_mode = True