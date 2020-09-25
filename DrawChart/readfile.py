import pandas as pd

def main():
    df = pd.read_csv('../data/health_data.csv')
    cols  = df.columns
    for col in cols:
        print(col)
if __name__ == '__main__':
    main()