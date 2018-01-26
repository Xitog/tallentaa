import re

test = "Je suis Monsieur Poulpe."

re_name = re.compile("Monsieur (.+)\\.")

res = re.search(re_name, test)

print(res.group(1)) # 10h51
