import os
import lancedb

from lib.models.models import Document
from ui.load_wiki_data import load_data_docs
from pprint import pprint as pp
from lib.logger import log


def main():
    log.info("Start")
    table_name = os.environ["DB_NAME"]

    db = lancedb.connect("./data/lance")

    tbl = db.create_table(table_name, schema=Document, exist_ok=True)

    query = input("Input Query> ")
    # query = "where can I create a monkey?"

    result = tbl.search(query, query_type="hybrid").limit(1).to_list()[0]

    pp(Document.model_validate(result))


if __name__ == "__main__":
    main()