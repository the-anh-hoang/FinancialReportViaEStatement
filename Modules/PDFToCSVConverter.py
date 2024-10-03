import pdfplumber
import pandas as pd
import re

# Parse a line of transaction into a python string list
def parse_line(line):
    # components to parse
    date, description, withdrawals, deposits, balance = None, None, None, None, None
    transaction_components = line.split()

    for month in ['Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        if month in transaction_components[0]:
            date = transaction_components[0]
            transaction_components = transaction_components[1:]
        else:
            date = "NA"
    for component_index in range(len(transaction_components)):
        if transaction_components[component_index][0].isdigit():
            description = " ".join(transaction_components[0:component_index-1])
            withdrawals = transaction_components[component_index]

    return [date, description, withdrawals]


# Check if line have withdrawal amount
def contain_value(line):
    pattern = '\d+\.\d{2}'
    return re.search(pattern, line)


with pdfplumber.open("Data/TestStatement.pdf") as pdf:
    data = []

    for page in pdf.pages:
        start = False
        skip_next_line = False
        linesInOnePage = page.extract_text().split("\n")

        for line_index in range(len(linesInOnePage)):
            if skip_next_line:
                skip_next_line = False
                continue

            line = linesInOnePage[line_index]

            if start and 'OpeningBalance' not in line:

                print("----------------")
                # Processing one transaction by parsing date, description, and balance
                print(line)
                # If the line does not contain value, join with the next line, completing the transaction
                if not contain_value(line):
                    line += " " + linesInOnePage[line_index + 1]
                    skip_next_line = True
                transaction = parse_line(line)
                data.append(transaction)

            # Start parsing if reached transaction part
            if line == "Date Description Withdrawals($) Deposits($) Balance($)":
                start = True
                continue

            # Stop when end of file
            if "ClosingBalance" in line:
                break

    # df = pd.DataFrame(data, columns=["Date", "Description", "Withdrawals($)", "Deposits($)", "Balance($)"])
    # print(df)
