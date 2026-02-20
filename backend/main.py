from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import re
from datetime import datetime



DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LeadDB(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    company = Column(String)
    phone = Column(String)
    email = Column(String)
    message = Column(String)
    created_at = Column(String)


Base.metadata.create_all(bind=engine)



class Lead(BaseModel):
    name: str
    company: str
    phone: str
    email: EmailStr
    message: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if not re.match(r"^\+7\d{10}$", v):
            raise ValueError("Телефон должен быть в формате +7XXXXXXXXXX")
        return v


@app.post("/api/lead")
def create_lead(lead: Lead):
    db = SessionLocal()

    new_lead = LeadDB(
        name=lead.name,
        company=lead.company,
        phone=lead.phone,
        email=lead.email,
        message=lead.message,
        created_at=datetime.now().isoformat()
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    db.close()

    return {"status": "saved"}
