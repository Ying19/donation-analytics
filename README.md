This program is wrote in python 2.7.


Approach summary:
Two types of datastructures are used in this program. Firstly, using a list to simulate regular table. In this way, we can keep tracking all the streamed in valid records. Secondly, using dictionay datastructure to keep tracking repeat donors and recipient statistics. In this way, the cross-checking time complexity is only O(1) in average case.


Here are the logical steps:
-- Read the required percentile value 
-- Stream in the data from itcont.txt file
-- Validate each record 
-- Check if someone is a repeat donor
-- If someone is indeed a repeat donor, calculating the recipient statistics
-- Write to the ouput file


Simulated table structures are as follows:
-- record_table
index | cmte_id | name | zipcode | year | donation

-- donor_table
{key:value}
key = (name, zipcode)
value = list [corresponding index of each record in record_table]

-- recipient_statistics
{key:value}
key = (cmte_id, zipcode, year)
value = [total_dollars, total_number_contributuion, contribution_list_from_repeat_donors[]]