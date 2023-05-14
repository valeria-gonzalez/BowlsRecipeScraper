# Usage

Can find at: https://test.pypi.org/project/bowlsRecipeScraper/

```
#before-hand use: pip install -i https://test.pypi.org/simple/ bowlsRecipeScraper
from bowlsRecipeScraper import bowlsRecipeScraper as brs

# connect to website using selenium and web driver
brs.connect(url)

# get all recipe links from one page
brs.get_links_from_one_page(my_webpage)

# get all recipe links from all pages on the website
brs.get_links_from_site(recipe_driver, num_pages)

# get all links from site based on a category
brs.get_links_site_by_category(category) #(needs a try catch because sometime is faulty, and need to re-try, my bad, will work on it)

# scrap recipe summary from a specific recipe link
brs.get_summary(link)

# to get all data from a recipe based on specific recipe link
brs.get_recipe(link)

# to get all recipes and their information from a category
brs.get_recipe_data_by_interval(category, links, start, end)
```
