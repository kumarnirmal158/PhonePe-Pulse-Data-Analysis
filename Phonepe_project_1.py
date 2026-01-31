
import os
import pandas as pd
import json
import sqlite3


# 1️⃣ Aggregated Transaction

path= "C:/Program Files/pulse/data/aggregated/transaction/country/india/state/"
Agg_state_list = os.listdir(path)

tab_1 = {'State':[],'Year':[],'quarter':[],'Transaction_type':[],'Transaction_count':[],'Transaction_amount':[]}

for i in Agg_state_list:
     p_i=path+i+"/"
     Agg_yr=os.listdir(p_i)
     for j in Agg_yr:
         p_j=p_i+j+"/"
         Agg_yr_list=os.listdir(p_j)
         for k in Agg_yr_list:
             p_k=p_j+k
             try:
                  with open(p_k, 'r') as Data:
                        D = json.load(Data)
                        data = D.get('data')
                        for z in D['data']['transactionData']:
                            count = z['paymentInstruments'][0]['count']
                            amount = z['paymentInstruments'][0]['amount']
                            tab_1['Transaction_type'].append(z.get('name'))
                            tab_1['Transaction_count'].append(count)
                            tab_1['Transaction_amount'].append(amount)
                            tab_1['State'].append(i)
                            tab_1['Year'].append(j)
                            tab_1['quarter'].append(int(k.strip('.json')))

             except Exception as e:
                        print(f"Error reading {p_k}: {e}")

#Succesfully created a dataframe
Agg_Tran=pd.DataFrame(tab_1)


# 2️⃣ Aggregated User

path="C:/Program Files/pulse/data/aggregated/user/country/india/state/"
user_state_list = os.listdir(path)

tab_2 = {'State': [], 'Year': [], 'quarter': [], 'Transaction_brand': [], 'Transaction_count': [], 'Transaction_percentage': []}

for i in user_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            try:
                with open(p_k, 'r') as Data:
                    D = json.load(Data)

                    data = D.get('data')
                    if data is not None:
                        users = data.get('usersByDevice')
                        if users:
                            for z in users:
                                brand = z.get('brand')
                                count = z.get('count')
                                percentage = z.get('percentage')
                                if brand is not None and count is not None and percentage is not None:
                                    tab_2['State'].append(i)
                                    tab_2['Year'].append(j)
                                    tab_2['quarter'].append(int(k.strip('.json')))
                                    tab_2['Transaction_brand'].append(brand)
                                    tab_2['Transaction_count'].append(count)
                                    tab_2['Transaction_percentage'].append(percentage)
            except Exception as e:
                print(f"Error in file {p_k}: {e}")

# Create DataFrame
Agg_user = pd.DataFrame(tab_2)


# 3️⃣ Aggregated Insurance

path = "C:/Program Files/pulse/data/aggregated/insurance/country/india/state/"
ins_state_list = os.listdir(path)

tab_3 = {'State':[], 'Year':[], 'quarter':[],  'Transaction_type':[],  'Transaction_count':[],  'Transaction_amount':[]}

for i in ins_state_list:
     p_i=path+i+"/"
     Agg_yr=os.listdir(p_i)
     for j in Agg_yr:
         p_j=p_i+j+"/"
         Agg_yr_list=os.listdir(p_j)
         for k in Agg_yr_list:
             p_k=p_j+k
             try:
                  with open(p_k, 'r') as Data:
                        D = json.load(Data)
                        data = D.get('data')
                        for z in D['data']['transactionData']:
                            count = z['paymentInstruments'][0]['count']
                            amount = z['paymentInstruments'][0]['amount']
                            tab_3['Transaction_type'].append(z.get('name'))
                            tab_3['Transaction_count'].append(count)
                            tab_3['Transaction_amount'].append(amount)
                            tab_3['State'].append(i)
                            tab_3['Year'].append(j)
                            tab_3['quarter'].append(int(k.strip('.json')))

             except Exception as e:
                        print(f"Error reading {p_k}: {e}")
# Create DataFrame
Agg_ins = pd.DataFrame(tab_3)




# 4️⃣ map transaction

path="C:/Program Files/pulse/data/map/transaction/hover/country/india/state/"
map_state_list = os.listdir(path)

tab_4 = {'State': [], 'Year': [], 'quarter': [], 'Transaction_type': [], 'Transaction_district': [], 'Transaction_count': [], 'Transaction_amount': []}

