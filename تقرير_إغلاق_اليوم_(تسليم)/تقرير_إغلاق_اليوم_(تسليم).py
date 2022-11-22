# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	
	
	
	# data = prepare_data(filters)
	
	# data = export_data
	return columns, data

def get_data(filters):
	
	userBranch = frappe.db.get_value("Employee", {'user_id':frappe.session.user}, ["branch"])
	data = []

	cash_list_head = [{'mode_of_payment': 'مبيعات نقدية','indent':0, 'has_value': True}]
	data.append(cash_list_head[0])

	# for parent in cash_list_head:
	# 	parent["has_value"] = True
	# 	data.append(parent)

	cash_data = frappe.db.get_list('Payment Entry',
	fields=['mode_of_payment','name','paid_from_account_balance','base_paid_amount','received_amount', ('received_amount-base_paid_amount as diff'), 'posting_date', '1 as indent'],		filters={
			'status':"Submitted",
			'mode_of_payment':["like",f"%نقدية%"],
			'posting_date':["between", (filters.get("from_date"),filters.get("to_date"))]})
	
	for data_f in cash_data:
		data_f["has_value"] = False
		data.append(data_f)

	frappe.msgprint(str(cash_list_head[0]))

	credit_list_head = [{'mode_of_payment': 'مبيعات بطاقة','indent':0, 'has_value': True}]
	data.append(credit_list_head[0])

	credit_data = frappe.db.get_list('Payment Entry',
		fields=['mode_of_payment','name','paid_from_account_balance','base_paid_amount','received_amount', ('received_amount-base_paid_amount as diff'), 'posting_date', '1 as indent'],
		filters={
			'status':"Submitted",
			'mode_of_payment':["like",],
			'mode_of_payment':["like",f"%بطاقة%"],
			'posting_date':["between", (filters.get("from_date"),filters.get("to_date"))]})
	
	for data_f in credit_data:
		data_f["has_value"] = False
		data.append(data_f)




	bank_list_head = [{'mode_of_payment': 'مبيعات صكوك','indent':0, 'has_value': True}]
	data.append(bank_list_head[0])

	bank_data = frappe.db.get_list('Payment Entry',
		fields=['mode_of_payment','name','paid_from_account_balance','base_paid_amount','received_amount', ('received_amount-base_paid_amount as diff'), 'posting_date', '1 as indent'],
		filters={
			'status':"Submitted",
			'mode_of_payment':["like","%صك%"],
			'posting_date':["between", (filters.get("from_date"),filters.get("to_date"))]})
	
	for data_f in bank_data:
		data_f["has_value"] = False
		data.append(data_f)

	# frappe.msgprint(bek)
	return data


def get_columns():

	return [
		# Mode of payment
		{
			"fieldname": "mode_of_payment",
			"label": _("طريقة الدفع"),
			"fieldtype": "Data",
			# "options": "Mode of Payment",
			"width": 100
		}
		,
		{
			"fieldname": "posting_date",
			"label": _("التاريخ"),
			"fieldtype": "Data",
			"width": 100
		}
		,
		# name
		{
			"fieldname": "name",
			"label": _("الرقم الإشاري"),
			"fieldtype": "Data",
			"width": 150
		}
		,
		{
			"fieldname": "paid_from_account_balance",
			"label": _("رصيد الحساب"),
			"fieldtype": "Data",
			"width": 100
		}
		,
		{
			"fieldname": "base_paid_amount",
			"label": _("الحساب"),
			"fieldtype": "Data",
			"width": 100
		}
		,
		{
			"fieldname": "received_amount",
			"label": _("المسلم"),
			"fieldtype": "Data",
			"width": 100
		}
		,
		{
			"fieldname": "diff",
			"label": _("الفروقات"),
			"fieldtype": "Data",
			"width": 100
		}
		
		
	]