
import os
import re

file_path = r'c:/Users/sanja/OneDrive/Desktop/ignite_admin/dashboard/templates/dashboard/dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define replacements
replacements = [
    (
        r'{% if filters.team_size==size\|stringformat:"s"\s+%\}selected{% endif %}', 
        '{% if filters.team_size == size|stringformat:"s" %}selected{% endif %}'
    ),
    (
        r'{% if filters.idea_theme==theme %\}selected{% endif\s+%\}', 
        '{% if filters.idea_theme == theme %}selected{% endif %}'
    ),
    (
        r'{% if filters.selection_status==\'pending\' %\}selected{%\s+endif %\}',
        '{% if filters.selection_status == \'pending\' %}selected{% endif %}'
    ),
    (
        r'{% if filters.selection_status==\'selected\' %\}selected{%\s+endif %\}',
        '{% if filters.selection_status == \'selected\' %}selected{% endif %}'
    ),
    (
        r'{% if filters.selection_status==\'rejected\' %\}selected{%\s+endif %\}',
        '{% if filters.selection_status == \'rejected\' %}selected{% endif %}'
    ),
    (
        r'{% if filters.selection_status==\'waitlisted\'\s+%\}selected{% endif %\}',
        '{% if filters.selection_status == \'waitlisted\' %}selected{% endif %}'
    )
]

new_content = content

# 1. Fix Team Size
# The pattern in the file (from view_file) is:
# {% if filters.team_size==size|stringformat:"s"
#                                             %}selected{% endif %}
# Regex to match this spanning multiple lines
new_content = re.sub(
    r'{%\s*if filters\.team_size==size\|stringformat:"s"\s+%\}selected{%\s*endif\s*%\}',
    '{% if filters.team_size == size|stringformat:"s" %}selected{% endif %}',
    new_content,
    flags=re.DOTALL
)

# 2. Fix Theme
# {% if filters.idea_theme==theme %}selected{% endif
#                                             %}
new_content = re.sub(
    r'{%\s*if filters\.idea_theme==theme\s*%\}selected{%\s*endif\s*%\}',
    '{% if filters.idea_theme == theme %}selected{% endif %}',
    new_content,
    flags=re.DOTALL
)

# 3. Fix Payment Status (all options)
# pattern: {% if filters.selection_status=='pending' %}selected{%
#                                             endif %}
new_content = re.sub(
    r'{%\s*if filters\.selection_status==\'([a-z]+)\'\s*%\}selected{%\s*endif\s*%\}',
    r"{% if filters.selection_status == '\1' %}selected{% endif %}",
    new_content,
    flags=re.DOTALL
)

# 4. Fix Table Selection Status (reg.selection_status)
# pattern: {% if reg.selection_status=='pending' %}selected{% endif %}
# or split across lines
new_content = re.sub(
    r'{%\s*if reg\.selection_status==\'([a-z]+)\'\s*%\}selected{%\s*endif\s*%\}',
    r"{% if reg.selection_status == '\1' %}selected{% endif %}",
    new_content,
    flags=re.DOTALL
)

# Also fix specific split cases if the above generic one doesn't catch them
new_content = re.sub(
    r'{%\s*if reg\.selection_status==\'([a-z]+)\'\s*%\}selected{%\s*endif',
    r"{% if reg.selection_status == '\1' %}selected{% endif",
    new_content,
    flags=re.DOTALL
)

if content != new_content:
    print("Found and fixed broken tags.")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
else:
    print("No matching patterns found. Dumping a snippet to debug...")
    # Find where 'stringformat' is to see what it looks like
    idx = content.find('stringformat:"s"')
    if idx != -1:
        print(f"Context around 'stringformat':\n{content[idx-20:idx+100]}")
    else:
        print("Could not even find 'stringformat:\"s\"' string in file.")
