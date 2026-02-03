import re

# Read the file
file_path = r'C:\Users\sanja\OneDrive\Desktop\ignite_admin\dashboard\templates\dashboard\dashboard.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Line 925-926 - Team Size filter
content = re.sub(
    r'<option value="{{ size }}" {% if filters\.team_size==size\|stringformat:"s"\s+%}selected{% endif %}>',
    '<option value="{{ size }}" {% if filters.team_size == size|stringformat:"s" %}selected{% endif %}>',
    content
)

# Fix 2: Line 937-938 - Theme filter
content = re.sub(
    r'<option value="{{ theme }}" {% if filters\.idea_theme==theme %}selected{% endif\s+%}>',
    '<option value="{{ theme }}" {% if filters.idea_theme == theme %}selected{% endif %}>',
    content
)

# Fix 3: Lines 948-955 - Selection status filter (multiple options)
content = re.sub(
    r'<option value="pending" {% if filters\.selection_status==\'pending\' %}selected{%\s+endif %}>Pending</option>',
    '<option value="pending" {% if filters.selection_status == \'pending\' %}selected{% endif %}>Pending</option>',
    content
)
content = re.sub(
    r'<option value="selected" {% if filters\.selection_status==\'selected\' %}selected{%\s+endif %}>Selected</option>',
    '<option value="selected" {% if filters.selection_status == \'selected\' %}selected{% endif %}>Selected</option>',
    content
)
content = re.sub(
    r'<option value="rejected" {% if filters\.selection_status==\'rejected\' %}selected{%\s+endif %}>Rejected</option>',
    '<option value="rejected" {% if filters.selection_status == \'rejected\' %}selected{% endif %}>Rejected</option>',
    content
)
content = re.sub(
    r'<option value="waitlisted" {% if filters\.selection_status==\'waitlisted\'\s+%}selected{% endif %}>Waitlisted</option>',
    '<option value="waitlisted" {% if filters.selection_status == \'waitlisted\' %}selected{% endif %}>Waitlisted</option>',
    content
)

# Fix 4: Lines 1106-1113 - Registration table status (multiple options)
content = re.sub(
    r'<option value="pending" {% if reg\.selection_status==\'pending\' %}selected{% endif %}>\s+Pending</option>',
    '<option value="pending" {% if reg.selection_status == \'pending\' %}selected{% endif %}>Pending</option>',
    content
)
content = re.sub(
    r'<option value="selected" {% if reg\.selection_status==\'selected\' %}selected{% endif\s+%}>Selected</option>',
    '<option value="selected" {% if reg.selection_status == \'selected\' %}selected{% endif %}>Selected</option>',
    content
)
content = re.sub(
    r'<option value="rejected" {% if reg\.selection_status==\'rejected\' %}selected{% endif\s+%}>Rejected</option>',
    '<option value="rejected" {% if reg.selection_status == \'rejected\' %}selected{% endif %}>Rejected</option>',
    content
)
content = re.sub(
    r'<option value="waitlisted" {% if reg\.selection_status==\'waitlisted\' %}selected{%\s+endif %}>Waitlisted</option>',
    '<option value="waitlisted" {% if reg.selection_status == \'waitlisted\' %}selected{% endif %}>Waitlisted</option>',
    content
)

# Write the file back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File fixed successfully!")
