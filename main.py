import asyncio

import aiohttp
from more_itertools import chunked

from models import init_db, close_db, Character, AsyncSession

MAC_CHUNK_SIZE = 5

async def get_character(http_session, character_id):
    response = await http_session.get(f"https://www.swapi.tech/api/people/{character_id}")
    json_data = await response.json()
    return character_id, json_data

async def insert_characters(list_characters_json):
    character_id = list_characters_json[0]
    data = list_characters_json[1]
    async with AsyncSession() as async_session:
        characters = [Character(
            api_id=character_id,
            name=character_json['result']['properties']['name'],
            birth_year=character_json['result']['properties']['birth_year'],
            eye_color=character_json['result']['properties']['eye_color'],
            gender=character_json['result']['properties']['gender'],
            hair_color=character_json['result']['properties']['hair_color'],
            homeworld=character_json['result']['properties']['homeworld'],
            mass=character_json['result']['properties']['mass'],
            skin_color=character_json['result']['properties']['skin_color'],
            ) for character_json in data]
        async_session.add_all(characters)
        await async_session.commit()

async def main():
    await init_db()
    async with aiohttp.ClientSession() as http_session:
        for characters_chunk in chunked(range(1, 100), MAC_CHUNK_SIZE):
            coros = [get_character(http_session, num) for num, _ in enumerate(characters_chunk, start=1)]
            characters = await asyncio.gather(*coros)
            inserts_characters_coro = insert_characters(characters)
            insert_characters_task = asyncio.create_task(inserts_characters_coro)
    tasks = asyncio.all_tasks()
    main_task = asyncio.current_task()
    tasks.remove(main_task)
    await asyncio.gather(*tasks)
    await close_db()
    
    # await close_db()
if __name__ == '__main__':
    asyncio.run(main())