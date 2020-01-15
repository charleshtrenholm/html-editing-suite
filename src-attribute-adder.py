from bs4 import BeautifulSoup
import re

# find all tags with 'data-' prepended to attributes (only imgs and sources)
def no_src_attr(tag):
  if tag.name == 'img':
    return tag.has_attr('data-src') and not tag.has_attr('src')
  elif tag.name == 'source':
    return tag.has_attr('data-srcset') and not tag.has_attr('srcset')
  else:
    return False

# make it 2 space indents instead of the default 1 space (gross)
def pretty_2_space(gross_nightmare_markup):
  r = re.compile(r'^(\s*)', re.MULTILINE)
  return r.sub(r'\1\1', gross_nightmare_markup.prettify())

filepath = 'output.html'

# open copied over file from output.html
with open(filepath) as file:
  html = file.read()
  soup = BeautifulSoup(html, 'html.parser')

bad_tags = soup(no_src_attr)

# copy over data-whatever tags to new regular whatever tags
for tag in bad_tags:
  attr_to_copy = 'src' if tag.name == 'img' else 'srcset'
  value_to_copy = tag['data-' + attr_to_copy]
  tag[attr_to_copy] = value_to_copy

# output new html back to output file
with open(filepath, 'w', encoding='utf-8') as file:
  file.write(str(pretty_2_space(soup)))

print("%s tags were modified" % (len(bad_tags)))