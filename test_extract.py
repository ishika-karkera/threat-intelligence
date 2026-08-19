from extract import extract_ttp_ids

# Test 1: text that explicitly mentions a technique ID
text1 = "The attackers used PowerShell (T1059.001) to execute the payload."
print("Test 1:", extract_ttp_ids(text1))
# Expect to see: ['T1059.001']

# Test 2: text with a keyword but no explicit ID
text2 = "The malware relied on a scheduled task to maintain persistence."
print("Test 2:", extract_ttp_ids(text2))
# Expect to see: ['T1053.005']  (from your KEYWORD_MAP)

# Test 3: text with nothing relevant
text3 = "The company released its quarterly earnings report today."
print("Test 3:", extract_ttp_ids(text3))
# Expect to see: []  (empty list)

# Test 4: text with multiple techniques
text4 = "Credential dumping (T1003) was followed by spearphishing attachment delivery."
print("Test 4:", extract_ttp_ids(text4))
# Expect to see something like: ['T1003', 'T1566.001']
