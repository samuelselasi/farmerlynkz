# def authLogin(user: loginUser, db: Session):
#     userDb: Query = findByEmail(user.email, db)
#     if userDb.count():
#         verify_password(user.password, )


def NotConfirmPassword(password: str, confirmPassword: str):
    if(password != confirmPassword):
        return True
    else:
        return False
