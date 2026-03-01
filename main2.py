from fastmcp import FastMCP
import os
import asyncio
import tempfile
import aiosqlite

conn = await aiosqlite.connect("test.db")

async def init_db():
    async with aiosqlite.connect("test.db") as c:
        await c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)
        await c.commit()

asyncio.run(init_db())

async def add_expense():
    async with aiosqlite.connect("test.db") as c:
        await c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            ("2024-01-01", 100.0, "Food", "Groceries", "Bought groceries")
        )
        await c.commit()