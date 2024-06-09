import pandas as pd
import itertools
import time
import os
# from mlxtend.frequent_patterns import apriori
from apyori import apriori

# Load the dataset      
for dataset_path in os.listdir(os.getcwd()):
    if ".csv" in dataset_path:
        df = pd.read_csv(dataset_path)
        print("For Dataset :",dataset_path)

        # Convert itemsets to lists
        df['itemset'] = df['itemset'].apply(lambda x: x.split(', '))

        def get_frequent_itemsets_brute_force(transactions, min_support):
            transactions = [set(transaction) for transaction in transactions]
            items = set(itertools.chain(*transactions))
            def get_support(itemset):
                return sum(1 for transaction in transactions if itemset.issubset(transaction))
            frequent_itemsets = []
            k = 1
            current_itemsets = [{item} for item in items]
            while current_itemsets:
                next_itemsets = []
                for itemset in current_itemsets:
                    support = get_support(itemset)
                    if support >= min_support:
                        frequent_itemsets.append((itemset, support))
                        for item in items:
                            new_itemset = itemset | {item}
                            if len(new_itemset) == k + 1:
                                next_itemsets.append(new_itemset)
                current_itemsets = next_itemsets
                k += 1
            return frequent_itemsets

        # Define minimum support
        min_support = 2

        # Measure time for brute force method
        start_time = time.time()
        frequent_itemsets_brute_force = get_frequent_itemsets_brute_force(df['itemset'], min_support)
        brute_force_time = time.time() - start_time

        print(f"Brute Force Method Time: {brute_force_time} seconds")
        print(f"Frequent Itemsets (Brute Force): {frequent_itemsets_brute_force}")


        # Convert transactions to list of lists
        transactions = df['itemset'].tolist()

        # Define minimum support proportion
        min_support_proportion = min_support / len(transactions)

        # Measure time for Apriori algorithm
        start_time = time.time()
        frequent_itemsets_apriori = list(apriori(transactions, min_support=min_support_proportion))
        apriori_time = time.time() - start_time

        print(f"Apriori Algorithm Time: {apriori_time} seconds")
        print(f"Frequent Itemsets (Apriori): {frequent_itemsets_apriori}")




        # Extract and format frequent itemsets from brute force method
        brute_force_itemsets = set(frozenset(itemset) for itemset, support in frequent_itemsets_brute_force)

        # Extract and format frequent itemsets from Apriori algorithm
        apriori_itemsets = set(frozenset(item.items) for item in frequent_itemsets_apriori if len(item.items) > 0)

        # Compare the outputs
        print(f"Brute Force Frequent Itemsets: {brute_force_itemsets}")
        print(f"Apriori Frequent Itemsets: {apriori_itemsets}")

        # Check if both methods output the same frequent itemsets
        if brute_force_itemsets == apriori_itemsets:
            print("Both methods produced the same frequent itemsets.")
        else:
            print("The outputs are not the same!")

        print()

        
