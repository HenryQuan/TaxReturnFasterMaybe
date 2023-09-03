# Tax Return Faster Maybe?
Extract texts from Bank Statements (PDFs) and find keywords to print out their values or output to a csv file. This works the best if the statement starts with the date (01 Jan/20 Dec) and ends with either the value (1,230.13) or value + balance (5.43 60.00).

## Folder setup
- Place bank statements (PDFs) in `documents/`
- Processed statements will be placed in `processed/`
- Place `keywords.txt` in `config/`

### Config
Keywords are in the following format:
```
WATER
CITY OF SYDNEY
# APPLE
# GOOGLE
```
Any lines starting with `#` will be ignored.
