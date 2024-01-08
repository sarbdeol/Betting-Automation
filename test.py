import csv



def clear_csv(file_path='sample.csv'):
    with open(file_path, 'w', newline='') as csvfile:
        pass  # The file is opened and closed immediately without writing anything


clear_csv()
