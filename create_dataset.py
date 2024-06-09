import pandas as pd
import random 

items = [
    "Diapers", "Clothes", "Bread", "Milk", "Eggs", "Cheese", "Butter", "Chicken", "Beef", "Fish",
    "Apples", "Bananas", "Oranges", "Grapes", "Carrots", "Potatoes", "Tomatoes", "Lettuce", "Cereal",
    "Rice", "Pasta", "Canned Beans", "Soap", "Shampoo", "Toothpaste", "Detergent", "Paper Towels",
    "Toilet Paper", "Dish Soap", "Coffee"]


for i in range(5):
    l1=[]
    trans=[]
    nums=[1,2,3,4,5]
    for n in range(20):
        l2=[]
        
        number=random.choice(nums)
        for n in range(number):
            l2.append(random.choice(items))
        l1.append(l2)
        trans.append(f"T{n+1}")
    df=pd.DataFrame({"transaction":trans,"itemset":l1})
    df.to_csv(f"dataset{i+1}.csv",index=False)
    
    print(df)
    print()

