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

      # Look for the category and folder name in the markdown
      lines = text.split('\n')
      for l in lines:
        if '[_metadata_:category]' in l:
          category = l.split('- ')[1].replace('"', '')
        if '[_metadata_:folder]' in l:
          folder = l.split('- ')[1].replace('"', '')

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
        result = fd.create_article(title, html, folder_id)
      else:
        print("Found: "+ title +", Attempting to update")
        result = fd.update_article(title, html, val["article_id"])
