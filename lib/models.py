from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from lib.database import Base

class Chapter(Base):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title_id = Column(Integer, ForeignKey('titles.id'))
    chapter_number = Column(Integer, comment="Номер главы")

    title = relationship("Title", back_populates="chapters")
    chapter_assignments = relationship("ChapterAssignment", back_populates="chapter")

class ChapterAssignment(Base):
    __tablename__ = 'chapter_assignments'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    worker_id = Column(Integer, ForeignKey('workers.id'))
    chapter_id = Column(Integer, ForeignKey('chapters.id'))

    worker = relationship("Worker", back_populates="chapter_assignments")
    chapter = relationship("Chapter", back_populates="chapter_assignments")

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, unique=True, comment="Название роли")

    workers = relationship("Worker", back_populates="role")

class Title(Base):
    __tablename__ = 'titles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title_name = Column(String, unique=True, comment="Название тайтла")

    chapters = relationship("Chapter", back_populates="title")
    title_assignments = relationship("TitleAssignment", back_populates="title")

class TitleAssignment(Base):
    __tablename__ = 'title_assignments'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    worker_id = Column(Integer, ForeignKey('workers.id'))
    title_id = Column(Integer, ForeignKey('titles.id'))

    worker = relationship("Worker", back_populates="title_assignments")
    title = relationship("Title", back_populates="title_assignments")

class Worker(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    nickname = Column(String, unique=True, comment="Никнейм в Discord")

    role = relationship("Role", back_populates="workers")
    title_assignments = relationship("TitleAssignment", back_populates="worker")
    chapter_assignments = relationship("ChapterAssignment", back_populates="worker")
