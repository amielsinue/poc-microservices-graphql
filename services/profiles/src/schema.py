import strawberry
from typing import List, Optional
from strawberry.fastapi import GraphQLRouter
from sqlalchemy import text
from database import get_db

from models import Profile


@strawberry.type
class ProfileType:
    id: int
    user_id: int
    bio: str
    location: str

@strawberry.type
class Query:
    @strawberry.field
    async def profile(self, info, user_id: int) -> Optional[ProfileType]:
        async for db in get_db():
            result = await db.execute(text(f"SELECT * FROM profiles WHERE user_id = :user_id"), {'user_id': user_id})
            profile = result.fetchone()
            if profile:
                return ProfileType(id=profile.id, user_id=profile.user_id, bio=profile.bio, location=profile.location)
        return None

    @strawberry.field
    async def profiles(self, info) -> List[ProfileType]:
        async for db in get_db():
            profiles = await db.execute(text("SELECT * FROM profiles"))
            result = profiles.fetchall()
            return [ProfileType(id=profile.id, user_id=profile.user_id, bio=profile.bio, location=profile.location) for profile in result]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_profile(self, info, user_id: int, bio: str, location: str) -> ProfileType:
        async for db in get_db():
            new_profile = Profile(user_id=user_id, bio=bio, location=location)
            db.add(new_profile)
            await db.commit()
            await db.refresh(new_profile)
            return ProfileType(id=new_profile.id, user_id=new_profile.user_id, bio=new_profile.bio, location=new_profile.location)


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
