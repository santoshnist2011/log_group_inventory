import boto3
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from openpyxl import Workbook
from openpyxl.styles import Alignment


def convert_bytes(size_in_bytes):
    """
    Convert bytes into a human-readable format (Bytes, KB, MB, GB, TB, PB).
    """
    if size_in_bytes == 0:
        return "0 Bytes"

    size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB")
    i = int((len(str(size_in_bytes)) - 1) // 3)
    p = 1024 ** i
    s = round(size_in_bytes / p, 2)
    return f"{s} {size_name[i]}"


def fetch_log_groups(region, account_id):
    client = boto3.client('logs', region_name=region)
    log_groups = []

    paginator = client.get_paginator('describe_log_groups')
    for page in paginator.paginate():
        for log_group in page['logGroups']:
            log_groups.append({
                'Region': region,
                'Account ID': account_id,
                'LogGroup Name': log_group['logGroupName'],
                'ARN': log_group['arn'],
                'Log Class': log_group.get('kmsKeyId', 'Standard'),
                'Retention': log_group.get('retentionInDays', 'Never'),
                'Stored bytes': log_group['storedBytes'],  # Keep raw bytes for sorting
                'Stored bytes formatted': convert_bytes(log_group['storedBytes']),
                'Creation time': datetime.fromtimestamp(log_group['creationTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            })
    return log_groups


def generate_unique_filename(base_filename='log_groups_inventory.xlsx'):
    counter = 1
    filename, extension = os.path.splitext(base_filename)
    new_filename = base_filename

    while os.path.exists(new_filename):
        new_filename = f"{filename}_{counter}{extension}"
        counter += 1

    return new_filename


def save_to_excel(log_groups, filename):
    df = pd.DataFrame(log_groups)
    df = df.sort_values(by='Stored bytes', ascending=False).drop(columns='Stored bytes')  # Sort and drop raw bytes

    # Create a workbook and add a worksheet
    workbook = Workbook()
    sheet = workbook.active

    # Write the header
    sheet.append(df.columns.tolist())

    # Write the data
    for row in df.itertuples(index=False):
        sheet.append(row)

    # Apply left alignment to all cells
    for row in sheet.iter_rows():
        for cell in row:
            cell.alignment = Alignment(horizontal='left')

    # Save the workbook
    workbook.save(filename)
    print(f'Log groups inventory saved to {filename}')


def main(regions):
    sts_client = boto3.client('sts')
    account_id = sts_client.get_caller_identity()['Account']

    all_log_groups = []

    with ThreadPoolExecutor(max_workers=len(regions)) as executor:
        future_to_region = {executor.submit(fetch_log_groups, region, account_id): region for region in regions}

        for future in as_completed(future_to_region):
            region = future_to_region[future]
            try:
                log_groups = future.result()
                print(f'Fetched {len(log_groups)} log groups from region: {region}')
                all_log_groups.extend(log_groups)
            except Exception as e:
                print(f'Error fetching log groups from region {region}: {str(e)}')

    if all_log_groups:
        unique_filename = generate_unique_filename()
        save_to_excel(all_log_groups, unique_filename)
    else:
        print('No log groups found.')


if __name__ == '__main__':
    # Specify the AWS regions you want to query
    regions_to_query = ['us-east-1', 'us-west-2']

    # Run the main function
    main(regions_to_query)

