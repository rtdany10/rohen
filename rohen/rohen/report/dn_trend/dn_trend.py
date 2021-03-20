# Copyright (c) 2013, Dany RObert and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: return [], []
	columns = [
		_("Item") + ":Link/Item:350", _("Customer") + ":Link/Customer:340",
		_("Quantity") + ":Float:180", _("Amount") + ":Currency:220"
	]
	data = []
	delivery_note = frappe.db.sql("""select name, customer from `tabDelivery Note` where {}""".format(get_conditions(filters)), as_dict=1)
	for dn in delivery_note:
		if filters.get("item_code"):
			cond = "parent = '{}' and item_code = '{}'".format(dn.name, filters.get("item_code"))
		else:
			cond = "parent = '{}'".format(dn.name)
		items = frappe.db.sql("""select item_code, qty, base_net_amount from `tabDelivery Note Item` where {}""".format(cond), as_dict=1)
		for item in items:
			data.append([item.item_code, dn.customer, item.qty, item.base_net_amount])
	return columns, data

def get_conditions(filters):
	conditions = "docstatus = 1"
	if filters.get("from_date"): conditions += " and posting_date >= '{}'".format(filters.get("from_date"))
	if filters.get("to_date"): conditions += " and posting_date <= '{}'".format(filters.get("to_date"))
	if filters.get("company"): conditions += " and company = '{}'".format(filters.get("company"))
	if filters.get("customer"): conditions += " and customer = '{}'".format(filters.get("customer"))

	return conditions
