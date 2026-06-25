from sqlalchemy import Column, Integer, String
from models.food import Base


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    protein_target = Column(Integer)
    total_protein = Column(Integer)
    remaining_protein = Column(Integer)