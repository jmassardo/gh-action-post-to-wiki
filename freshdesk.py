import requests, json, sys, os

if 'URL_ROOT' in os.environ:
    url_root = os.environ['URL_ROOT']
elif 'url_root' in os.environ:
    url_root = os.environ['url_root']
else:
    sys.exit("Missing URL_ROOT")

if 'API_KEY' in os.environ:
    api_key = os.environ['API_KEY']
elif 'api_key' in os.environ:
    api_key = os.environ['api_key']
else:
    sys.exit("Missing API_KEY")

password = "x"
headers = {'Content-type': 'application/json'}

# Function for making API calls and trapping errors
def rest_api(method, url, query):
    result = requests.request(
        method,
        url,
        headers=headers,
        json=query,
        auth=(api_key, password)
    )

    # TODO: Should this fail the entire run? Or should we send the status code to the user?
    # If we get anything besides a 200, catch the error and bail
    if result.status_code == 200:
      print("API call succeeded")
    elif result.status_code == 201:
      print("Successfully created object")
    else:
      sys.exit("API call failed. Code: " + str(result.status_code) + ", Reason: " + result.reason + ", Details: " + result.text)
    return result

# We need a list of the categories first so let's
# fetch them and return their id's and names
def get_categories():
  category_list = []
  result = rest_api('GET', url_root +"categories", '')
  categories = json.loads(result.text)
  for c in categories:
    print("Found category: "+ c["name"])
    category_list.append({"id": c["id"], "name": c["name"]})
  return category_list

# Now that we have the cagetories, let's use that to get a list of 
# the folders in each category.
def get_folders():
  folder_list = []
  for category in get_categories():
    result = rest_api('GET', url_root +"categories/"+ str(category["id"]) +"/folders", '')
    folders = json.loads(result.text)
    for f in folders:
      print("Found folder: "+ f["name"] +" in category: "+ category["name"])
      folder_list.append({"cat_id": category["id"], "cat_name": category["name"], "folder_id": f["id"], "folder_name": f["name"]})
  return folder_list

# Finally, we need to get use the folder list to get a list of
# all the KB articles.
def get_articles():
  article_list = []
  for folder in get_folders():
    result = rest_api('GET', url_root +"folders/"+ str(folder["folder_id"]) +"/articles", '')
    articles = json.loads(result.text)
    for a in articles:
      print("Found article titled: "+ a["title"] +" in folder: "+ folder["folder_name"] +" in category: "+ folder["cat_name"])
      article_list.append({"cat_id": folder["cat_id"], "cat_name": folder["cat_name"], "folder_id": folder["folder_id"], "folder_name": folder["folder_name"], "article_id": a["id"], "article_title": a["title"], "article_description": a["description"]})
  return article_list

# Make a single article in a specific folder.
def create_article(title, description, folder_id):
  article = {
          'title': title,
          'description' : description,
          'status': 2
      }
  response = rest_api('POST', url_root +"folders/"+ str(folder_id) +"/articles", article)
  result = json.loads(response.text)
  print("Created article named: " + result['title'] + " with id: " + str(result['id']))
  return result["id"]

# Update a specific article
def update_article(title, description, article_id):
  article = {
          'title': title,
          'description' : description,
          'status': 2
      }
  response = rest_api('PUT', url_root +"articles/"+ str(article_id), article)
  result = json.loads(response.text)
  print("Updated article named: " + result['title'])
  return result["id"]
