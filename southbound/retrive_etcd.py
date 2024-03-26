import etcd3

# Create an instance of Etcd3Client
client = etcd3.client()

def retrieve_data_from_etcd(key):
    # Retrieve data associated with the given key
    value, _ = client.get(key)
    return value.decode() if value else None

if __name__ == "__main__":
    # Example key to retrieve data
    example_key = "hotstar" #One/subnet11/n111"

    # Retrieve data from etcd
    data = retrieve_data_from_etcd(example_key)

    if data:
        print("Retrieved data:")
        print(data)
    else:
        print("Data not found for the given key.")
