// Copyright (c) 2016, Finbyz Tech Pvt Ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Issue Report"] = {
	"filters": [
		{
			fieldname: "issue_id",
			label: __("Issue"),
			fieldtype: "Data"
		},
		{
			fieldname: "opening_date",
			label:__("Opening Date"),
			fieldtype: "Date",
			default : frappe.datetime.add_days(frappe.datetime.nowdate(), -1)
		},
		{
			fieldname: "status",
			label:__("Status"),
			fieldtype: "Select",
			options: ["", "Open", "Work In Progress", "Hold", "Overdue", "Closed"]
		}
	]
}
