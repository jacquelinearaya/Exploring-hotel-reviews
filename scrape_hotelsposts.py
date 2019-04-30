#!/apps/anaconda3-4.3.0/bin/python
#################################
#Scrape comments for a given hotel

import json
import time
import io
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select


# def basics():
# 	#get basic hotel information
# 	name = driver.find_element_by_xpath('//*[@id="hp_hotel_name"]')
# 	try:
# 		hotel_type = str((driver.find_element_by_xpath('//*[@id="hp_hotel_name"]/span')).text)

# 	except:
# 		hotel_type = None
# 	# try:
# 	# 	stars = (driver.find_element_by_xpath('//*[@id="wrap-hotelpage-top"]/div[1]/span/span[1]/i/span')).text
# 	# except:
# 	# 	stars = None
# 	try:		
# 		hotel_coord = driver.find_element_by_xpath('//*[@id="hotel_address"]')
# 		hotel_coords = hotel_coord.get_attribute("data-atlas-latlng")
# 	except:
# 		hotel_coords = None
# 	return str(name.text), hotel_type, hotel_coords


def get_review(hotel):
	#find general review and scores
	try:
		hotel['review_score'] = float(driver.find_element_by_xpath('//*[@id="review_list_score"]/span/span').text)
		score = driver.find_element_by_xpath('//*[@id="review_list_score_breakdown"]')
		hotel['cleanliness'] = float(score.get_attribute('data-hotel_clean'))
		hotel['comfort'] = float(score.get_attribute('data-hotel_comfort'))
		hotel['location'] = float(score.get_attribute('data-hotel_location'))
		hotel['services'] = float(score.get_attribute('data-hotel_services'))
		hotel['staff'] = float(score.get_attribute('data-hotel_staff'))
		hotel['value_formoney'] = float(score.get_attribute('data-hotel_value'))
		try:
			hotel['wifi'] = float(score.get_attribute('data-hotel_wifi'))
		except:
			hotel['wifi'] = float(score.get_attribute('data-hotel_paid_wifi'))
	except:
		hotel['review_score'] = None
		hotel['cleanliness'] = None
		hotel['comfort'] = None
		hotel['location'] = None
		hotel['services'] = None
		hotel['staff'] = None
		hotel['value_formoney'] = None
		hotel['wifi'] = None
	return hotel

def get_posts(counter, hotel):
	keep = True
	while keep == True:
		#time.sleep(0.5)
		try:
			reviews_list = lambda: driver.find_elements_by_class_name('review_item')
		except:
			keep = False
			return hotel
		#time.sleep(0.5)
		for item in reviews_list():
			#print(item.tag_name)
			try:
				score1 = item.find_element_by_class_name('review-score-badge')
				score = float(score1.text)
			except:
				score = None
			#don't pick up the text	
			# evethg = item.find_elements_by_xpath('div[3]/div/*')
			# print([str(i.text) for i in evethg])
			# print(len([str(i.text) for i in evethg]))
			#Country in the post
			try:
				post_origin1 = item.find_element_by_xpath('div[2]/span/span[2]/span')
				post_origin = post_origin1.text
			except:
				post_origin = None
			#Date of the post
			try:		
				post_date1 = item.find_element_by_class_name('review_item_date')
				post_date = post_date1.text[10:]
			except:
				post_date = None
			#Number of reviews of the person writing the review
			try:
				number_ofposts1 = item.find_element_by_xpath('div[2]/div[3]')
				#number_ofposts = number_ofposts1.text[:-7]
				number_ofposts = [int(s) for s in (number_ofposts1.text).split() if s.isdigit()]
			except:
				number_ofposts = None	
			#print(post_origin.text)
			#print(post_date.text)
			#print(number_ofposts.text)
			#hotel['posts'][counter] = {'post_score':float(score.text), 'post_content': [str(i.text) for i in evethg]}
			#Fill in dictionary by post
			hotel['posts'][counter] = {'post_score':score, 'post_country': post_origin,\
			 'post_date':post_date, 'number_ofposts': number_ofposts[0]}
			#print('OK_%s'%counter)
			counter+=1
		try:
			#print('trying next page')
			next_reviewpage = driver.find_element_by_id('review_next_page_link')
			next_reviewpage.click()
			time.sleep(0.6)
		except:
			keep = False
			return hotel


def hotel_name(hotel):
	findhtml = hotel.find('.html?')
	hotel_ref = hotel[33:findhtml]
	return hotel_ref


init = int(sys.argv[1])
fin = int(sys.argv[2])
country = sys.argv[3]
#country_letters = sys.argv[4]
driver = webdriver.Chrome()

hotel_dict = {}

