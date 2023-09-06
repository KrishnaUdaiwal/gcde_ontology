# %%
import pandas as pd

data = pd.read_excel('/home/agar2/Documents/1Projects/6Projects/GCDE_ontology/gcde_ontology/src/patterns/data/Entities Summary View_v1.xlsx', sheet_name='Entities Summary View', na_values=['NaN'])
data['ID'] = "GCDE:"+data['ID'].astype(str).str.zfill(7)            # Add GCDE prefix and pad with zeros

# %%
desc = data['Description'].str.replace('[a-zA-Z0-9 .,]', '')[data['Description'].str.replace('[a-zA-Z0-9 .,]', '').notna()]
spec_chars = ""
for i in desc:
    if i == "":
        continue
#    print(i)
    for j in i:
        if j not in spec_chars:
            spec_chars += j

print(spec_chars)

#TODO Use above to create a list of special characters to remove, except for the ones we want to keep
# only allow alphanumeric characters, special characters: .,() and space
# '+-:()/\'–$&!;‑"|°?€=£·#~±%@[]'

# https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python/1280823#1280823
delchars = ''.join(spec_chars for c in map(chr, range(256)) if not c.isalnum() and c not in ' .,+-:()/\'–$&!;‑"|°?€=£·#~±%@[]')
del_map = str.maketrans('', '', delchars)

def remove_special_characters(text):
    return text.translate(del_map)

# Test
a = pd.Series(['a™', 'édf\nd', ' c   '])
print("Test:", a, a.str.replace('\n', ' ').apply(lambda x: remove_special_characters(x.strip()) if isinstance(x, str) else x), sep='\n')

# %%
# Remove new lines, leading and trailing whitespaces, and special characters
def fix_text(text):
    return text.str.replace('\n', ' ').apply(lambda x: remove_special_characters(x.strip()) if isinstance(x, str) else x) 

data['Description'] = fix_text(data['Description'])
data['French Description'] = fix_text(data['French Description'])
data['Admin Notes'] = fix_text(data['Admin Notes'])

# Update parent class to include GCDE prefix

data_view = data[['ID', 'Connections - Entity From', 'Label', 'Entity Short Form', 'Tags', 'Type', 'SubType', 'Description', 'OrgClass', 'OrgSubType', 'Portfolio', 'URL', 'Source of Entry', 'Admin Notes', 'Data Provider', 'Record Status', 'Last Modified By', 'Created', 'French Entity Full Name', 'French Short Form', 'French Description', 'French URL']]
data_view.rename(columns={"Label": "defined_class_label",
                          "ID":"defined_class",
                          "Connections - Entity From": "parent_class",
                          "Description": "definition",
                          "URL": "definition_source"})
data_view.to_csv('/home/agar2/Documents/1Projects/6Projects/GCDE_ontology/gcde_ontology/src/patterns/data/Entities Summary View_v1.tsv', sep= "\t", index=False)

# %%



