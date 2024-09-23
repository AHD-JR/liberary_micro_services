from sqlite_config import SessionLocal, User

class UsersStore():
    def __init__(self):
        self.db = SessionLocal()
        
    def close(self):
        if self.db:
            self.db.close()

    def store_user(self, user):
        try:
            new_user = User(**user)
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            return user
        finally:
            self.close()

    def find_user_by_email(self, email):
        try:
            return self.db.query(User).filter(User.email == email).first()
        finally:
            self.close()

    def find_users(self, limit, offset):
        try:
            return self.db.query(User).limit(limit).offset(offset).all()
        finally:
            self.close()

    
        


