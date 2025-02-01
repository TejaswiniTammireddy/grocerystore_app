from datetime import datetime
from sql_connection import get_sql_connection
def insert_order(connection,order):
    cursor = connection.cursor()
    order_query=("insert into orders"
                 "(customer_name,total, datetime) "
                 "values (%s,%s,%s)")
    order_data=(order['customer_name'],float(order['grand_total']),datetime.now())
    cursor.execute(order_query,order_data)
    order_id=(cursor.lastrowid)
    order_details_query=("insert into order_details"
                 "(order_id,product_id,quantity,total_price) "
                 "values (%s,%s,%s,%s)")
    order_details_data=[]
    for order_detail_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_detail_record['product_id']),
            float(order_detail_record['quantity']),
            float(order_detail_record['total_price'])
        ])
    cursor.executemany(order_details_query, order_details_data)
    connection.commit()
    return order_id
def get_all_orders(connection):
    cursor = connection.cursor()
    query= ("select * from orders")
    cursor.execute(query)
    response = []
    for (order_id,customer_name,total,datetime) in cursor:
        response.append({
            'order_id':order_id,
            'customer_name':customer_name,
            'total': total,
            'datetime':datetime
        })
    return response

if __name__=="__main__":
    connection = get_sql_connection()
    print(get_all_orders(connection))