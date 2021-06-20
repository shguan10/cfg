acceptable_chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
chars2num = {c:ind for ind,c in enumerate(acceptable_chars)}

def sequitur(s):
  nums = [chars2num[c] for c in s if c is in acceptable_chars]
  rules = list(acceptable_chars)
  while True:
    bigrams = []
    addedrule = False
    # read through nums, counting the bigrams
    ind = -1
    while ind < len(nums) and len(nums)>=2:
      ind += 1
      if ind==0: continue
      prevchar = nums[ind-1]
      curchar = nums[ind]

      # if either is negative, it is to be replaced by a rule
      if prevchar<0 or curchar<0: continue 
      
      # see if prevchar,curchar is a known bigram
      bmatch = None
      for ii,b in enumerate(bigrams): 
        if b[0]==prevchar and b[1] == curchar:
          bmatch = ii
      if bmatch is None:
        # we have not seen this bigram yet, so add it to bigrams
        bigrams.append((prevchar,curchar,ind,ind-1))
      else:
        # check if it is in rules
        rmatch = None
        for ii,r in enumerate(rules): 
          if len(r)==2 and r[0]==prevchar and r[1] == curchar:
            rmatch = ii
        if rmatch is None:
          # put it in rules
          addedrule = True
          rmatch = len(rules)
          rules.append((prevchar,curchar))

          # mark the original bigram to be replaced
          nums[bigrams[bmatch][2]] = -rmatch
          nums[bigrams[bmatch][3]] = -rmatch
        
        # mark the current bigram to be replaced
        nums[ind] = -rmatch
        nums[ind-1] = -rmatch
        
        # we are replacing this bigram with a rule so skip the next bigram
        ind+=1
    
    # replace the string with the new chars
    if addedrule:
      newnums = []
      ind = -1
      while ind < len(nums):
        ind+=1
        if nums[ind]<0:
          rule = -nums[ind]
          newnums.append(rule)
          ind+=1 # skip the next char because it is part of the same bigram
      # replace nums with newnums
      nums = newnums
    else: 
      break
      
  return rules


if __name__ == '__main__':
  print(sequitur("qwqqwq"))