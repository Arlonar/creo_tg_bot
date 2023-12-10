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
    # status = ('canceled', 'waiting', 'in_progress', 'done')
    async def get_profile_info(self, tg_id):
        async with Database() as db:
            res = await db.fetchrow(f"SELECT * FROM users WHERE tg_id = '{tg_id}'")
        return res
    
    async def create_user(self, tg_id, *args):
        async with Database() as db:
            await db.execute(f"INSERT INTO users (tg_id) VALUES ('{tg_id}')")
        
    async def set_profile_info(self, tg_id, data : dict):
        s = ''
        for key, value in data.items():
            if value:
                s += key + '=' + f"'{value}'"
        async with Database() as db:
            await db.execute("UPDATE users SET " + s + f" WHERE tg_id='{tg_id}'")
    
    async def get_contractor_info(self, tg_id):
        async with Database() as db:
            res = await db.fetchrow((f"SELECT contractors.*, users.first_name, users.last_name "
                                    f"FROM contractors JOIN users ON users.id=contractors.id WHERE users.tg_id='{tg_id}'"))
        return res

    async def get_notify_contractors_ids(self):
        async with Database() as db:
            res = await db.fetch(f"SELECT users.tg_id FROM contractors JOIN users ON users.id=contractors.id WHERE contractors.notification=true")
        return res
    
    async def register_contractor(self, tg_id):
        async with Database() as db:
            await db.execute(f"UPDATE users SET is_contractor=true WHERE tg_id='{tg_id}'")
            await db.execute(f"INSERT INTO contractors(id) VALUES((SELECT id FROM users WHERE users.tg_id='{tg_id}'))")

    async def get_history(self, tg_id):
        async with Database() as db:
            res = await db.fetch(f"SELECT orders.*, users.first_name, users.last_name, users.tg_id \
                                    FROM orders LEFT JOIN contractors ON contractors.id=orders.contractor_id \
                                    LEFT JOIN users ON users.id=contractors.id \
                                    WHERE client_id=(SELECT id FROM users WHERE tg_id='{tg_id}') \
                                    AND (orders.status='done' OR orders.status='canceled') ORDER BY orders.id")
        return res
    
    async def get_actual_orders(self, tg_id):
        async with Database() as db:
            res = await db.fetch(f"SELECT orders.*, users.tg_id, users.first_name, users.last_name \
                                    FROM orders LEFT JOIN contractors ON contractors.id=orders.contractor_id \
                                    LEFT JOIN users ON users.id=contractors.id \
                                    WHERE client_id=(SELECT id FROM users WHERE tg_id='{tg_id}') \
                                    AND (orders.status='in_progress' OR orders.status='waiting') ORDER BY orders.id")
        return res
    
    async def get_order_by_id(self, id):
        async with Database() as db:
            res = await db.fetchrow(f"SELECT orders.*, users.first_name, users.last_name, users.tg_id\
                                     FROM orders LEFT JOIN contractors ON contractors.id=orders.contractor_id LEFT JOIN users ON users.id=contractors.id\
                                     WHERE orders.id={id};")
        return res

    async def add_order(self, tg_id, amount, title, description):
        async with Database() as db:
            await db.execute(f"INSERT INTO orders(client_id, amount, title, description) " +\
                                f"VALUES((SELECT id FROM users WHERE users.tg_id='{tg_id}'), {amount}, '{title}', '{description}')")
    
    async def delete_order(self, order_id):
        async with Database() as db:
            await db.execute(f"UPDATE orders SET status='canceled' WHERE id={order_id}")
            await db.execute(f"INSERT INTO refund_requests(order_id) VALUES({order_id})")
        
    async def get_order_id_by_data(self, title, description, amount, client_id):
        async with Database() as db:
            id = await db.fetchrow(f"SELECT id FROM orders WHERE title='{title}' AND description='{description}' AND amount='{amount}'"
                                   f"AND client_id=(SELECT id FROM users WHERE tg_id='{client_id}')")
        return id
        
    async def set_contractor_for_order(self, order_id, contractor_tg_id):
        async with Database() as db:
            print(f"UPDATE orders SET contractor_id=(SELECT id FROM users WHERE tg_id='{contractor_tg_id}') WHERE id={order_id}")
            await db.execute(f"UPDATE orders SET status='in_progress', contractor_id=(SELECT id FROM users WHERE tg_id='{contractor_tg_id}') WHERE id={order_id}")




if __name__ == '__main__':
    async def main():
        await ManageDB().create_user(843)
    
    asyncio.run(main())
