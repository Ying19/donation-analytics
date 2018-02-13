#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


import sys
import datetime
import math

percentile_file_path = './input/percentile.txt'
itcont_file_path = './input/itcont.txt'
output_file_path = './output/repeat_donors.txt'

# check whether a record is valid or not
def validate_record(recipient, name, zipcode, transaction_dt, transaction_amt, other_id):
    if recipient == '' or len(recipient) != 9:
        return False
    if name == '' or len(name) > 200:
        return False
    if zipcode == '' or len(zipcode) < 5 or len(zipcode) > 9:
        return False
    if transaction_dt == '':
        return False
    elif validate_date(transaction_dt):
        pass
    else:
        return False

    if transaction_amt == '':
        return False
    elif validate_amt(transaction_amt):
        pass
    else:
        return False

    if  other_id == '':
        return True

    return False

# check if the transaction date is valid
def validate_date(transaction_dt):
    if len(transaction_dt) != 8:
        return False
    try:
        datetime.datetime.strptime(transaction_dt,'%m%d%Y')
        return True
    except:
        return False

# check if the transaction amount is valid
def validate_amt(transaction_amt):
    transaction_amt = float(transaction_amt)
    if int(transaction_amt) != int(abs(transaction_amt)):
        return False
    length = amount_precision_scale(transaction_amt)
    if length[0]>14 or length[1]>2:
        return False
    return True

# determine the precision and scale
def amount_precision_scale(number):
    max_digit = 14
    int_part = int(number)
    fraction_part = number - int_part
    if int_part == 0:
        integer_digits = 1
    else:
        integer_digits = int(math.log10(int_part)) + 1
    if integer_digits > 14:
        return (integer_digits, 0)
    left_digits = 10**(max_digit - integer_digits)
    fraction_digits = int(left_digits * fraction_part + 0.5) + left_digits
    while fraction_digits % 10 == 0:
        fraction_digits = fraction_digits / 10
    scale = int(math.log10(fraction_digits))
    return (integer_digits + scale, scale)

# check if someone is a repeat donor
def is_repeat_donor(index, record):
    key = (record[1], record[2])
    if key not in donor_table:
        donor_table[key] = list()
        donor_table[key].append(index)
        return False
    else:
        value = donor_table[key]
        value.append(index)
        donor_table[key] = value
        current_index = index
        previous_index = current_index - 1
        while previous_index >= 0:
            if int(record_table[current_index][3]) > int(record_table[previous_index][3]):
                return True
            previous_index -= 1
        return False

# keep tracking the recipient
def add_recipient(record):
    key = (record[0], record[2], record[3])
    if key not in recipient_table:
        total_dollars = float(record[4])
        total_number_contribution = 1
        contribution_list = list()
        contribution_list.append(record[4])
        new_value = [total_dollars, total_number_contribution, contribution_list]
        recipient_table[key] = new_value
    else:
        total_dollars = float(recipient_table[key][0]) + float(record[4])
        total_number_contribution = int(recipient_table[key][1]) + 1
        contribution_list = recipient_table[key][2]
        contribution_list.append(record[4])
        new_value = [total_dollars, total_number_contribution, contribution_list]
        recipient_table[key] = new_value

# calculate the running percentile
def running_percentile(output_index):
    selection_list = recipient_table[output_index][2]
    N = int(recipient_table[output_index][1])
    rank = math.ceil(percentile / 100 * N)
    rank = int(rank)
    result = sorted(selection_list)[rank-1]
    result = float(result)
    frac = result - int(result)
    if frac < 0.5:
        result = math.floor(result)
        result = int(result)
    else:
        result = math.ceil(result)
        result = int(result)
    return result


if __name__ == '__main__':

    # read percentile value
    fhand = open(percentile_file_path)
    try:
        percentile = float(fhand.read())
        fhand.close()
    except:
        fhand.close()
        sys.exit(1)

    # clear the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write('')

    # read itcont.txt
    fhand = open(itcont_file_path)
    record_table = list()
    donor_table = dict()
    recipient_table = dict()
    for line in fhand:
        string = line.strip().split('|')

        # Validate the record
        if validate_record(string[0], string[7], string[10], string[13], string[14], string[15]):
            cmte_id = string[0]
            name = string[7]
            zipcode = string[10][0:5]
            year = string[13][4:8]
            donation = string[14]
            record = (cmte_id, name, zipcode, year, donation)
            record_table.append(record)
            index = len(record_table) - 1
            if is_repeat_donor(index, record):
                add_recipient(record)
                output_recipient = str(record_table[index][0])
                output_zipcode = str(record_table[index][2])
                output_year = str(record_table[index][3])
                output_index = (output_recipient, output_zipcode, output_year)
                output_percentile = str(running_percentile(output_index))
                output_amount = float(recipient_table[output_index][0])
                if output_amount - int(output_amount) == 0:
                    output_amount = int(output_amount)
                output_amount = str(output_amount)
                output_number_transaction = str(recipient_table[output_index][1])
                with open(output_file_path, 'a') as output_file:
                    output_file.write(output_recipient + '|' + output_zipcode + '|' + output_year + '|' + output_percentile + '|' + output_amount + '|' + output_number_transaction + '\n')

    fhand.close()
