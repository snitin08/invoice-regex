def convert_key_value_pairs(text):
    import re
    print(text)
    # format dd/mm/yyyy
    date_regex = re.compile('[0-9]*/\d{2}/\d{4}')
    # format of 1 item1 50.00
    item_regex = re.compile('([\d+]*) (\w+[\s\w+]) (\d*[\.]\d*)')
    # format: <text>:(optional) 123456
    invoice_regex = re.compile('(\S+[\s#: ]*)(\d+)')


    invoice_field = re.search(invoice_regex,text)
    date_field = re.search(date_regex,text)
    items_field = re.findall(item_regex,text)
    
    if invoice_field is not None:
        print(invoice_field)
        print("Invoice number",invoice_field.groups())
    if date_field is not None:
        print("Date",date_field.group())
    if item_regex is not None:
        print("Items",items_field)
    



