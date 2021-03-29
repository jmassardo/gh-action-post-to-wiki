import markdown, glob, os
import freshdesk as fd

# Let's get the existing articles in Freshdesk
articles = fd.get_articles()

# Let's find any files that have an external audience tag
for kb in glob.glob("./wiki/*.md"):
  print("Checking file: "+ kb)
  with open(kb, 'r') as reader:
    # read the whole file in
    text = reader.read()
    if '[_metadata_:audience]:- "external"' in text:
      # Convert markdown to HTML
      html = markdown.markdown(text)

      # Setting a default empty string for the tags
      # If there aren't any tags, we need to give it an empty string to prevent errors
      tags = []

      # Split out the other metadata
      lines = text.split('\n')
      for l in lines:
        if '[_metadata_:category]' in l:
          category = l.split('- ')[1].replace('"', '')
        if '[_metadata_:folder]' in l:
          folder = l.split('- ')[1].replace('"', '')
        
        # We need the tags in a list instead of a string.
        if '[_metadata_:tags]' in l:

          # Split the single string off from the header, remove the quotes, finally split it into a list
          tags = l.split('- ')[1].replace('"', '').split(', ')

      # Strip the extension so we can use the filename as the article title
      title = kb.replace('.md', '')
      title = title.replace('./wiki/', '')
      val = next((item for item in articles if item["article_title"] == title), None)
      if val == None:
        # This isn't optimal but it gets the folder id we need.
        filtered_cats = [c for c in articles if c["cat_name"] == category]
        folders = [f for f in filtered_cats if f["folder_name"] == folder]
        folder_id = folders[0]["folder_id"]

        print("Didn't find: "+ title +", Attempting to create")
        result = fd.create_article(title, html, folder_id, tags)
      else:
        print("Found: "+ title +", Attempting to update")
        result = fd.update_article(title, html, val["article_id"], tags)
