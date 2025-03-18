from fastapi import FastAPI, Depends, HTTPException
from lib.database import get_session, engine, Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy import select, update
from typing import Annotated
import lib.models as models
import lib.schemas as schemas
import uvicorn

app = FastAPI()

session_dependency = Annotated[AsyncSession, Depends(get_session)]


# Generic CRUD functions for all models
async def create_entity(session, model, data):
    new_entity = model(**data.dict())
    session.add(new_entity)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        return {"error": str(e)}
    return {"message": f"{model.__name__} created"}

async def get_entities(session, model):
    query = select(model)
    result = await session.execute(query)
    return result.scalars().all()

async def update_entity(session, model, entity_id, data):
    try:
        query = update(model).where(model.id == entity_id).values(**data.dict())
        result = await session.execute(query)
        if not result.rowcount:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    except Exception as e:
        await session.rollback()
        return {"error": str(e)}
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        return {"error": str(e)}
    return {"message": f"{model.__name__} updated"}

async def delete_entity(session, model, entity_id):
    entity = await session.get(model, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    try:
        await session.delete(entity)
        await session.commit()
    except Exception as e:
        await session.rollback()
        return {"error": str(e)}
    return {"message": f"{model.__name__} deleted"}


# Define routes for roles using the generic functions
@app.get("/roles", tags=["Roles"], name="Получить список ролей")
async def get_roles(session: session_dependency):
    return await get_entities(session, models.Role)

@app.post("/roles", tags=["Roles"], name="Создать роль")
async def create_role(data: schemas.RoleBase, session: session_dependency):
    return await create_entity(session, models.Role, data)

@app.post("/roles/{id}", tags=["Roles"], name="Изменить роль")
async def update_role(id: int, data: schemas.RoleBase, session: session_dependency):
    return await update_entity(session, models.Role, id, data)

@app.delete("/roles/{id}", tags=["Roles"], name="Удалить роль")
async def delete_role(id: int, session: session_dependency):
    return await delete_entity(session, models.Role, id)

# Define routes for workers using the generic functions
@app.get("/workers", tags=["Workers"], name="Получить список работников")
async def get_workers(session: session_dependency):
    return await get_entities(session, models.Worker)

@app.post("/workers", tags=["Workers"], name="Создать работника")
async def create_worker(data: schemas.WorkerBase, session: session_dependency):
    return await create_entity(session, models.Worker, data)

@app.post("/workers/{id}", tags=["Workers"], name="Изменить работника")
async def update_worker(id: int, data: schemas.WorkerBase, session: session_dependency):
    return await update_entity(session, models.Worker, id, data)

@app.delete("/workers/{id}", tags=["Workers"], name="Удалить работника")
async def delete_worker(id: int, session: session_dependency):
    return await delete_entity(session, models.Worker, id)


# Define routes for titles using the generic functions
@app.get("/titles", tags=["Titles"], name="Получить список тайтлов")
async def get_titles(session: session_dependency):
    return await get_entities(session, models.Title)

@app.post("/titles", tags=["Titles"], name="Создать тайтл")
async def create_title(data: schemas.TitleBase, session: session_dependency):
    return await create_entity(session, models.Title, data)

@app.post("/titles/{id}", tags=["Titles"], name="Изменить тайтл")
async def update_title(id: int, data: schemas.TitleBase, session: session_dependency):
    return await update_entity(session, models.Title, id, data)

@app.delete("/titles/{id}", tags=["Titles"], name="Удалить тайтл")
async def delete_title(id: int, session: session_dependency):
    return await delete_entity(session, models.Title, id)


# Define routes for title assignments using the generic functions
@app.get("/title-assignments", tags=["Title Assignments"], name="Получить список назначений")
async def get_assignments(session: session_dependency):
    return await get_entities(session, models.TitleAssignment)

@app.post("/title_assignments", tags=["Title Assignments"], name="Создать назначение")
async def create_assignment(data: schemas.TitleAssignmentBase, session: session_dependency):
    return await create_entity(session, models.TitleAssignment, data)

@app.post("/title_assignments/{id}", tags=["Title Assignments"], name="Изменить назначение")
async def update_assignment(id: int, data: schemas.TitleAssignmentBase, session: session_dependency):
    return await update_entity(session, models.TitleAssignment, id, data)

@app.delete("/title_assignments/{id}", tags=["Title Assignments"], name="Удалить назначение")
async def delete_assignment(id: int, session: session_dependency):
    return await delete_entity(session, models.TitleAssignment, id)


# Define routes for chapters using the generic functions
@app.get("/chapters", tags=["Chapters"], name="Получить список глав")
async def get_chapters(session: session_dependency):
    return await get_entities(session, models.Chapter)

@app.get("/chapters/{id}/workers", tags=["Chapters"], name="Получить работников по определенной главе")
async def get_chapter_workers(id: int, session: session_dependency):
    query = select(models.Worker).join(models.ChapterAssignment).where(models.ChapterAssignment.chapter_id == id)
    result = await session.execute(query)
    return result.scalars().all()

@app.post("/chapters", tags=["Chapters"], name="Создать главу")
async def create_chapter(data: schemas.ChapterBase, session: session_dependency):
    return await create_entity(session, models.Chapter, data)

@app.post("/chapters/{id}", tags=["Chapters"], name="Изменить главу")
async def update_chapter(id: int, data: schemas.ChapterBase, session: session_dependency):
    return await update_entity(session, models.Chapter, id, data)

@app.delete("/chapters/{id}", tags=["Chapters"], name="Удалить главу")
async def delete_chapter(id: int, session: session_dependency):
    return await delete_entity(session, models.Chapter, id)


# Define routes for chapter assignments using the generic functions
@app.get("/chapter-assignments", tags=["Chapter Assignments"], name="Получить список назначений")
async def get_assignments(session: session_dependency):
    return await get_entities(session, models.ChapterAssignment)

@app.post("/chapter_assignments", tags=["Chapter Assignments"], name="Создать назначение")
async def create_assignment(data: schemas.ChapterAssignmentBase, session: session_dependency):
    return await create_entity(session, models.ChapterAssignment, data)

@app.post("/chapter_assignments/{id}", tags=["Chapter Assignments"], name="Изменить назначение")
async def update_assignment(id: int, data: schemas.ChapterAssignmentBase, session: session_dependency):
    return await update_entity(session, models.ChapterAssignment, id, data)

@app.delete("/chapter_assignments/{id}", tags=["Chapter Assignments"], name="Удалить назначение")
async def delete_assignment(id: int, session: session_dependency):
    return await delete_entity(session, models.ChapterAssignment, id)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
