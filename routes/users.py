from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from ..schemas import User, db, UserResponse
from ..utils import get_password_hash

import secrets

router = APIRouter(
    tags=["User Routes"]
)

@router.post("/registration", response_description="Register a user", response_model=UserResponse)
async def registration(user_info: User):
    user_dict = jsonable_encoder(user_info)

    # check if user already exists
    username_exists = await db["users"].find_one({"name": user_dict["name"]})
    email_found = await db["users"].find_one({"email": user_dict["email"]})

    if username_exists: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="Username already exists")
    
    if email_found: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="Email already exists")
    
    # Hash user password
    user_dict["password"] = get_password_hash(user_dict["password"])

    user_dict["apiKey"] = secrets.token_hex(30)
    new_user = await db["users"].insert_one(user_dict)

    created_user = await db["users"].find_one({"_id": new_user.inserted_id})

    # send email to the user

    return created_user

