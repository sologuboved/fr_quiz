import os

from pymongo import MongoClient

from global_vars import (
    ADJECTIFS,
    DB_NAME,
    LOCALHOST,
    NOMS,
    PHRASES,
    PORT,
    VERBES,
    VOCABULAIRES,
)
from helpers import read_csv


def csv_to_mongo(anew, collname, fname=None):
    if not fname:
        fname = os.path.join(os.sep, VOCABULAIRES, collname + '.csv')
    print(f"{fname} -> {collname}...")
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][collname]
    if anew:
        target.drop()
    else:
        print(f"Initially {target.estimated_document_count()} entries")
    target.insert_many(list(read_csv(fname)))
    print(f"Currently {target.estimated_document_count()} entries")


def total_upd_from_csv():
    for collname in (
        ADJECTIFS,
        NOMS,
        PHRASES,
        VERBES,
    ):
        csv_to_mongo(anew=True, collname=collname)


if __name__ == '__main__':
    from os_ops import delete_pid, write_pid

    pid_fname = write_pid()
    total_upd_from_csv()
    delete_pid(pid_fname)
