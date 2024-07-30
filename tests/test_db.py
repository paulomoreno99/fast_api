from sqlalchemy import select

from fast_api.models import User


def test_create_user(session):
    new_user = User(
        username='paulo', password='123456', email='paulo@email.com'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'paulo'))

    assert user.username == 'paulo'
