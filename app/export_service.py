from openpyxl import Workbook
from sqlalchemy import select

from app.db import SessionLocal
from app.models import User


def export_users_to_excel(file_path: str, chunk_size: int = 2000):
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
    total = 0

    try:
        while True:
            stmt = select(User).order_by(User.id).offset(offset).limit(chunk_size)

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

            total += len(users)
            offset += chunk_size
            print(f"Exported {total} users")

        wb.save(file_path)
        print(f"Excel saved to {file_path}")

    finally:
        session.close()
