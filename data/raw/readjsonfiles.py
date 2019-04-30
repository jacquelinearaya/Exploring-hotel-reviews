import io
import json
import pandas as pd
import os

# with io.open("./Chicago_reviews_0_346.json",'r',encoding='utf-8') as json_file:
# 	data = json.load(json_file)

#list city folders in folder
dirs = [ name for name in os.listdir("./top10us_scrape/") if os.path.isdir(os.path.join("./top10us_scrape/", name)) ]
#list of all json files
files = []
for f in dirs:
	files.extend(os.listdir("top10us_scrape/%s"%f))



# #df: main dataframe of hotels (no posts)
# df = pd.read_json("./Chicago_reviews_0_346.json", orient='index')
# df['name']= df.index
# df['city'] = city
# df['hotelid'] = list(range(1,len(df)+1))
# df.set_index('hotelid', inplace=True)

''''function to create main dataframe with the correspondent hotel id
input: file is the json file to read and idcount is the moving id
output: dataframe of all hotel information
'''

def main_df(file, idcount):
	#df: main dataframe of hotels (no posts)
	f = "./top10us_scrape/%s/%s"%(file[0:file.find("_")], file)
	df = pd.read_json(f, orient='index')
	df['name']= df.index
	df['city'] = file[0:file.find("_")]
	finalid = idcount+len(df)
	df['hotelid'] = list(range(idcount, finalid))
	#df.set_index('hotelid', inplace=True)
	return df


''''function to check if post's dict exist and convert it to dataframe
input: x is a dataframe
output: dataframe of all posts by hotel
'''
def dict_to_df(x):
	filldf = pd.DataFrame(columns= ['hotelid','post_id','post_country','post_score','number_ofposts','post_date','city'])
	for row in x.iterrows():
		if isinstance(row[1][0], dict):
			temp = pd.DataFrame.from_dict(row[1][0], orient='index')
			temp['hotelid'] = row[1][2]
			temp['post_id'] = temp.index
			temp['city'] = row[1][1]
			filldf = filldf.append(temp, ignore_index = True)
			#print(temp)
		# else:
		# 	filldf = filldf.append([row[0],"NA","NA","NA","NA","NA"], ignore_index = True)
	return filldf


# df.loc[df['posts'] == None, 'posts'] = 0
# df.loc[df['posts'] != None, 'posts'] = 1
#if the hotel has posts:1 else:0
#df['posts'] = df['posts'].apply(lambda x: 0 if x==None else 1)

#df.drop('posts', axis=1, inplace=True)
# df.to_csv("./Chicago_reviews_0_346.csv", na_rep="NA")
# df2.to_csv("./Chicago_posts_0_346.csv", na_rep="NA" )

counter_id = 1
maindf = pd.DataFrame()
postdf = pd.DataFrame()

for file in files:
	print(file)
	main_aux = main_df(file, counter_id)
	counter_id += len(main_aux)
	#fill post df
	post_aux = dict_to_df(pd.DataFrame(main_aux[['posts','city','hotelid']]))
	main_aux['posts'] = main_aux['posts'].apply(lambda x: 0 if x==None else 1)
	maindf = maindf.append(main_aux, ignore_index=True)
	postdf = postdf.append(post_aux, ignore_index= True)



maindf.to_csv("./hotels_2.csv", na_rep="NA")
postdf.to_csv("./posts_2.csv", na_rep="NA" )