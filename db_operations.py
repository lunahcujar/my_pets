from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datebase import Pets

async def create_pet(
        db_session:AsyncSession,
        name:str,
        breed:str=None,
        birth:int=None,
        kind:str=None,
        female:bool=None,
):
    pet = Pets(
        name=name,
        breed=breed,
        birth=birth,
        kind=kind,
        female=female,
    )
    async with db_session.begin():
        db_session.add(pet)
        await db_session.flush()
        pet_id = pet.id
        await db_session.commit()
    return pet_id

#recuperar por id
async def db_get_one_pet(pet_id:int, db_session:AsyncSession):
    query= (select(Pets).wehere(Pets.id==pet_id))
    result = await db_session.execute(query)

    pet= result.scalars().first()

    return pet

#recuperar todas las mascotas de db

async def db_get_all_peets(db_session:AsyncSession):
    query= (select(Pets))
    result = await db_session.execute(query)
    pets=result.scalars().all()
    return pets

#Modificar una mascota
async def db_mofify_name(pet_id:int, new_name: str, db_session:AsyncSession):
    query=(update(Pets).where(Pets.id==pet_id).values(name=new_name))
    result = await db_session.execute(query)
    #confirmacion de cambio
    await db_session.commit()
    if result.rowcount == 0:
        return False
    return True

#renover mascota
async def db_remove_pet(pet_id:int, db_session:AsyncSession):
    result=await db_session.execute(delete(Pets).where(Pets.id==pet_id))
    await db_session.commit()
    if result.rowcount == 0:
        return False
    return True

