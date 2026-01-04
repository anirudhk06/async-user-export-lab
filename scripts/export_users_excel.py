from openpyxl import Workbook
from sqlalchemy import select

from app.db import SessionLocal
from app.models import User

CHUNK_SIZE = 2_000
EXPORT_FILE = "exports/users_export.xlsx"


def export_users() -> None:
    session = SessionLocal()

    wb = Workbook(write_only=True)
    ws = wb.create_sheet(title="Users")

    ws.append(
        [
            "ID",
            "First Name",
            "Last Name",
            "Email",
            "Is Active",
            "Created At",
        ]
    )

    offset = 0
    total_exported = 0

    try:
        while True:
            stmt = select(User).order_by(User.id).offset(offset).limit(CHUNK_SIZE)

            users = session.execute(stmt).scalars().all()

            if not users:
                break

            for user in users:
                ws.append(
                    [
                        user.id,
                        user.first_name,
                        user.last_name,
                        user.email,
                        user.is_active,
                        user.created_at,
                    ]
                )

            total_exported += len(users)
            offset += CHUNK_SIZE

            print(f"Exported {total_exported} users")

        wb.save(EXPORT_FILE)
        print(f"Excel export completed: {EXPORT_FILE}")

    finally:
        session.close()


if __name__ == "__main__":
    export_users()
