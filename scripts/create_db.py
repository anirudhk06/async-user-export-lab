from app.db import engine, Base
from app import models


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database and tables created")


if __name__ == "__main__":
    main()
