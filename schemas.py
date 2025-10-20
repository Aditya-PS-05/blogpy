from dotenv import load_dotenv
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import Any

import motor.motor_asyncio
import os

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))

db = client.blog_api

# MongoDB uses BSON and Fastapi uses JSON, so we need to convert the data
class PyObjecyId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda x: str(x)),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return ObjectId(v)

class User(BaseModel):
    id: PyObjecyId = Field(default_factory=PyObjecyId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "email": "Johndoe@gmail.com",
                "password": "secret_code",
            }
        }
    }

class UserResponse(BaseModel):
    id: PyObjecyId = Field(default_factory=PyObjecyId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "email": "Johndoe@gmail.com",
            }
        }
    }