for i in map_state_list:
    p_i=path+i+"/"
    map_yr=os.listdir(p_i)
    for j in map_yr:
        p_j=p_i+j+"/"
        map_yr_list=os.listdir(p_j)
        for k in map_yr_list:
            p_k=p_j+k
            try:
                  with open(p_k, 'r') as Data:
                        D = json.load(Data)
                        for z in D['data']['hoverDataList']:
                          name = z['name']    
                          ttype = z['metric'][0]['type']
                          count = z['metric'][0]['count']
                          amount = z['metric'][0]['amount']
                          tab_4['Transaction_district'].append(name)
                          tab_4['Transaction_type'].append(ttype)
                          tab_4['Transaction_count'].append(count)
                          tab_4['Transaction_amount'].append(amount)
                          tab_4['State'].append(i)
                          tab_4['Year'].append(j)
                          tab_4['quarter'].append(int(k.strip('.json')))
            except Exception as e:
                        print(f"Error reading {p_k}: {e}")

# Create DataFrame
map_trans=pd.DataFrame(tab_4)


# 5️⃣ map user

path="C:/Program Files/pulse/data/map/user/hover/country/india/state/"
mapuser_state_list = os.listdir(path)

tab_5 = {'State': [], 'Year': [], 'quarter': [], 'District': [],'Registered_user': [], 'App_opening': []}

for i in mapuser_state_list:
    p_i = path+i+"/"
    year = os.listdir(p_i)
    for j in year:
        p_j = p_i+j+"/"
        file = os.listdir(p_j)
        for k in file:
            p_k = p_j+k
            Data = open(p_k, 'r')
            D = json.load(Data)
            try:
                for z in D['data']["hoverData"]:
                    district = z
                    registered_user =  D['data']["hoverData"][z]["registeredUsers"]
                    app_opening = D['data']["hoverData"][z]["appOpens"]
                    tab_5['District'].append(district)
                    tab_5['Registered_user'].append(registered_user)
                    tab_5['App_opening'].append(app_opening)
                    tab_5['State'].append(i)
                    tab_5['Year'].append(j)
                    tab_5['quarter'].append(int(k.strip('.json')))
            except Exception as e:
              print(f"Error in file {p_k}: {e}")

# Create DataFrame
map_users = pd.DataFrame(tab_5)


# 6️⃣ map insurance

path = "C:/Program Files/pulse/data/map/insurance/hover/country/india/state/"
map_ins_state_list = os.listdir(path)

tab_6 = {'State':[], 'Year':[],'quarter':[],'User_District':[], 'Transaction_count':[], 'Transaction_amount':[]}

for i in map_ins_state_list:
     p_i=path+i+"/"
     Agg_yr=os.listdir(p_i)
     for j in Agg_yr:
         p_j=p_i+j+"/"
         Agg_yr_list=os.listdir(p_j)
         for k in Agg_yr_list:
             p_k=p_j+k
             try:
                  with open(p_k, 'r') as Data:
                        D = json.load(Data)
                        for z in D['data']['hoverDataList']:
                               count = z['metric'][0]['count']
                               amount = z['metric'][0]['amount']
                               tab_6['User_District'].append(z.get('name'))
                               tab_6['Transaction_count'].append(count)
                               tab_6['Transaction_amount'].append(amount)
                               tab_6['State'].append(i)
                               tab_6['Year'].append(j)
                               tab_6['quarter'].append(int(k.strip('.json')))
             except Exception as e:
                       print(f"Error in file {p_k}: {e}")
            
# Create DataFrame
map_ins = pd.DataFrame(tab_6)



# 7️⃣ Top Transaction

path= "C:/Program Files/pulse/data/top/transaction/country/india/state/" 
top_trans_state_list = os.listdir(path)

tab_7 = {'State': [], 'Year': [], 'quarter': [], 'Transaction_type': [],'Level': [], 'Name': [], 
         'Transaction_count': [], 'Transaction_amount': []}

for i in top_trans_state_list:
    p_i=path+i+"/"
    top_trans_yr=os.listdir(p_i)
    for j in top_trans_yr:
        p_j=p_i+j+"/"
        top_trans_yr_list=os.listdir(p_j)
        for k in top_trans_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['districts']:
              name = z['entityName']
              mtype = z['metric']['type']
              count = z['metric']['count']
              amount = z['metric']['amount']
              tab_7['Level'].append('District')
              tab_7['Name'].append(name)
              tab_7['Transaction_type'].append(mtype)
              tab_7['Transaction_count'].append(count)
              tab_7['Transaction_amount'].append(amount)
              tab_7['State'].append(i)
              tab_7['Year'].append(j)
              tab_7['quarter'].append(int(k.strip('.json')))

            for z in D['data']['pincodes']:
              name = z['entityName']
              mtype = z['metric']['type']
              count = z['metric']['count']
              amount = z['metric']['amount']
              tab_7['Level'].append('Pincode')
              tab_7['Name'].append(name)
              tab_7['Transaction_type'].append(mtype)
              tab_7['Transaction_count'].append(count)
              tab_7['Transaction_amount'].append(amount)
              tab_7['State'].append(i)
              tab_7['Year'].append(j)
              tab_7['quarter'].append(int(k.strip('.json')))


