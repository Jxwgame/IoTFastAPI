from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
# from sqlalchemy.orm import relationship

from database import Base

class Students(Base):
    __tablename__ = 'Student_info'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    date = Column(Date, index=True)
    sex = Column(String, index=True)

