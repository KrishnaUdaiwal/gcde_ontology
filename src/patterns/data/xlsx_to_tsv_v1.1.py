# %%
import pandas as pd

data = pd.read_excel('Entities Summary View_v1.xlsx', sheet_name='Entities Summary View', na_values=['NaN'])
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


# %%
def add_prefix(x):
    # takes lists: splits, pads with zeros, and adds GCDE prefix, then joins
    # takes strings: pads with zeros, and adds GCDE prefix
    if isinstance(x, list):
        return ",".join(["GCDE:"+i.astype(str).str.zfill(7) for i in x])
    return "GCDE:"+x.astype(str).str.zfill(7)
add_prefix(pd.Series([1,2,3]))

# %%
def add_prefix(x):
    # takes lists: splits, pads with zeros, and adds GCDE prefix, then joins
    # takes strings: pads with zeros, and adds GCDE prefix
    if isinstance(x, (str, list)):
        #print("recogized as list")  6000
        y = ""
        #print(type(x), str(*x).split(","), "note3")
        for i in str(*x).split(", "):
            y = y+";"+("GCDE:"+i.zfill(7))
#            print(type(i), y, "Note2")
        return "{"+y[1:]+"}"
#        print(",".join(["GCDE:"+i.zfill(7) for i in x]))
#        return "{"+",".join(["GCDE:"+i.zfill(7) for i in x])+ "}"
    return "GCDE:"+str(x).zfill(7)
print(add_prefix(["1, 32, 3"]))
add_prefix(1)

# %%
# Update parent class to include GCDE prefix
# Split with GCDE prefixes

connections = []
for i in data['Connections - Entity From']:
    if isinstance(i, float):
        connections += [i]
    else:
        #print(type(i), i, "note1")
        connections += [add_prefix([i])]
    
print(len(connections))
data['Connections - Entity From'] = connections
#["GCDE:"+x.astype(str).str.zfill(7) for x in data['Connections - Entity From'].str.split(',') if isinstance(x, list)]

# %%
data_view = data[['ID', 'Label', 'Connections - Entity From', 'Entity Short Form', 'Tags', 'Type', 'SubType', 'Description', 'OrgClass', 'OrgSubType', 'Portfolio', 'URL', 'Source of Entry', 'Admin Notes', 'Data Provider', 'Record Status', 'Last Modified By', 'Created', 'French Entity Full Name', 'French Short Form', 'French Description', 'French URL']]
data_view = data_view.rename(columns={"Label": "defined_class_label",
                          "ID":"defined_class",
                          "Connections - Entity From": "parent_class",
                          "Description": "definition",
                          "URL": "definition_source"})
#df.rename(columns={"A": "a", "B": "c"})


# %%
data_view.to_csv('/home/agar2/Documents/1Projects/6Projects/GCDE_ontology/gcde_ontology/src/patterns/data/airtable_full.tsv', sep= "\t", index=False)


# %% [markdown]
# Label ->            defined_class_label
# ID ->               defined_class
# Connections - Entity From -> parent_class
# Entity Short Form	
# Tags	            
# Type	            
# SubType	
# Description	->      definition
# OrgClass	
# OrgSubType	
# Portfolio	
# URL ->              definition_source
# Source of Entry	
# Admin Notes	
# Data Provider	
# Record Status	
# Last Modified By	
# Created	
# French Entity Full Name	
# French Short Form	
# French Description	
# French URL
# 


