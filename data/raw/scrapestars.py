#!/apps/anaconda3-4.3.0/bin/python
#################################
#Script to scrape hotel links from booking.com

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select



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

def hotel_links(country,counter,write_to):
#to scrape name and hotel stars	
	# hotel_list = '//*[@id="hotellist_inner"]//div[2]/div[1]/div[1]/h3/a/span[1]'
	# hotel_list_elems = driver.find_elements_by_xpath(hotel_list)
	#stars = 'html/body/div[3]/div/div[3]/div[1]/div[1]/div[5]/div[3]/div[1]/div//div'
	stars = '//*[@id="hotellist_inner"]'
	starsfind = driver.find_elements_by_xpath(stars)
	# for item in hotel_list_elems:
	# 	#print(item.tag_name)
	# 	link = item.text
	# 	print(link)
	count = [2*n for n in range(1,17)]
	del count[4]
	for i in starsfind:
		for j in count:
			try:
				k = i.find_element_by_xpath('div[%s]'%j)
				hotel_stars = k.get_attribute('data-class')
				l = k.find_element_by_xpath('div/a/img')
				hotel_name = l.get_attribute("alt")
				#l = i.find_element_by_xpath('div[%s]/div[2]/div[1]/div[1]/h3/a/span[1]'%j)
				#l = i.find_elements_by_xpath('div[%s]/div[2]/div[1]/div[1]/h3/a//span'%j)
				# for el in l:
				# 	print(el.tag_name)
				# 	name = el.find_element_by_class_name("sr-hotel__name\n")
				# 	hotel_name = name.text
				#hotel_name = l.text
				write_to.write('%s\t\"%s\"\t%d'%(country,hotel_name,int(hotel_stars)))
				write_to.write('\n')
			except:
				print(driver.current_url)
				print(country)
				pass


#usa_file = open('usa_hotels_en','w')

with open('top10_ita','r') as f:
	for line in f:
		line = line.split(",")
		driver = webdriver.Firefox()
		country = line[0].replace(" ", "")
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
		#Extra code for 5 stars	
		#try:
		time.sleep(1)
		try:
			checkstar = driver.find_element_by_xpath('//*[@id="filter_class"]/div[2]/a[6]')
			checkstar.click()
		except:
			pass
		counter = 1
		#with open('%s_stars'%country,'w') as w_file:
		with open('%s_stars_6'%country,'w') as w_file:
			while counter<no_pages+1:
				time.sleep(2)
				hotel_links(country,counter,w_file)
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

