Sure! Here's a **README.md** file for your AWS Log Groups Inventory script:

---

# **AWS Log Groups Inventory Script**

## **Overview**
This Python script retrieves details of **AWS CloudWatch Log Groups** across multiple regions, organizes the data, and exports it to an **Excel file**. It uses `boto3` to interact with AWS services and `pandas` and `openpyxl` for data handling.

## **Features**
✔ Fetches **log group details** for specified AWS regions  
✔ Records **Log Group Name, Region, Retention Period, Stored Bytes, ARN, Log Class, Creation Time**  
✔ Converts **stored bytes into human-readable format** (KB, MB, GB, etc.)  
✔ Generates a **unique Excel filename** to prevent overwriting  
✔ Uses **multi-threading** to speed up execution across regions  

## **Prerequisites**
Before running the script, ensure you have:
1. **Python** (>= 3.7) installed
2. **AWS CLI** configured with valid credentials (`aws configure`)
3. Required dependencies installed:
   ```bash
   pip install boto3 pandas openpyxl
   ```

## **Usage**
### **1️⃣ Modify AWS Regions**
Update the `regions_to_query` list in the script with the AWS regions you want to scan:
```python
regions_to_query = ['us-east-1', 'us-west-2']
```

### **2️⃣ Run the Script**
Execute the script:
```bash
python script.py
```

### **3️⃣ Output File**
The script creates an **Excel file** with a unique name like:
```
Log_Groups_Inventory.xlsx
```
If a file with the same name already exists, it generates:
```
Log_Groups_Inventory_1.xlsx
Log_Groups_Inventory_2.xlsx
```
etc.

## **Excel File Format**
The generated Excel file contains the following columns:
| Region | Account ID | Log Group Name | ARN | Log Class | Retention | Stored Bytes | Creation Time |
|---------------|--------|------------|-----|-----------|------------------|--------------|---------------------|
| us-east-1 | 123456789 | example-log-group | arn:aws:logs:... | Standard | 30 days | 1.5 MB | 2025-05-20 12:25:00 |

## **Error Handling**
- If a region fails to fetch log groups, it will log the error without stopping execution.
- If no log groups are found, the script will display:
  ```
  No log groups found.
  ```

## **Customization**
- Change the **retention period** or other parameters as needed in the script.
- Modify the **filename format** in `generate_unique_filename()`.

## **License**
This script is free to use and modify as needed.

---

This README file provides instructions on setup, usage, and output details. Let me know if you need any modifications! 🚀📊
