from random import randrange
from datetime import datetime
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()

my_users = list()

class Users(BaseModel):
    _id         : int   = None
    first       : str 
    last        : str
    email       : str   = None
    wallets     : list  = None
    createdAt   : str   = None

def find_user(id):
    for index, user in enumerate(my_users):
        if user['_id'] == id:
            return user, index

@app.get("/")
def root():
    return {'message': 'Hello World'}

@app.get("/users")
def get_users():
    return {'users': my_users}

@app.get("/users/{id}")
def get_user(id: int):
    user, _ = find_user(id)
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User ID {id} not found')
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': f'User ID {id} not found'}
    return {'user': user}

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_users(new_user: Users):
    post_user = new_user.dict()
    post_user['_id'] = randrange(0, 1000)
    post_user['createdAt'] = datetime.now()
    my_users.append(post_user)
    return {'data': post_user}

@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_users(id: int):
    user, _ = find_user(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User ID {id} not found')
    my_users.remove(user)
    # Si mandamos un 204, no deberiamos retornar nada

@app.put("/users/{id}")
def update_users(id: int, updated_user: Users):
    user, index = find_user(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User ID {id} not found')
        
    updated_user = updated_user.dict()
    updated_user['_id'] = id
    my_users[index] = updated_user

    return {'message': f'Updated user {id} successfully'}

