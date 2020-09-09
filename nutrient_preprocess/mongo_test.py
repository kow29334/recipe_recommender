import pymongo
import json


# Create connnect
client = pymongo.MongoClient(host='localhost', port=27017)

# assign database
db = client.tibame
 # assign colection
collection = db.recipe_raw


# insert one item
# insert_item = {'test_id' : 2, 'tester' : 'KC'}
# insert_result = db.scraping.insert_one(insert_item)
#
# print(insert_result)

# Query all
# search_response = db.scraping.find()
# for item in search_response:
#     print(item)

# Query specific column
queryArgs = {}
projectField = {'url' : True, 'title' : True, 'time' : True, 'author' : True, 'ingredient' : True, 'stpes' : True, 'comment' : True}
search_response = db.recipe_raw.find(queryArgs, projection=projectField)

print(type(search_response))

result_recipe = []
for n, item in enumerate(search_response):
    result_recipe.append(item)

recipe_1 = result_recipe[0]
print(recipe_1['ingredient'])





# Delete entire collection
# db.recipe_raw.delete_many({})
