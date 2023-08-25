# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 11:45:50 2023

@author: pschw
"""
with open('Alm_matrix.csv', encoding='iso-8859-1') as data:
        lines = data.readlines()

errors = []
dig_an = []
nc_no = []
 
for line in lines[14:32]:
    columns = line.strip().split(',')
    errors.append(columns[4])
    dig_an.append(columns[5])
    nc_no.append(columns[6])

work_matrix = [[dig_an], [nc_no]]
print(work_matrix)