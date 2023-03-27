import os
import json
from config_data.config import BRANCH_PHOTO, CUR, CONNECT_BASE, lock


def list_orders():
    """
    Проверка всех папок вдиректории с заказнаряами. при обнаружени файла с данными переностятся данные в SQL.
    после чего, по SQL бале проверяются всезаказ наряда на наличии папок, техпапок чтонет,
    в SQL ставиться признак закртого заказнаряда
    :return:
    """
    for item in os.listdir(BRANCH_PHOTO):
        way = os.path.join(BRANCH_PHOTO, item)

        if os.path.isdir(way):
            file_name = os.path.join(way, 'content.txt')
            if os.path.isfile(file_name):
                with open(file_name, 'r') as file_open:
                    data = json.load(file_open)

                data_for_sql = (data['order'],)
                # with lock:
                CUR.execute("""SELECT "order" FROM orders_list WHERE "order" = ? """, data_for_sql)
                ord=CUR.fetchall()

                if ord == []:
                    print('insert')
                    # with lock:
                    CUR.execute("""INSERT INTO "orders_list"("closed", "order", "phone", "plate_number", "barcode") 
                                    VALUES (FALSE, ?,?,?,?)""",
                                    (data['order'], data['phone'], data['plate_number'], data['barcode'], ))
                    CONNECT_BASE.commit()
                else:
                    print('Update')
                    data_for_update = (data['barcode'], data['order'], )
                    # with lock:
                    CUR.execute("""UPDATE orders_list SET barcode = ? WHERE "order" = ? """, data_for_update)
                    CONNECT_BASE.commit()
                    print(data['plate_number'], data['phone'], data['barcode'], data['order'])

    # Проверка заказ нарядов на закрытие

    # with lock:
    data = CUR.execute("""SELECT "order" FROM orders_list """)

    order_list = data.fetchall()
    print(order_list)
    for item in order_list:
        print(item)
        order = item[0]
        if not os.path.isdir(os.path.join(BRANCH_PHOTO, order)):
            # with lock:
            CUR.execute("""UPDATE "orders_list" SET closed = TRUE WHERE "order" = ?""", (order,))
            CONNECT_BASE.commit()

