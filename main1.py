import streamlit as st
import pandas as pd
from tabulate import tabulate

def get_unique_records(records):
    df = pd.DataFrame(records, columns=["Record"])
    df['Record'] = df['Record'].str.lower()  # Convert all records to lowercase
    df = df[df['Record'].notna()]
    unique_records = df.drop_duplicates().reset_index(drop=True)
    return unique_records
def get_duplicate_records(records):
    df = pd.DataFrame(records)
    df = df.dropna()  # Drop rows with NaN values
    duplicate_mask = df.duplicated(keep=False)
    duplicate_records = df[duplicate_mask].reset_index(drop=True)
    print("Duplicate Records:", duplicate_records)  # Debugging statement
    return duplicate_records



def get_record_counts(records):
    record_counts = records['Record'].value_counts().reset_index()
    record_counts.columns = ['Record', 'Count']
    return record_counts

def display_unique_records(unique_records, record_counts):
    st.subheader("Unique Records")
    st.text(tabulate(unique_records, headers='keys', tablefmt='grid'))

    st.subheader("Unique Record Counts")
    st.text(tabulate(record_counts, headers='keys', tablefmt='grid'))

    st.subheader("Justification for Unique Records")
    st.write("A record is considered unique if all its details are distinct from other records.")

def display_duplicate_records(duplicate_records):
    st.subheader("Duplicate Records")
    st.write(duplicate_records)

    st.subheader("Duplicate Record Counts")
    st.write("Total number of duplicate records: ", len(duplicate_records))

    st.subheader("Justification for Duplicate Records")
    st.write("Records are considered duplicates if they have identical content. They may arise due to data entry errors, system glitches, or merging data from multiple sources.")

def main():
    st.title("Unique Record Analyzer")

    st.header("Enter Database Records")
    records_input = st.text_area("Enter records separated by new lines")

    if st.button("Analyze"):
        records = [record.strip() for record in records_input.split('\n') if record.strip()]
        unique_records = get_unique_records(records)
        duplicate_records = get_duplicate_records(records)
        print("Length of Duplicate Records:", len(duplicate_records))  # Debugging statement
        unique_record_counts = get_record_counts(unique_records)
        display_unique_records(unique_records, unique_record_counts)
        if not duplicate_records.empty:
            display_duplicate_records(duplicate_records)



if __name__ == "__main__":
    main()
