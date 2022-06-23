import pandas as pd
import json
import sqlite3


def C2DB(name="c2db.db"):
    # Connect C2DB
    db = sqlite3.connect(name)
    df = pd.read_sql_query("SELECT * FROM systems", db)

    # key-value-pairs
    key_value_pairs = []
    for line in df.key_value_pairs:
        key_value_pairs.append(json.loads(line))
    key_value_pairs = pd.DataFrame(key_value_pairs)

    # extract chemistry formula
    line_list = list(key_value_pairs['folder'].str.split('/'))
    formulas = []
    for line in line_list:
        formulas.append(line[-1])
    key_value_pairs['formula'] = formulas

    # magnetic moment
    magnetic_moment = list(df.magmom)
    key_value_pairs['magnetic_moment'] = magnetic_moment

    # total_energy
    total_energy = list(df.energy)
    key_value_pairs['total_energy'] = total_energy

    # atoms number
    natoms = list(df.natoms)
    key_value_pairs['natoms'] = natoms

    return key_value_pairs


if __name__ == "__main__":
    C2DB("c2db-2021-06-24.db")