from auth.models import CoreUser
import random
import string

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    password = ''.join(random.choice(string.ascii_letters) for i in range(20))
    user = CoreUser(email='patkennedy79@gmail.com')
    user.set_password(password=password)
    assert user.email == 'patkennedy79@gmail.com'
    assert user.password_hash != password
