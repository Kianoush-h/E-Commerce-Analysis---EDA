
"""
@author: Kianoush 

GitHUb: https://github.com/Kianoush-h
YouTube: https://www.youtube.com/channel/UCvf9_53f6n3YjNEA4NxAkJA
LinkedIn: https://www.linkedin.com/in/kianoush-haratiannejadi/

Email: haratiank2@gmail.com

"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import conda
from mpl_toolkits.basemap import Basemap




# =============================================================================
# Geo Exploratory
# =============================================================================

geo_data = pd.read_csv('data/olist_geolocation_dataset.csv')

head = geo_data.head(10)


lat = geo_data['geolocation_lat']
lon = geo_data['geolocation_lng']

plt.figure(figsize=(10,10))

m = Basemap(llcrnrlat=-55.401805,llcrnrlon=-92.269176,urcrnrlat=13.884615,urcrnrlon=-27.581676)
m.bluemarble()
m.drawmapboundary(fill_color='#46bcec') # Make your map into any style you like
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec') # Make your map into any style you like
m.drawcountries()
m.scatter(lon, lat,zorder=10,alpha=0.5,color='tomato')



plt.figure(figsize=(10,10))
sns.countplot(x ='geolocation_state', data = geo_data, 
              order = geo_data['geolocation_state'].value_counts().sort_values().index, 
              palette='icefire_r')




# =============================================================================
# Data Exploratory
# =============================================================================

order_data = pd.read_csv('data/olist_orders_dataset.csv')

order_data.isnull().sum()

order_data_head = order_data.head(10)


# =============================================================================
# PART 1: Feature Enginering with Time
# =============================================================================

'''' Since, missing values' proportion is around 3%, 
Null Values from customer date feature will be filled with forward-fill method.
 This method, propagate the previous value forward'''
 
 
order_data['order_delivered_customer_date'] = order_data['order_delivered_customer_date'].fillna(method='ffill')
order_data['order_delivered_customer_date'].isnull().sum()

# Delivered time and Estimate time features will be created.

order_data['delivered_time'] = pd.to_datetime(order_data['order_delivered_customer_date'], format='%Y-%m-%d').dt.date
order_data['estimate_time'] = pd.to_datetime(order_data['order_estimated_delivery_date'], format='%Y-%m-%d').dt.date

# Weekly feature created based on order delivered customer date

order_data['weekly'] = pd.to_datetime(order_data['order_delivered_customer_date'], format='%Y-%m-%d').dt.week

# Yearly feature created based on order delivered customer date

order_data['yearly'] = pd.to_datetime(order_data['order_delivered_customer_date']).dt.to_period('M')
order_data['yearly'] = order_data['yearly'].astype(str)


# Finding different days of delivered and estimated times.

order_data['diff_days'] = order_data['delivered_time'] - order_data['estimate_time']
order_data['diff_days'] = order_data['diff_days'].dt.days





plt.figure(figsize=(20,10))
sns.lineplot(x='weekly', y='diff_days', data=order_data, color="coral", linewidth=5,
            markers=True,dashes=False, estimator='mean')

plt.xlabel("Weeks", size=14)
plt.ylabel("Difference Days", size=14)
plt.title("Average Difference Days per Week",size=15, weight='bold')





# =============================================================================
# PART 2: Customer Top 10 Product
# =============================================================================


# Upload Olist_Order_Items and Product Data
order_item_data = pd.read_csv('data/olist_order_items_dataset.csv')
products_data = pd.read_csv('data/olist_products_dataset.csv')

# Merge data
total_orders = pd.merge(order_data, order_item_data)
product_orders = pd.merge(total_orders,products_data, on="product_id")
product_orders.info()


# Since the product_id value name is long, it needed to be shortened to make an analysis. 
# With taking the last eight characters, uniqueness preserved.

product_orders['product_id_shorten'] = product_orders['product_id'].str[-8:]



#Plotting Top 10 Products
plt.figure(figsize=(20,10))
sns.countplot(x='product_id_shorten', data=product_orders, palette='gist_earth',
             order=product_orders['product_id_shorten'].value_counts()[:10]\
             .sort_values().index).set_title("Top 10 Products", fontsize=15,
                                             weight='bold')


product_orders.groupby(["product_category_name"])["product_id_shorten"].count().sort_values(ascending=False).head(10)


group_category = product_orders.groupby(['product_id_shorten','product_category_name',])['product_id_shorten'].count().sort_values(ascending=False).head(10)

print(group_category)




# =============================================================================
# PART 3: Top 10 Seller 
# =============================================================================

sellers_data = pd.read_csv('data/olist_sellers_dataset.csv')

# First seller dataset will be merged with the product orders data.

seller_products = pd.merge(product_orders, sellers_data, on="seller_id")
seller_products.info()



seller_products['seller_id_shorten'] = seller_products['seller_id'].str[-6:]



plt.figure(figsize=(20,10))
seller_products['seller_id_shorten'].value_counts()[:10].plot.pie(autopct='%1.1f%%', shadow=True, startangle=90, cmap='tab20')
plt.title("Top 10 Seller",size=14, weight='bold')




'''
Assuming for the orders' product category of these sellers, we can use 'product category' values. 
Below table shows the Top 10 sellers category, and since they can sell multiple product types, 
 garden tools are the most selling product of the best seller.
'''


seller_category = seller_products.groupby(['seller_id_shorten', 'product_category_name'])['seller_id_shorten'].count().sort_values(ascending=False).head(10)
seller_category




f, (ax1, ax2) = plt.subplots(2, 1, figsize=(20,15))
group_category.plot.barh(ax=ax1, cmap='summer')
seller_category.plot.barh(ax=ax2, cmap='autumn')

ax1.set_title('Top10 Product', fontweight='bold')
ax2.set_title('Top10 Seller', fontweight='bold')

ax1.set_xlabel('Count', fontsize=15)
ax1.set_ylabel('Product Name', fontsize=15)
ax1.xaxis.set_tick_params(labelsize=12)
ax1.yaxis.set_tick_params(labelsize=15)

ax2.set_xlabel('Count', fontsize=15)
ax2.set_ylabel('Product Name', fontsize=15)
ax2.xaxis.set_tick_params(labelsize=12)
ax2.yaxis.set_tick_params(labelsize=15)




















