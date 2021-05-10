from datetime import datetime, timedelta

import numpy as np

def sneaker_shops():
    """
    Finds returning customers in the dataset.
    """
    with open('Shopify-F21/W19_DS_Intern_Challenge_Data_Set.csv') as f:
        headers, *data = f.read().split('\n')
    headers = headers.split(',')
    data = [row.split(',') for row in data]
    user_info = {}
    shop_info = {}
    for row in data:
        # Transform variables
        order_id = int(row[0])
        shop_id = int(row[1])
        user_id = int(row[2])
        order_amount = int(row[3])
        # Initialize entries
        if user_id not in user_info:
            user_info[user_id] = {
                'purchase_amt': [],
                'purchase_loc': [],
                'purchase_id': [],
            }
        if shop_id not in shop_info:
            shop_info[shop_id] = {
                'purchase_amt': [],
                'purchase_id': [],
            }
        # Update values
        user_info[user_id]['purchase_amt'].append(order_amount)
        user_info[user_id]['purchase_loc'].append(shop_id)
        user_info[user_id]['purchase_id'].append(order_id)
        shop_info[shop_id]['purchase_amt'].append(order_amount)
        shop_info[shop_id]['purchase_id'].append(order_id)

    # Remove single-purchase users
    user_info = {
        k: v for k, v in user_info.items()
        if len(v['purchase_amt']) > 1
    }
    # Analysis
    stores = {}
    user_outlier_ids = []
    shop_outlier_ids = []
    for user_id, user_details in user_info.items():
        mean = np.mean(user_details['purchase_amt'])
        stdev = np.std(user_details['purchase_amt'])
        three_sigma = int(mean + 3 * stdev)
        extreme_outliers = [
            purchase for purchase in user_details['purchase_amt']
            if purchase > three_sigma
        ]
        for value in extreme_outliers:
            idx = user_details['purchase_amt'].index(value)
            store = user_details['purchase_loc'][idx]
            order_id = user_details['purchase_id'][idx]
            if store not in stores:
                stores[store] = 0
            stores[store] += 1
            user_outlier_ids.append(order_id)
    for shop_id, shop_details in shop_info.items():
        mean = np.mean(shop_details['purchase_amt'])
        stdev = np.std(shop_details['purchase_amt'])
        three_sigma = int(mean + 3 * stdev)
        extreme_outliers = [
            purchase for purchase in shop_details['purchase_amt']
            if purchase > three_sigma
        ]
        for value in extreme_outliers:
            idx = shop_details['purchase_amt'].index(value)
            order_id = shop_details['purchase_id'][idx]
            shop_outlier_ids.append(order_id)
    # print({
    #     k: v for k, v in
    #     sorted(stores.items(), key=lambda item: item[1], reverse=True)
    # })
    # print(sum([v for k, v in stores.items()]))
    # print(sorted(user_outlier_ids))
    # print(sorted(shop_outlier_ids))
    # print()
    print(sorted(set(user_outlier_ids).intersection(set(shop_outlier_ids))))

sneaker_shops()
