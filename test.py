def generate_sql_query(abonement_ids):
    sql_query = "INSERT INTO salon.loyalty_abonement_type_service_links (service_id, service_category_id, count, abonement_type_id)\nVALUES\n"

    values = []
    for abonement_id in abonement_ids:
        values.append("  (0, 13483294, 0, {}),".format(abonement_id))
        values.append("  (0, 13459880, 0, {}),".format(abonement_id))

    sql_query += "\n".join(values)
    sql_query = sql_query.rstrip(',') + ";"

    return sql_query

abonement_ids = [597852,
597853,
597856,
597857,
599126
]  # Здесь можно указать нужные abonement_id
sql_query = generate_sql_query(abonement_ids)
print(sql_query)