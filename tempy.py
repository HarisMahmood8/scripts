if __name__ == "__main__":
    Test_Cases, df = generate_full(environment_precedence)
        
    unique_cases, df_duplicates = remove_duplicates(Test_Cases)
    
    print(f"Number of Unique Test Cases: {len(unique_cases)}")
    
    # Save unique test cases to a separate CSV file
    unique_cases_df = pd.DataFrame(unique_cases)
    unique_cases_df.to_csv("./Unique_Test_Cases.csv", index=False)
    
    # Save duplicate report to "Duplicates_Report.csv" file
    df_duplicates.to_csv("./Duplicates_Report.csv", index=False)