# Create DataFrame
top_trans = pd.DataFrame(tab_7)


# 8️⃣ top user

path= "C:/Program Files/pulse/data/top/user/country/india/state/" 
top_users_state_list = os.listdir(path)

tab_8  = {'State': [], 'Year': [], 'quarter': [], 'registeredusers': [], 'Level': [], 'Name': []}

for i in top_users_state_list:
    p_i=path+i+"/"
    top_users_yr=os.listdir(p_i)
    for j in top_users_yr:
        p_j=p_i+j+"/"
        top_users_yr_list=os.listdir(p_j)
        for k in top_users_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['districts']:
              name = z['name']
              registeredusers = z['registeredUsers']
              tab_8 ['registeredusers'].append(registeredusers)
              tab_8 ['Level'].append('District')
              tab_8 ['Name'].append(name)
              tab_8 ['State'].append(i)
              tab_8 ['Year'].append(j)
              tab_8 ['quarter'].append(int(k.strip('.json')))
            for z in D['data']['pincodes']:
              name = z['name']
              registeredusers = z['registeredUsers']
              tab_8 ['registeredusers'].append(registeredusers)
              tab_8 ['Level'].append('Pincode')
              tab_8 ['Name'].append(name)
              tab_8 ['State'].append(i)
              tab_8 ['Year'].append(j)
              tab_8 ['quarter'].append(int(k.strip('.json')))  

# Create DataFrame
top_user = pd.DataFrame(tab_8)


# 9️⃣ Top Insurance

path = "C:/Program Files/pulse/data/top/insurance/country/india/state/" 
top_ins_state_list= os.listdir(path)

tab_9 = {'State': [], 'Year': [], 'quarter': [], 'Level': [], 'Name': [], 'Transaction_Count': [], 'Transaction_Amount': [] }

for i in top_ins_state_list:
     p_i=path+i+"/"
     Agg_yr=os.listdir(p_i)
     for j in Agg_yr:
         p_j=p_i+j+"/"
         Agg_yr_list=os.listdir(p_j)
         for k in Agg_yr_list:
             p_k=p_j+k
             try:
                 with open(p_k, 'r') as Data:
                        D = json.load(Data)
                        for z in D['data']['districts']:
                            count = z['metric']['count']
                            amount = z['metric']['amount']
                            name = z.get('entityName')
                            tab_9['Transaction_Count'].append(count)
                            tab_9['Transaction_Amount'].append(amount)
                            tab_9['Level'].append('District')
                            tab_9['Name'].append(name)
                            tab_9['State'].append(i)
                            tab_9['Year'].append(j)
                            tab_9['quarter'].append(int(k.strip('.json')))
                        for z in D['data']['pincodes']:
                            count = z['metric']['count']
                            amount = z['metric']['amount']
                            name = z.get('entityName')
                            tab_9['Level'].append('Pincode')
                            tab_9['Name'].append(name)
                            tab_9['Transaction_Count'].append(count)
                            tab_9['Transaction_Amount'].append(amount)
                            tab_9['State'].append(i)
                            tab_9['Year'].append(j)
                            tab_9['quarter'].append(int(k.strip('.json')))
             except Exception as e: 
                       print(f"Error in file {p_k}: {e}")                       

# Create DataFrame
top_ins = pd.DataFrame(tab_9)


import sqlite3

# Connect to SQLite (This will create a new database file if it doesn't exist)
connection = sqlite3.connect("Phonepe_project.db")
 # Creates a database file 'my_database.db'


 # Create a cursor object
cursor = connection.cursor()

# 1️⃣ aggregated transaction

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS Agg_Tran (State VARCHAR(100), Year INT, quarter INT, 
               Transaction_type VARCHAR(100), Transaction_count INT, Transaction_amount INT)''')

# insert values in tables
for index , row in Agg_Tran.iterrows():
    cursor.execute("""INSERT INTO Agg_Tran (State,Year,quarter,Transaction_type,Transaction_count,Transaction_amount)
                     VALUES (?,?,?,?,?,?)""",(row["State"], row["Year"], row["quarter"], row["Transaction_type"], 
                                              row["Transaction_count"], row["Transaction_amount"]))



# 2️⃣ Aggregated User

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS Agg_user (State VARCHAR(100), Year INT, quarter INT,
                    Transaction_brand VARCHAR(100), Transaction_count INT, Transaction_percentage float)''')

