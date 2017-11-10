def uniqueValues( table):
    for col in table:
        print(col)
        print(table[col].unique())
        print("\n")
