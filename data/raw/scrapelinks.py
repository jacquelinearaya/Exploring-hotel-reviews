#!/apps/anaconda3-4.3.0/bin/python
#################################
#Script to scrape hotel links from booking.com

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException



def next_page(counter):
	#find next page
	try:
		time.sleep(1)
		nxt_page = driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/div[1]/ul/li[3]/a')
		nxt_page.click()
	except:
		print('next page failed at %s'%counter)
		print(driver.current_url) #if it fails, print the current url
		pass

def hotel_links(counter,write_to):
	try:
		#get link of every hotel
		hotel_list = '//*[@id="hotellist_inner"]//div[2]/div[1]/div[1]/h3/a'
		#//*[@id="hotellist_inner"]/div[2]/div[2]/div[1]/div[1]/h3/a
		#//*[@id="hotellist_inner"]/div[3]/div[2]/div[1]/div[1]/h3/a
		hotel_list_elems = driver.find_elements_by_xpath(hotel_list)
		for item in hotel_list_elems:
			write_to.write(item.get_attribute("href"))
			write_to.write('\n')
	except:
		print('hotel links not found %s'%counter)
		print(driver.current_url) #if it fails, print the current url
		pass


#usa_file = open('usa_hotels_en','w')

with open('top10_ita','r') as f:
	for line in f:
		line = line.split(",")
		driver = webdriver.Firefox()
		country = line[0]
		init_html = line[1]
		no_pages = int(line[2].strip())
		#USA page
		#init_html = 'https://www.booking.com/country/us.es.html?label=gen173nr-1FCAEoggI46AdIM1gEaKcCiAEBmAExuAEZyAEP2AEB6AEB-AECiAIBqAID;sid=d675f1392f1ef4bb31149cc2e12aab35'
		#init_html = 'https://www.booking.com/searchresults.html?label=gen173nr-1FCAEoggI46AdIM1gEaKcCiAEBmAExuAEZyAEP2AEB6AEB-AECiAIBqAID;sid=1902f11eaecfc890d0115563686fadc9;atlas_src=lp_map;dest_id=224;dest_type=country&;map=1#map_closed'
		#print(line)
		html_req = driver.get(init_html)
		time.sleep(2)
		#close pop-up
		try:
			pop_up = driver.find_element_by_xpath('//*[@id="close_map_lightbox"]/i')
			pop_up.click()
		except NoSuchElementException:
			pass

		counter = 1
		with open('%s_links'%country,'w') as w_file:
			while counter<no_pages+1:
				time.sleep(2)
				hotel_links(counter,w_file)
				time.sleep(3)
				if counter == 25:
					time.sleep(30)
				if counter == 50:
					time.sleep(30)
				counter+=1
				next_page(counter)
		time.sleep(2)
		driver.quit()

		#usa_file.close()
# show_map = '//*[@id="bodyconstraint-inner"]/div[3]/div[1]/a'
# show_map_f = '/html/body/div[4]/div/div[4]/div[1]/a/href' #firefox dooesn't find it
# show_map_elem = driver.find_element_by_xpath(show_map).click()
#<a href="/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIM1gEaKcCiAEBmAExuAEZyAEP2AEB6AEB-AECiAIBqAID;sid=e8aeb620275029c1d4aee961f1b5e5a8;atlas_src=lp_map;dest_id=224;dest_type=country&amp;;map=1" class=" static_map static_map_banner show_map lp_single_horizontal_map_divider " data-source="map_thumbnail" data-center="37.2099990844726,-97.2113533020019" data-zoom="2" data-offset-x="" data-offset-y="" data-height="110" data-width="1110">

