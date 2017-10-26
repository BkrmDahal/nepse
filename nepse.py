"""get data from npse"""
import re
from collections import defaultdict
from functools import lru_cache

import pandas as pd

from util_nepse import get_text, get_soup, 
					chunks, get_date_range, write_csv, clean_names


#-------------------------------------------------------------------
def company_listed(url='http://www.nepalstock.com/company?_limit=500', 
                   table='my-table table') -> list:
	"""get all company listed
	   
	   Params:
	   -------
	   url: url of page
	   table: class id of table
	   
	   Return
	   -------
	   list of information in table as list of list"""
	   
    npse = get_soup(url)
    table = npse.find('table', {'class':table})

    #get all row 
    rows = table.find_all('tr')[1:-1] #remove  first and last row
	body_list = []
    for row in rows:
        body = row.find_all('td')
        link = row.find('a').get('href') # add company link
        body_list.append(get_text(body)+[link])
		
    colnames  = clean_names(body_list[0])
    colnames = colnames[:-1] + ['link']
    body_list[0] =  colnames  # first list is colnames
    return body_list

company = company_listed()

# I like converting to DataFrame for analysis and wangling
company = pd.DataFrame(company[1:], columns=company[0])
company['url_id'] = company['link'].str.split('/').str[-1]

#------------------------------------------------------------------------
def company_detail(company_id = '397', 
				   table='my-table table'):
    """Get company additional detail
	   Params:
	   -------
	   company_id: company display id
	   table: class id of table
	   
	   Return
	   -------
	   list of information in table as list of list"""
    url = 'http://www.nepalstock.com/company/display/{}'.format(company_id)
    npse = get_soup(url)
    table = npse.find('table', {'class':table})
    rows = table.find_all('tr')[2:] #remove  unwanted row
	body_list = []
    for i in rows:
        body = i.find_all('td')
        body_list.append(get_text(body))
		
    #remove unwanted row
    del body_list[0][0], body_list[1]
    
    body_list.append(['url_id', company_id])
    return body_list

#get detail of all company
detail = defaultdict(list)
for i in company['url_id']:
    c_detail = company_detail(i)
    for key, values in c_detail:
        detail[key].append(values)
detail = pd.DataFrame(detail)

##join company with detail
company = pd.merge(company, detail, how='left', on=['url_id'])
company.to_csv('company_full.csv')

#--------------------------------------------------------------------------
def stock_today(date, 
				table='table table-condensed table-hover', 
				headers = True):
    """Get data from stock table
	   Params:
	   -------
	   date: 'str' -- 'YYYY-MM-DD'
	   table: class id of table
	   headers: if you want to return header of table
	   
	   Return
	   -------
	   list of information in table as list of list"""
	   
    url = ('http://www.nepalstock.com/todaysprice?'
           +'startDate={}&stock-symbol=&_limit=500'.format(date))
    npse = get_soup(url)
	pages = npse.find_all(text=re.compile('Page.*')) #'Page' is only present if page has data
    if pages:
        table = npse.find('table', {'class':table})

        #get title 
        title = table.find_all('tr')[1].find_all('td') #title of table
        title = get_text(title)
        title = clean_names(title)
        title = ['date'] + title #added date to data

        #tr in table are nested, so we only need top tr
        body = table.find_all('tr')[2].find_all('td')
        body = list(chunks(get_text(body), 10)) #get all data and make chuck of rows
        body = [[date] + i  for i in body] #added date to data
        body_list = [title] + body
        if headers:
            return body_list[:-1] #last coloum is total, so ignored
        else:
            return body_list[1:-1]
    else:
        print("No data on stock exchange, was that day public holiday!!")
        pass

def stockprice_range(start, end):
	"""get stock price of each company each day for given range
	
		Params
		--------
		start: str -- 'YYYY-MM-DD'
		end: str -- 'YYYY-MM-DD'
		
		Return
		-------
		list of information as list of list, first list as header"""
		
    ranges = get_date_range(start, end)
    stock = []
    for date, day in ranges:
        if day not in [5, 4]: #stock market is closed on fri and sat
            if not stock:
                temp = stock_today(date)
                if temp:
                    stock = temp
            else:
                temp = stock_today(date, headers=False)
                if temp:
                    stock += temp
    return stock
	
stock_all = stockprice_range('2017-01-01', '2017-10-25')
stock_all = pd.DataFrame(stock_all[1:], columns=stock_all[0])
stock_all.to_csv('stock_range.csv')

#-----------------------------------------------------------------------------------#





