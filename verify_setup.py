import asyncio
from database import init_db, AsyncSessionLocal
from models_db import Users
from repo import BaseRepository

async def main():
    print("--- STEP 1: Initializing Tables in PostgreSQL ---")
    await init_db()
    print("✓ Tables created successfully!")

    print("\n--- STEP 2: Testing Repository CRUD Operations ---")
    # Open an async session manually for testing
    async with AsyncSessionLocal() as session:
        # Initialize your BaseRepository for the Users model
        user_repo = BaseRepository(session, Users)

        # 1. Create a test user (matching your schema fields)
        new_user = Users(
            username="kavya_test",
            email="kavya@example.com",
            fullname="Kavya More"
        )
        
        created = await user_repo.create(new_user)
        print(f"✓ User created! Assigned ID: {created.user_id}")
        print(f"  Username: {created.username} | Created At: {created.created_at}")

        # 2. Fetch the user back by ID
        fetched = await user_repo.get_by_id(created.user_id)
        print(f"✓ Fetched by ID successfully: {fetched.fullname}")

        # 3. Check total user count using repository count()
        total = await user_repo.count()
        print(f"✓ Total users in database: {total}")

    print("\n🎉 All database, model, and repository checks passed!")

if __name__ == "__main__":
    asyncio.run(main())