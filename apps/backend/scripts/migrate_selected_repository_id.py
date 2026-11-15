from sqlalchemy import inspect, text

from app.db.session import engine


TABLE_NAME = "workspaces"
COLUMN_NAME = "selected_repository_id"


def main() -> None:
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if TABLE_NAME not in tables:
        raise RuntimeError(
            f"Table {TABLE_NAME!r} does not exist. "
            f"Available tables: {tables}"
        )

    if engine.dialect.name != "postgresql":
        raise RuntimeError(
            f"Expected PostgreSQL, got {engine.dialect.name!r}."
        )

    columns = {
        column["name"]
        for column in inspector.get_columns(TABLE_NAME)
    }

    if COLUMN_NAME in columns:
        print(
            f"Migration skipped: {TABLE_NAME}.{COLUMN_NAME} "
            "already exists."
        )
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                f"ALTER TABLE {TABLE_NAME} "
                f"ADD COLUMN {COLUMN_NAME} TEXT NULL"
            )
        )

    updated_columns = {
        column["name"]
        for column in inspect(engine).get_columns(TABLE_NAME)
    }

    if COLUMN_NAME not in updated_columns:
        raise RuntimeError("Migration verification failed.")

    print(
        f"Migration successful: "
        f"{TABLE_NAME}.{COLUMN_NAME} is now available."
    )


if __name__ == "__main__":
    main()
