import frappe

def execute():
    """
    Update item barcode table with minimum six letters and add it 
    in barcodes table as well
    """
    item_list = frappe.get_list('Item')
    for row in item_list:
        item_doc = frappe.get_doc('Item', row.name)
        if item_doc.barcode:
            try:
                barcode_len = len(item_doc.barcode)
                if barcode_len < 6:
                    new_barcode = ''
                    for i in range(6 - barcode_len):
                        new_barcode += '0'
                    
                    item_doc.barcode = new_barcode + item_doc.barcode
                has_barcode = False
                for row in item_doc.barcodes:
                    if row.barcode == item_doc.barcode:
                        has_barcode = True
                
                if not has_barcode:
                    item_doc.append('barcodes', {
                        'barcode': item_doc.barcode
                    })
                
                item_doc.save()
                frappe.db.commit()
                print(f'{item_doc.item_code} updated')
            except:
                print(f'Error while processing {item_doc.item_code}')