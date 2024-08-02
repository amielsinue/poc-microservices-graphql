import strawberry
from typing import List, Optional
from strawberry.fastapi import GraphQLRouter
from sqlalchemy import text
from models import User
from database import get_db



@strawberry.type
class UserType:
    id: int
    username: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, info, id: int) -> Optional[UserType]:
        async for db in get_db():
            user = await db.execute(text(f"SELECT * FROM users WHERE id = {id}"))
            result = user.fetchone()
            if result:
                return UserType(id=result.id, username=result.username, email=result.email)
            return None

    @strawberry.field
    async def users(self, info) -> List[UserType]:
        async for db in get_db():
            users = await db.execute(text("SELECT * FROM users"))
            result = users.fetchall()
            return [UserType(id=user.id, username=user.username, email=user.email) for user in result]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, info, username: str, email: str) -> UserType:
         async for db in get_db():
            new_user = User(username=username, email=email)
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return UserType(id=new_user.id, username=new_user.username, email=new_user.email)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
