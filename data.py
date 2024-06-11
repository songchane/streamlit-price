import requests
import pandas as pd

API_KEY = '6a6f6c57776a6961353445704a6c6b'

def main():
    data = pd.DataFrame()
    page = 1
    while True:
        url = f'http://openAPI.seoul.go.kr:8088/{API_KEY}/json/ListNecessariesPricesService/{(page-1)*1000+1}/{page*1000}'
        print("Fetching data from:", url)
        req = requests.get(url)
        content = req.json()
        rows = content['ListNecessariesPricesService']['row']

        if len(rows) == 0 or len(data) >= 2000:  # Stop if no more data or reached 30,000 rows
            break

        data = pd.concat([data, pd.DataFrame(rows)], ignore_index=True)

        page += 1
    
    if not data.empty:
        # Convert 'P_DATE' column to datetime if necessary
        if 'P_DATE' in data.columns:
            data['P_DATE'] = pd.to_datetime(data['P_DATE'], format=("%Y-%m-%d"))
        data.to_csv('real.csv', index=False)

        print(data.head())
        print("Total rows:", len(data))

if __name__ == "__main__":
    main()
