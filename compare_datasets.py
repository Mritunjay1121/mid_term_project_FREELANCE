import csv
import itertools
import time
import os

# Function to read the dataset and convert itemsets to lists
def read_dataset(dataset_path):
    transactions = []
    with open(dataset_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            itemset = row['itemset'].split(', ')
            transactions.append(itemset)
    return transactions

# Brute force method to find frequent itemsets
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

# Apriori algorithm implemented from scratch
def get_frequent_itemsets_apriori(transactions, min_support):
    transactions = [set(transaction) for transaction in transactions]
    items = set(itertools.chain(*transactions))

    def get_support(itemset):
        return sum(1 for transaction in transactions if itemset.issubset(transaction))

    def join_sets(itemsets, length):
        return set([frozenset(i.union(j)) for i in itemsets for j in itemsets if len(i.union(j)) == length])

    frequent_itemsets = []
    k = 1
    current_itemsets = [frozenset([item]) for item in items if get_support(frozenset([item])) >= min_support]
    while current_itemsets:
        frequent_itemsets.extend([(itemset, get_support(itemset)) for itemset in current_itemsets])
        current_itemsets = join_sets(current_itemsets, k + 1)
        current_itemsets = [itemset for itemset in current_itemsets if get_support(itemset) >= min_support]
        k += 1
    return frequent_itemsets

# Function to generate association rules from frequent itemsets
def generate_association_rules(frequent_itemsets, transactions, min_confidence):
    rules = []
    for itemset, support in frequent_itemsets:
        if len(itemset) > 1:
            for antecedent in itertools.chain.from_iterable(itertools.combinations(itemset, r) for r in range(1, len(itemset))):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                if consequent:
                    antecedent_support = sum(1 for transaction in transactions if antecedent.issubset(transaction))
                    confidence = support / antecedent_support
                    if confidence >= min_confidence:
                        rules.append((antecedent, consequent, support, confidence))
    return rules

# Main function to compare brute force and apriori algorithm
for dataset_path in os.listdir(os.getcwd()):
    if ".csv" in dataset_path:
        transactions = read_dataset(dataset_path)
        print("For Dataset:", dataset_path)

        min_support = 2
        min_confidence = 0.6

        # Brute force method
        start_time = time.time()
        frequent_itemsets_brute_force = get_frequent_itemsets_brute_force(transactions, min_support)
        brute_force_time = time.time() - start_time

        print(f"Brute Force Method Time: {brute_force_time} seconds")
        print(f"Frequent Itemsets (Brute Force): {frequent_itemsets_brute_force}")

        # Apriori algorithm
        start_time = time.time()
        frequent_itemsets_apriori = get_frequent_itemsets_apriori(transactions, min_support)
        apriori_time = time.time() - start_time

        print(f"Apriori Algorithm Time: {apriori_time} seconds")
        print(f"Frequent Itemsets (Apriori): {frequent_itemsets_apriori}")

        # Extract and format frequent itemsets
        brute_force_itemsets = set(frozenset(itemset) for itemset, support in frequent_itemsets_brute_force)
        apriori_itemsets = set(frozenset(itemset) for itemset, support in frequent_itemsets_apriori)

        # Compare the outputs
        print(f"Brute Force Frequent Itemsets: {brute_force_itemsets}")
        print(f"Apriori Frequent Itemsets: {apriori_itemsets}")

        # Check if both methods output the same frequent itemsets
        if brute_force_itemsets == apriori_itemsets:
            print("Both methods produced the same frequent itemsets.")
        else:
            print("The outputs are not the same!")

        # Generate and compare association rules
        association_rules_brute_force = generate_association_rules(frequent_itemsets_brute_force, transactions, min_confidence)
        association_rules_apriori = generate_association_rules(frequent_itemsets_apriori, transactions, min_confidence)

        print("Association Rules (Brute Force):")
        for antecedent, consequent, support, confidence in association_rules_brute_force:
            print(f"Rule: {set(antecedent)} => {set(consequent)}, Support: {support}, Confidence: {confidence}")

        print("Association Rules (Apriori):")
        for antecedent, consequent, support, confidence in association_rules_apriori:
            print(f"Rule: {set(antecedent)} => {set(consequent)}, Support: {support}, Confidence: {confidence}")

        # Check if both methods output the same association rules
        brute_force_rules = set((frozenset(antecedent), frozenset(consequent), support, confidence) for antecedent, consequent, support, confidence in association_rules_brute_force)
        apriori_rules = set((frozenset(antecedent), frozenset(consequent), support, confidence) for antecedent, consequent, support, confidence in association_rules_apriori)

        if brute_force_rules == apriori_rules:
            print("Both methods produced the same association rules.")
        else:
            print("The outputs are not the same!")

        print()
