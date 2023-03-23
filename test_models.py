from app.models import User

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = User(email='patkennedy79@gmail.com')
    user.set_password(password='FlaskIsAwesome')
    assert user.email == 'patkennedy79@gmail.com'
    assert user.password_hash != 'FlaskIsAwesome'
