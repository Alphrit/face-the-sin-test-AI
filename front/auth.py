import pandas as pd
import hashlib
import os

USER_DATA_PATH = "data/users.csv"

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def init_user_db():
    if not os.path.exists("data"):
        os.makedirs("data")
        
    if not os.path.exists(USER_DATA_PATH) or os.path.getsize(USER_DATA_PATH) == 0:
        df = pd.DataFrame(columns=["username", "password", "name"])
        df.to_csv(USER_DATA_PATH, index=False)

def register_user(username, password, name):
    try:
        df = pd.read_csv(USER_DATA_PATH)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=["username", "password", "name"])
        
    if username in df["username"].values:
        return False, "이미 존재하는 아이디입니다."
    
    new_user = pd.DataFrame([[username, hash_password(password), name]], 
                            columns=["username", "password", "name"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_DATA_PATH, index=False)
    return True, "회원가입 성공!"

def login_user(username, password):
    try:
        df = pd.read_csv(USER_DATA_PATH)
    except pd.errors.EmptyDataError:
        return False, None
        
    hashed_pw = hash_password(password)
    
    user = df[(df["username"] == username) & (df["password"] == hashed_pw)]
    if not user.empty:
        return True, user.iloc[0]["name"]
    return False, None