# insert values in tables
for index , row in Agg_user.iterrows():
   cursor.execute("""INSERT INTO Agg_user (State,Year,quarter,Transaction_brand,Transaction_count,Transaction_percentage)
                     VALUES (?,?,?,?,?,?)""",(row["State"], row["Year"], row["quarter"], row["Transaction_brand"], 
                                              row["Transaction_count"],row["Transaction_percentage"]))


# 3️⃣ Aggregated Insurance

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS Agg_ins (State VARCHAR(100), Year INT, quarter INT, Transaction_type VARCHAR(100),
                  Transaction_count INT, Transaction_amount INT)''')

# insert values in tables
for index , row in Agg_ins.iterrows():
    cursor.execute("""INSERT INTO Agg_ins (State,Year,quarter,Transaction_type,Transaction_count,Transaction_amount)
                     VALUES (?,?,?,?,?,?)""",(row["State"], row["Year"], row["quarter"], row["Transaction_type"], 
                                              row["Transaction_count"],row["Transaction_amount"]))


# 4️⃣ map transaction

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS map_trans (State VARCHAR(100), Year INT, quarter INT, Transaction_type VARCHAR(100),
                  Transaction_district VARCHAR(100),Transaction_count INT, Transaction_amount INT)''')
# insert values in tables
for index , row in map_trans.iterrows():
    cursor.execute("""INSERT INTO map_trans (State,Year,quarter,Transaction_type,Transaction_district, Transaction_count,Transaction_amount)
                     VALUES (?,?,?,?,?,?,?)""",(row["State"], row["Year"], row["quarter"], row["Transaction_type"], row["Transaction_district"],
                     row["Transaction_count"], row["Transaction_amount"]))


# 5️⃣ map user

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS map_users (State VARCHAR(100), Year INT, quarter INT,
                  District VARCHAR(100),Registered_user INT, App_opening INT)''')

# insert values in tables
for index , row in map_users.iterrows():
    cursor.execute("""INSERT INTO map_users (State,Year,quarter,District,Registered_user, App_opening)
                     VALUES (?,?,?,?,?,?)""",(row["State"], row["Year"], row["quarter"], row["District"], 
                                              row["Registered_user"],row["App_opening"]))


# 6️⃣ map insurance

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS map_ins (State VARCHAR(100), Year INT, quarter INT,
                  User_District VARCHAR(50),Transaction_count INT,  Transaction_amount FLOAT)''')

# insert values in tables
for index , row in map_ins.iterrows():
    cursor.execute("""INSERT INTO map_ins (State,Year,quarter,User_District,Transaction_count, Transaction_amount)
                     VALUES (?,?,?,?,?,?)""",(row["State"], row["Year"], row["quarter"], row["User_District"], 
                                              row["Transaction_count"],row["Transaction_amount"]))


# 7️⃣ Top Transaction

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS top_trans (State VARCHAR(100), Year INT, quarter INT, Transaction_type VARCHAR(100),
                  Level VARCHAR(100),Name VARCHAR(100),Transaction_count INT, Transaction_amount INT)''')

# insert values in tables
for index , row in top_trans.iterrows():
    cursor.execute("""INSERT INTO top_trans (State,Year,quarter,Transaction_type,Level,Name, Transaction_count,Transaction_amount)
                     VALUES (?,?,?,?,?,?,?,?)""",(row["State"], row["Year"], row["quarter"], row["Transaction_type"], row["Level"],
                     row["Name"],row["Transaction_count"], row["Transaction_amount"]))


# 8️⃣ top user

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS top_users (State VARCHAR(100), Year INT, quarter INT,
                  registeredusers INT, Level VARCHAR(100), Name VARCHAR(100))''')

# insert values in tables
for index , row in top_user.iterrows():
    cursor.execute("""INSERT INTO top_users (State,Year,quarter,registeredusers, Level, Name)
                     VALUES (?,?,?,?,?,?)""",(row["State"], row["Year"], row["quarter"], row["registeredusers"],
                                                 row["Level"], row["Name"]))

# 9️⃣ Top Insurance

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS top_ins (State VARCHAR(100), Year INT, quarter INT,
                  Level VARCHAR(100),Name VARCHAR(100), Transaction_Count INT,  Transaction_Amount FLOAT)''')

# insert values in tables
for index , row in top_ins.iterrows():
    cursor.execute("""INSERT INTO top_ins (State,Year,quarter,Level,Name,Transaction_Count, Transaction_Amount)
                     VALUES (?,?,?,?,?,?,?)""",(row["State"], row["Year"], row["quarter"], row["Level"], row["Name"],
                      row["Transaction_Count"], row["Transaction_Amount"]))

# Commit the changes (required to save)
connection.commit()







