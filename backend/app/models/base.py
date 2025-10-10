from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# Example model placeholder (create proper models later)
# from sqlalchemy import Column, Integer, String
# class Recipient(Base):
# __tablename__ = 'recipients'
# id = Column(Integer, primary_key=True)
# email = Column(String, unique=True, index=True, nullable=False)