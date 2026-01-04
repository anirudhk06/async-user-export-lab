from faker import Faker

from app.db import SessionLocal
from app.models import User

TOTAL_USERS = 100_000
BATCH_SIZE = 1_000

fake = Faker()


def generate_users() -> None:
    session = SessionLocal()
    users_buffer: list[User] = []

    try:
        for i in range(1, TOTAL_USERS + 1):
            user = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                is_active=fake.boolean(chance_of_getting_true=90),
            )

            users_buffer.append(user)

            if i % BATCH_SIZE == 0:
                session.bulk_save_objects(users_buffer)
                session.commit()
                users_buffer.clear()
                print(f"Inserted {i} users")

        if users_buffer:
            session.bulk_save_objects(users_buffer)
            session.commit()

        print("User generation completed successfully")
    except Exception as e:
        session.rollback()
        print("Error:", e)

    finally:
        session.close()


if __name__ == "__main__":
    generate_users()
