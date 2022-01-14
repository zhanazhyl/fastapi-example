from fastapi import FastAPI
from pydantic.dataclasses import dataclass
from pony.orm import Database, PrimaryKey, Required, db_session, set_sql_debug
from pony.orm.core import desc, select
from pony.utils.utils import avg

app = FastAPI()
db = Database(provider='sqlite', filename='database.db', create_db=True)

class User(db.Entity):
    _table_ = "Users"
    id = PrimaryKey(int, auto=True)
    first_name = Required(str)
    salary = Required(int)
db.generate_mapping(create_tables=True)

@dataclass
class UserDTO:
    first_name: str
    salary: int


@app.get("/api/users")
def getUsers():
    users = None
    with db_session:
        users = User.select()
        return [u.to_dict() for u in users]

@app.post("/api/users")
def createUser(user: UserDTO):
    with db_session:
        User(first_name=user.first_name, salary=user.salary)
        db.commit()
        return {"message": "user was created"}