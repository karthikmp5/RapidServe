import etcd3

# Create an instance of Etcd3Client
client = etcd3.client()

# def retrieve_all_data_from_etcd():
#     all_data = {}

#     db = client.get_all()

#     for value, addr in db:
#         value_str = value.decode()
#         print(value_str)

#         # key = 

#     # return all_data


def retrieve_data_from_etcd(key):
    # Retrieve data associated with the given key
    value, _ = client.get(key)
    return value.decode() if value else None

if __name__ == "__main__":
    # Example key to retrieve data
    example_key = "netflix" #One/subnet11/n111"

    # Retrieve data from etcd
    data = retrieve_data_from_etcd(example_key)

    if data:
        print("Retrieved data:")
        print(data)
    else:
        print("Data not found for the given key.")



    # all_data = retrieve_all_data_from_etcd()

    # if all_data:
    #     print("Retrieved data:")
    #     for key, value in all_data.items():
    #         print(f"Key: {key}, Value: {value}")
    # else:
    #     print("No data found in etcd.")
