import asyncpg
import asyncio
import config


import asyncpg

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(user=config.DB_USERNAME, password=config.DB_PASSWORD, database=config.DB_NAME, host=config.DB_HOST)

    async def disconnect(self):
        await self.pool.close()

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()


class ManageDB:
    async def get_profile_info(self, tg_id):
        async with Database() as db:
            res = await db.fetchrow(f"select * from users where tg_id = '{tg_id}'")
        return res
    
    async def create_user(self, tg_id, *args):
        async with Database() as db:
            await db.execute(f"insert into users (tg_id) values ('{tg_id}')")
        
    async def set_profile_info(self, tg_id, data : dict):
        s = ''
        for key, value in data.items():
            if value:
                s += key + '=' + f"'{value}'"
        async with Database() as db:
            await db.execute("update users set " + s + f" where tg_id='{tg_id}'")

        





if __name__ == '__main__':
    async def main():
        await ManageDB().create_user(843)
    
    asyncio.run(main())