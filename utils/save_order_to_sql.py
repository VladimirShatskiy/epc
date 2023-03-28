import os
import json
from config_data.config import BRANCH_PHOTO, CUR, CONNECT_BASE, lock


def list_orders():
    """
    Проверка всех папок вдиректории с заказнаряами. при обнаружени файла с данными переностятся данные в SQL.
    После чего, по SQL бале проверяются всезаказ наряда на наличии папок, техпапок чтонет,
    в SQL ставиться признак закртого заказнаряда
    Так же, проводится проверка наличия папок с номерами заказ нарадов с базой SQL при отсутствии папки SQL ставится
    призак закрытого заказ наряда
    :return:
    """
    list_orders_dict = []

    for item in os.listdir(BRANCH_PHOTO):
        new_way = os.path.join(BRANCH_PHOTO, item)
        if os.path.isdir(new_way):
            file_name = os.path.join(new_way, 'content.txt')
            if os.path.isfile(file_name):
                with open(file_name, 'r', encoding='utf-8') as file_open:
                    data = json.load(file_open)
                list_orders_dict.append(data)

    for item in list_orders_dict:
        with lock:
            data = (item['order'],)
            CUR.execute("""SELECT "order" FROM orders_list WHERE "order" = ? """, data)
        if CUR.fetchone():
            with lock:
                data_for_update = (item['barcode'], item['plate_number'], item['phone'], item['order'], )
                CUR.execute("""UPDATE orders_list 
                SET barcode = ?, 
                    plate_number = ?, 
                    phone = ? 
                    WHERE "order" = ? """, data_for_update)
                CONNECT_BASE.commit()
        else:
            with lock:
                CUR.execute("""INSERT INTO "orders_list"("closed", "order", "phone", "plate_number", "barcode")
                                VALUES (FALSE, ?,?,?,?)""",
                                (item['order'], item['phone'], item['plate_number'], item['barcode'], ))
                CONNECT_BASE.commit()

    orders_list = []
# Перевод статуса заказ нарада в архив

    for item in list_orders_dict:
        orders_list.append(item['order'])

    with lock:
        CUR.execute("""SELECT "order" FROM "orders_list" WHERE "closed" = FALSE""")
        orders_list_sql = CUR.fetchall()

    for item in orders_list_sql:
        order = item[0]
        if order not in orders_list:
            with lock:
                CUR.execute("""UPDATE orders_list SET closed = TRUE WHERE "order" = ?""", (order,))
                CONNECT_BASE.commit()
