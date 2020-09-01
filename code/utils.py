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
    
    print("Invoice number",invoice_field.groups())
    print("Date",date_field.group())
    print("Items",items_field)
    


convert_key_value_pairs("Order #: 69923 5/26/2016  Lunch 45.90 1 Coke 3.00 SUB TOTAL: 51.90"
                )
