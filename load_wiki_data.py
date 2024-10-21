import glob
import os
import lancedb
from rich.console import Console

from models import Document
from logger import log


def read_file_content(file: str):
    with open(file, "r") as f:
        return f.read()


def load_data_docs(data_root: str = "data/blender-manual/manual/") -> list:
    files = []

    for index, file in enumerate(glob.glob(f"{data_root}**/*.rst", recursive=True)):
        files.append(dict(text=read_file_content(file)))

    return files


if __name__ == "__main__":
    log.info("Filling LanceDB")
    table_name = os.environ["DB_NAME"]

    log.info(f"Table-Name: {table_name}")

    docs = load_data_docs()

    db = lancedb.connect("./data/lance")

    if table_name in db.table_names():
        db.drop_table(table_name)

    tbl = db.create_table(table_name, schema=Document, exist_ok=True)
    console = Console()
    with console.status(f"Adding {len(docs)} docs to db") as status:
        tbl.add(docs)

    tbl.create_fts_index("text")
    log.info("Done.")
