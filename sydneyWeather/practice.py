import xlsxwriter, random



wb = xlsxwriter.Workbook('practice.xlsx')
sheet = wb.add_worksheet()

time = [i + 1 for i in range(10)]
price = [random.randint(10, 100) for _ in range(10)]

sheet.write(0, 0, 'time')
sheet.write(0, 1, 'price')
sheet.write_column(1, 0, time)
sheet.write_column(1, 1, price)

chart = wb.add_chart({'type': 'scatter', 'subtype': 'smooth_with_markers'})
chart.add_series({'name': 'Sheet1!$B$1', 'categories': '=Sheet1!$A2:$A11', 'values': '=Sheet1!$B2:$B11'})
chart.set_title({'name': 'Stock price'})
chart.set_x_axis({'name': 'Time'})
chart.set_y_axis({'name': 'Price ($)'})
chart.set_style(11)

sheet.insert_chart('D4', chart)


wb.close()