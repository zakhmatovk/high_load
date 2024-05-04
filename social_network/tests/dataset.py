



import datetime

from faker import Faker


class Dataset:

    @classmethod
    async def user(cls, **kwargs):
        from social_network.models.user import User
        fake = Faker()
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        user_name = f'{last_name} {first_name}'.lower().replace(' ', '_')
        email = user_name + '@example.com'
        
        kwargs.setdefault('username', user_name)
        kwargs.setdefault('email', email)
        kwargs.setdefault('password', 'mockpassword')
        kwargs.setdefault('first_name', first_name)
        kwargs.setdefault('last_name', last_name)
        kwargs.setdefault('birth_date', datetime.date.today())
        kwargs.setdefault('gender', "Male")
        kwargs.setdefault('city', "Mock City")
        kwargs.setdefault('interests', ["Coding", "AI"])


        user = User(**kwargs)
        return await user.insert()
