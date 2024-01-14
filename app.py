from http import client
from unicodedata import category
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import gspread
from oauth2client.service_account import ServiceAccountCredentials

client = gspread.service_account("/etc/secrets/creds.json")
sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1virgIh_FdgZHYLpIopt41uZ-HhQQUxYdOeKnoZp_9w8/").sheet1


app = FastAPI()


class Record(BaseModel):
    type: str
    description: str
    date: str
    amount: int
    category: str

def process_date(date):
    splits= date.split("/")
    splits[0], splits[1] = splits[1], splits[0]
    return "/".join(splits)


@app.post("/track/")
def save_to_gsheet(record: Record):

    row = [record.type, record.description, process_date(record.date), record.amount, record.category]
    index = 2  # Rows start at index 1, and we skip the header row
    sheet.append_row(row, index)  # Insert the row at the correct index
    return JSONResponse(status_code=200, content=jsonable_encoder({"message": f"Saved {record.description}"}), media_type="application/json")
