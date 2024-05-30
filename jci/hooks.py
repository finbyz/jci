# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "jci"
app_title = "Jci"
app_publisher = "Finbyz Tech Pvt Ltd"
app_description = "custom App for JCI"
app_icon = "octicon octicon-briefcase"
app_color = "orange"
app_email = "info@finbyz.com"
app_license = "GPL 3.0"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/jci/css/jci.css"
# app_include_js = "/assets/jci/js/jci.js"

# include js, css files in header of web template
# web_include_css = "/assets/jci/css/jci.css"
# web_include_js = "/assets/jci/js/jci.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "jci.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "jci.install.before_install"
# after_install = "jci.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "jci.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# doc_events = {
# 	"Issue": {
# 		"onload": "jci.api.customer_query1"	
# 	},

doc_events = {
	"Issue": {
 		"before_save": "jci.api.issue_before_save"
 	},
	"JCI Lead": {
		"before_save": "jci.api.jci_lead_before_save"
	}
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"jci.tasks.all"
# 	],
# 	"daily": [
# 		"jci.tasks.daily"
# 	],
# 	"hourly": [
# 		"jci.tasks.hourly"
# 	],
# 	"weekly": [
# 		"jci.tasks.weekly"
# 	]
# 	"monthly": [
# 		"jci.tasks.monthly"
# 	]
# }
scheduler_events = {
	"cron":{
		"0/1 * * * *": [
            "jci.api.issue_reports",
			"jci.api.jci_lead_email"
        ]
	}
}

# Testing
# -------

# before_tests = "jci.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "jci.event.get_events"
# }



