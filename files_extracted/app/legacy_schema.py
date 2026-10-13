"""Preserve the earlier PostgreSQL section columns when upgrading Railway.

Some production databases received section/role/grade tables outside the old
release's ORM. Keep those tables and their values, and support both column names
while the old deployment and the new deployment overlap.
"""
from sqlalchemy import inspect, text

_SYNC_SECTION = """
CREATE OR REPLACE FUNCTION platform_sync_section_columns()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        IF NEW.class_section IS DISTINCT FROM OLD.class_section
           AND NEW.section IS NOT DISTINCT FROM OLD.section THEN
            NEW.section := NEW.class_section;
        ELSIF NEW.section IS DISTINCT FROM OLD.section
           AND NEW.class_section IS NOT DISTINCT FROM OLD.class_section THEN
            NEW.class_section := NEW.section;
        END IF;
    END IF;
    IF NEW.section IS NOT NULL AND NEW.class_section IS NOT NULL
       AND NEW.section IS DISTINCT FROM NEW.class_section THEN
        RAISE EXCEPTION 'Conflicting section and class_section values';
    END IF;
    NEW.class_section := COALESCE(NEW.class_section, NEW.section);
    NEW.section := NEW.class_section;
    RETURN NEW;
END;
$$
"""


async def align_legacy_sections(conn) -> None:
    """Add the new names without dropping legacy columns, rows, or constraints.

Called before the ordered migrations because 0003 inserts teacher assignments.
The bridge is also recorded as 0005 for databases already on 0001-0004.
"""
    tables = set(await conn.run_sync(lambda sync: inspect(sync).get_table_names()))
    for table in ("students", "teacher_sections"):
        if table not in tables:
            continue
        columns = await conn.run_sync(lambda sync, name=table: inspect(sync).get_columns(name))
        names = {column["name"] for column in columns}
        if "section" not in names:
            continue
        if conn.dialect.name != "postgresql":
            raise RuntimeError("The legacy section bridge requires PostgreSQL; no data was changed")
        constraint = f"ck_{table}_class_section"
        if "class_section" not in names:
            await conn.execute(text(
                f"ALTER TABLE {table} ADD COLUMN class_section VARCHAR(1) "
                f"CONSTRAINT {constraint} CHECK (class_section IN ('A', 'B', 'C', 'D'))"
            ))
        conflicts = (await conn.execute(text(
            f"SELECT COUNT(*) FROM {table} WHERE class_section IS NOT NULL "
            "AND section IS NOT NULL AND class_section <> section"
        ))).scalar_one()
        if conflicts:
            raise RuntimeError(f"{table}: conflicting section columns; upgrade rolled back")
        await conn.execute(text(
            f"UPDATE {table} SET class_section = section "
            "WHERE class_section IS NULL AND section IS NOT NULL"
        ))
        # A BEFORE trigger fills the old required section column on new inserts.
        # Its legacy id/default and all original constraints remain untouched.
        await conn.execute(text(_SYNC_SECTION))
        trigger = f"trg_{table}_sync_sections"
        await conn.execute(text(f"""
            DO $$ BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_trigger
                    WHERE tgrelid = '{table}'::regclass AND tgname = '{trigger}'
                ) THEN
                    CREATE TRIGGER {trigger} BEFORE INSERT OR UPDATE
                    ON {table} FOR EACH ROW EXECUTE FUNCTION platform_sync_section_columns();
                END IF;
            END $$
        """))
        if table == "teacher_sections":
            await conn.execute(text(
                "ALTER TABLE teacher_sections ALTER COLUMN class_section SET NOT NULL"
            ))
            await conn.execute(text(
                "CREATE UNIQUE INDEX IF NOT EXISTS ux_teacher_sections_class_section "
                "ON teacher_sections (teacher_id, class_section)"
            ))
