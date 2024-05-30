# Copyright (c) 2013, Finbyz Tech Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import getdate, nowdate, add_days

def execute(filters=None):
	columns, data = [], []
	filters.opening_date = getdate(filters.opening_date or add_days(nowdate(), -1))
	columns = get_columns()
	data = get_data(filters)
	frappe.errprint(data)
	return columns, data

def get_columns():
	columns = [
		_("Ticket #") + ":Link/Issue:120",
		_("Status") + ":Select/Status:80",
		_("Opening Date") + ":Date:120",
		_("Opening Time") + ":Time:120",
		_("Customer") + ":Link/Customer:150",
		_("New Unique Reference") + ":Data:150",
		_("Issue Type") + ":Link/Customer Group:120",
		_("Engineer Assigned") + ":Link/Engineer:150",
		_("Resolution") + ":Data:100",
		_("Closing Date and Time") + ":Data:120",
		_("Time Difference") + ":Data:80",
		_("Description") + ":Data:150",
	]
	return columns

def get_data(filters):
	where_clause = filters.issue_id and " and name = '%s' " % filters.issue_id or ""
	where_clause += filters.status and " and status = '%s' " % filters.status or ""
	where_clause += filters.opening_date and " and opening_date = '%s' " % filters.opening_date or ""
	data = frappe.db.sql("""
		SELECT 
			name as "Ticket #", status as "Status", IF(opening_date, opening_date, " ") as "Opening Date", 
			IF(opening_time, opening_time, ' ') as "Opening Time",
			IF(customer='', ' ', customer) as "Customer", 
			IF(unique_ref_num='', ' ', unique_ref_num) as "New Unique Reference", 
			IF(customer_type='', ' ', customer_type) as "Issue Type",
			IF(engineer='', ' ', engineer) as "Engineer Assigned", 
			IF(description='', ' ', description) as "Description", 
			IF(resolution_details='', ' ', resolution_details) as "Resolution",
			IF(resolution_date, resolution_date, ' ') as "Closing Date and Time", 
			IF(time_difference, time_difference, ' ') as "Time Difference"
		FROM
			`tabIssue`
		WHERE name IS NOT NULL
		{where_clause}
		""".format(where_clause=where_clause), as_dict=1)
	return data

