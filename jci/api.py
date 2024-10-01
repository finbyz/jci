
import frappe
from frappe import _, sendmail
from frappe.core.doctype.communication.email import make
from frappe.utils.background_jobs import enqueue
import datetime
from datetime import timedelta, datetime
from frappe.desk.reportview import get_match_cond, get_filters_cond
from collections import defaultdict
# from frappe.utils import nowdate, add_days, getdate, get_time, add_months

def time_tango(date, time):
	if isinstance(date, datetime):
		date = date.date()
	return datetime.strptime("{}, {}".format(date, time), "%Y-%m-%d, %H:%M:%S")

@frappe.whitelist()
def issue_before_save(self, method): 
	if self.get('opening_date') and self.get('opening_time'):
		opening_datetime = time_tango(self.opening_date, str(self.opening_time).split('.')[0])
		self.due_date = opening_datetime + (timedelta(minutes=30))

	if self.get('resolution_date'):
		resolution_date = str(self.resolution_date).split()
		self.resolution = resolution_date[0]
		self.resolution_time = str(resolution_date[1]).split('.')[0]

		if self.status == "Closed":
			closing_datetime = time_tango(self.resolution, self.resolution_time)
			diff = closing_datetime - opening_datetime
			self.time_difference = diff

@frappe.whitelist()
def issue_reports():
	data = frappe.db.sql("""
			SELECT
				name, subject, project, status, engineer_name, email_sent, due_date, escalation_mail_to
			FROM
				`tabIssue`
			WHERE
				(status = 'Open') and
				email_sent = 0 and
				CASE WHEN due_date IS NOT NULL THEN 
					due_date < NOW()
				END
			""", as_dict=1)

	if data:
		for row in data:
			if not row.escalation_mail_to:
				row.escalation_mail_to = "shubham.dhamija@ibtevolve.com"
			frappe.db.set_value("Issue", row.name, "email_sent", 1)
			# frappe.db.set_value("Issue", row.name, "status", "Overdue")
			if row.engineer_name:
				msg = "The issue " + row.name+ "#"+ row.subject + " that was assigned to " + row.engineer_name +" is overdue"
			else:
				msg = "The issue " + row.name+ "#"+ row.subject +" is overdue"
			sendmail(recipients = [row.escalation_mail_to],
					subject = 'Issue '+ row.name + ' is Overdue', 
					message = msg,
					now= 1)
			frappe.db.commit()


@frappe.whitelist()
def jci_lead_before_save(self, method):
	if self.get('time') and self.get('date'):
		due_datetime = time_tango(self.date, str(self.time).split('.')[0])
		self.due_date = due_datetime + (timedelta(minutes=30))

@frappe.whitelist()
def jci_lead_email():
	data = frappe.db.sql("""
			SELECT
				name, email_sent, due_date, escalation_mail_to
			FROM
				`tabJCI Lead`
			WHERE
				(lead_status = 'Open') and
				email_sent = 0 and
				CASE WHEN due_date IS NOT NULL THEN 
					due_date < NOW()
				END
			""", as_dict=1)
	df_dict = defaultdict(list)
	escalation_mail = {}
	if data:
		for row in data:
			if not row.escalation_mail_to:
				escalation_mail.update({row.name:"shubham.dhamija@ibtevolve.com"})
			frappe.db.set_value("JCI Lead", row.name, "email_sent", 1)
			msg = """
				<p> Dear Team, </p>
				<p> Please note the Lead <b>{}</b> is not updated in the system yet. Please do the needful asap.</p>
				""".format(row.name)
			mail_list = row.escalation_mail_to.split(", ")
			for email in mail_list:
				df_dict[row.name].append(email)
		for key,value in df_dict.items():
			for v in value:
				sendmail(recipients = v,
						subject = 'Lead ' + key + ' - Overdue Alert', 
						message = msg,
						now= 1)
	

# searches for customer
@frappe.whitelist()
def customer_query(doctype, txt, searchfield, start, page_len, filters):
	conditions = []
	cust_master_name = frappe.defaults.get_user_default("cust_master_name")

	if cust_master_name == "Customer Name":
		fields = ["name", "new_unique_ref", "site_address", "territory"]
	else:
		fields = ["name", "customer_name", "new_unique_ref", "site_address", "territory"]

	meta = frappe.get_meta("Customer")
	searchfields = meta.get_search_fields()
	searchfields = searchfields + [f for f in [searchfield or "name", "customer_name"] \
			if not f in searchfields]
	fields = fields + [f for f in searchfields if not f in fields]
	fields = ", ".join(fields)
	searchfields = " or ".join([field + " like %(txt)s" for field in searchfields])

	return frappe.db.sql("""select {fields} from `tabCustomer`
		where docstatus < 2
			and ({scond}) and disabled=0
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, customer_name), locate(%(_txt)s, customer_name), 99999),
			idx desc,
			name, customer_name
		limit %(start)s, %(page_len)s""".format(**{
			"fields": fields,
			"scond": searchfields,
			"mcond": get_match_cond(doctype),
			"fcond": get_filters_cond(doctype, filters, conditions).replace('%', '%%'),
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		})
