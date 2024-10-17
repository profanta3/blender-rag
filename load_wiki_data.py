import glob
import os
import lancedb

from models import Document


def read_file_content(file: str):
    with open(file, "r") as f:
        return f.read()


def load_data_docs(data_root: str = "data/blender-manual/manual/") -> dict:
    files = []

    for index, file in enumerate(glob.glob(f"{data_root}**/*.rst", recursive=True)):
        files.append(dict(text=read_file_content(file)))

    print(len(files))
    # print(files[0])

    return files


if __name__ == "__main__":
    print("Filling LanceDB")
    table_name = os.environ["DB_NAME"]

    print(f"Table-Name: {table_name}")

    docs = load_data_docs()

    db = lancedb.connect("./data/lance")

    db.drop_table(table_name)

    tbl = db.create_table(table_name, schema=Document, exist_ok=True)

    print(f"Adding {len(docs)}-docs to table")
    tbl.add(docs)

    tbl.create_fts_index("text")
    print("Done.")