long_counter = 1
with open('./%s_links'%country,'r') as infile:
	links = infile.readlines()
	#print(links)
	for line in links[init:fin]:
		print(long_counter)
		long_counter+=1
		line = line.strip()
		# if long_counter == 100:
		# 	time.sleep(120)
		# if long_counter == 200:
		# 	time.sleep(120)
		# if long_counter == 400:
		# 	time.sleep(120)
		# if long_counter == 600:
		# 	time.sleep(120)
		# if long_counter == 800:
		# 	time.sleep(120)
		# if long_counter == 1000:
		# 	time.sleep(120)	
		hotelref= hotel_name(line)
		#review_page = 'https://www.booking.com/reviews/%s/hotel/%s.html'%(sys.argv[4],hotelref)
		review_page = 'https://www.booking.com/reviews/us/hotel/%s.html'%(hotelref)
		#print(review_page)
		#review_page = 'https://www.booking.com/reviews/us/hotel/windsor-hills-ow2.html'
		driver.get(review_page)
		#print(line)
		#html_req = driver.get(line)
		time.sleep(1)
		#bsc = basics()
		try:
			name = str((driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/div/div[1]/h1/a')).text)
		except:
			name = hotelref
		hotel_dict[name]={}
		#hotel_dict[bsc[0]]['hotel_name'] = str((driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/div/div[1]/h1/a')).text)
		try:
			hotel_dict[name]['hotel_address'] = str((driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/div/div[1]/p')).text)
		except:
			hotel_dict[name]['hotel_address'] = None
		#hotel_dict[bsc[0]]['hotel_type'] = bsc[1] 
		#hotel_dict[bsc[0]]['stars'] = bsc[2]
		#hotel_dict[bsc[0]]['coordinates'] = bsc[2]
		# hotelref= hotel_name(line)
		# review_page = 'https://www.booking.com/reviews/us/hotel/%s.html'%hotelref
		# print(review_page)
		# driver.get(review_page)
		#if there are reviews
		try:
			no_reviews = driver.find_element_by_class_name('no_more_content_text')
			hotel_dict[name]['posts'] = None
			continue
		except NoSuchElementException: #when the hotel doesn't have reviews
			try:
				language = Select(driver.find_element_by_xpath('//*[@id="language"]'))
				language.select_by_value("all")
				ok_button = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[2]/div/form/input[3]')
				ok_button.click()
				time.sleep(1)
				counter = 1
				rev_init = get_review(hotel_dict[name])
				#time.sleep(1)
				hotel_dict[name]['posts'] = {}
				#reviews_list = driver.find_elements_by_class_name('review_item')
				post_result = get_posts(counter, hotel_dict[name])
				#print(hotel_dict)
			except NoSuchElementException: #when there reviews page doesn't exist
				hotel_dict[name]['posts'] = None
				continue
		time.sleep(1)


#pagenotfound
#https://www.booking.com/reviews/us/hotel/new-4br-european-design-duplex-5min-to-downtown-chicago.html
#https://www.booking.com/hotel/us/new-4br-european-design-duplex-5min-to-downtown-chicago.html?aid=304142&label=gen173nr-1FCAYo7AE4gANIM1gEaKcCiAEBmAExuAEZyAEP2AEB6AEB-AECiAIBqAID&sid=57cb7d3869b67869d158b97b3afd3b39&ucfs=1&srpvid=b9f51f98def000b6&srepoch=1550723378&hpos=6&hapos=426&dest_id=20033173&dest_type=city&sr_order=popularity&from=searchresults;highlight_room=#hotelTmpl


#print(hotel_dict)

#find reviews list
#reviews_list = driver.find_elements_by_xpath('//*[@id="review_list_page_container"]/ul//li')
# reviews_list = driver.find_elements_by_class_name('review_item') #75 li in first page
# #print(reviews_list.text) 
# #print(driver.find_element_by_xpath('//*[@id="review_list_page_container"]/ul/li[2]/div[3]/div/div[1]/div[1]/span[2]/meta[1]').get_attribute('content'))
# # tags = [i.tag_name for i in reviews_list]
# # print(tags)
# # print(len(tags))
# counter = 1
# for item in reviews_list:
# 	#evethg = item.find_elements_by_xpath('//div[3]/div/*')
# 	score = item.find_element_by_class_name('review-score-badge')
# 	evethg = item.find_elements_by_xpath('div[3]/div/*')
# 	# print(counter)
# 	# print("score %s"%(score.text))
# 	# for i in evethg:
# 	# 	print(i.text)
# 	hotel_dict['posts'][counter] = {'post_score':float(score.text), 'post_content': [i.text for i in evethg]}
# 	counter+=1
# 	#text = item.find_elements_by_xpath('div[3]/div/div[1]/child::node()')
# 	# elements = item.find_elements_by_xpath('//div[3]/div/div[1]//meta[1]')
# 	# for j in elements:
# 	#  	print(j.get_attribute('content'))
# 	# #post_score = item.find_element_by_xpath('//div[3]/div/div[1]//meta[1]')
# 	# #post_score = item.find_element_by_xpath('div[3]/div/div[1]/div[1]/span[2]/meta[1]')
# 	# #print(post_score.get_attribute('content'))
# 	# post_content = item.find_elements_by_xpath('div[3]/div/div[2]//p')


driver.quit()

#write to file
json_obj = json.dumps(hotel_dict, indent=4, sort_keys=True,ensure_ascii=False)
with io.open('./%s/%s_reviews_%s_%s.json'%(country,country,init,fin),'w',encoding='utf-8') as f:
	f.write(json_obj)
