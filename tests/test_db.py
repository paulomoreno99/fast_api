from sqlalchemy import select

from fast_api.models import User


def test_create_user(session):
    new_user = User(username='paulomoreno', password='123456', email='paulo@gmail.com')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'paulomoreno'))

    assert user.username == 'paulomoreno'
