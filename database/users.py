# import pandas as pd
# import os

# FILE = "database/users.csv"

# def register_user(email, password, role):
#     # Load existing users or create empty DataFrame
#     df = pd.read_csv(FILE) if os.path.exists(FILE) else pd.DataFrame(columns=["email", "password", "role"])

#     # Check if email already exists
#     if email in df["email"].values:
#         return False

#     # ✅ Fix: Use pd.concat instead of deprecated .append()
#     new_user = pd.DataFrame([{"email": email, "password": password, "role": role}])
#     df = pd.concat([df, new_user], ignore_index=True)

#     # Save updated users list
#     df.to_csv(FILE, index=False)
#     return True

# def authenticate_user(email, password):
#     if not os.path.exists(FILE):
#         return None
#     df = pd.read_csv(FILE)
#     user = df[(df["email"] == email) & (df["password"] == password)]
#     if not user.empty:
#         return user.iloc[0].to_dict()
#     return None

# def get_all_users():
#     return pd.read_csv(FILE) if os.path.exists(FILE) else pd.DataFrame(columns=["email", "password", "role"])
import pandas as pd
import os

FILE = "database/users.csv"

def register_user(email, password, role):
    df = pd.read_csv(FILE) if os.path.exists(FILE) else pd.DataFrame(columns=["email", "password", "role"])

    if email in df["email"].values:
        return False

    new_user = pd.DataFrame([{"email": email, "password": password, "role": role}])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(FILE, index=False)
    return True

def authenticate_user(email, password):
    if not os.path.exists(FILE):
        return None
    df = pd.read_csv(FILE)
    user = df[(df["email"] == email) & (df["password"] == password)]
    if not user.empty:
        return user.iloc[0].to_dict()
    return None

def get_all_users():
    return pd.read_csv(FILE) if os.path.exists(FILE) else pd.DataFrame(columns=["email", "password", "role"])
