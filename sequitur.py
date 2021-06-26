acceptable_chars = "abc"
chars2num = {c:ind for ind,c in enumerate(acceptable_chars)}
startofnonterminals = len(acceptable_chars)

import pdb

def sequitur(s):
  nums = [chars2num[c] for c in s if c in acceptable_chars]
  rules = list(acceptable_chars)
  while True:
    bigrams = []
    addedrule = False
    # read through nums, counting the bigrams
    ind = -1
    while ind+1 < len(nums) and len(nums)>2:
      ind += 1
      if ind==0: continue
      prevchar = nums[ind-1]
      curchar = nums[ind]

      # if either is negative, it is to be replaced by a rule
      if prevchar<0 or curchar<0: continue 
      
      # see if prevchar,curchar is a known bigram
      bmatch = None
      for ii,b in enumerate(bigrams): 
        if b[0]==prevchar and \
            b[1] == curchar and \
            b[3] != ind-1:
          bmatch = ii
      if bmatch is None:
        # we have not seen this bigram yet, so add it to bigrams
        bigrams.append((prevchar,curchar,ind-1,ind))
      else:
        # check if it is in rules
        rmatch = None
        for ii,r in enumerate(rules): 
          if len(r)==2 and r[0]==prevchar and r[1] == curchar:
            rmatch = ii
        if rmatch is None:
          # check if the original bigram is marked to be replaced by another rule
          # if so, then we don't add a new rule because this bigram is the first time we've seen it
          if nums[bigrams[bmatch][2]] < 0 or nums[bigrams[bmatch][3]] < 0:
            bigrams[bmatch] = (prevchar,curchar,ind-1,ind)
            continue

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
        
    # replace the string with the new chars
    if addedrule:
      newnums = []
      ind = -1
      while ind+1 < len(nums):
        ind+=1
        if nums[ind]<0:
          # replace the next bigram with a rule
          rule = -nums[ind]
          newnums.append(rule)
          ind+=1 # skip the next char because it is part of the same bigram
        else:
          # curchar is not in a rule, so just append it to newnums
          newnums.append(nums[ind])
      # replace nums with newnums
      nums = newnums

    else: 
      break

  rules.append(nums)
  rules = prunerules(rules)
  return rules,rules[-1]

def prunerules(rules):
  # count the number of times a rule appears
  rcounts = [0 for _ in range(len(rules))]
  rlocs = [None for _ in range(len(rules))]
  rname = startofnonterminals
  while rname < len(rules):
    # read the rule
    for place,ch in enumerate(rules[rname]):
      rcounts[ch] += 1
      # keep track of in which rule it is used
      rlocs[ch] = (rname)
    rname+=1

  # now prune the rules that only appeared once
  rname = startofnonterminals
  while rname < len(rules):
    # how many times did it appear?
    if rcounts[rname]==1:
      # prune it!
      user = rlocs[rname]
      prevrule = list(rules[user])
      ii = 0
      while ii<len(prevrule) and prevrule[ii]!=rname: ii+=1
      newrule = list(prevrule[:ii]) +\
                  list(rules[rname]) +\
                  (prevrule[ii+1:]) if ii<len(prevrule) else []
      rules[user] = newrule
    rname+=1
  return rules

def decodeCFG(rules,nums,numsind=0):
  # decodes the nums according to rules
  buffer = []
  if numsind>=len(nums):
    return buffer

  rule2decode = nums[numsind]
  if rule2decode < len(acceptable_chars):
    buffer.extend(rules[rule2decode])
  else:
    # it's a non-terminal
    buffer.extend(decodeCFG(rules,rules[rule2decode]))

  buffer.extend(decodeCFG(rules,nums,numsind+1))
  return buffer

def teststr(s):
  rules,nums = sequitur(s)
  # print(list(enumerate(rules)),"\t",nums)
  d = ''.join(decodeCFG(rules,nums))
  # print(d)
  if s!=d: 
    print(s)
    assert False

if __name__ == '__main__':
  import numpy as np
  lens = np.random.rand(1000) * 1000
  for ln in lens:
    ln = int(ln)
    chars = [int(np.random.rand()*len(acceptable_chars)) for _ in range(ln)]
    chars = [acceptable_chars[ch] for ch in chars]
    teststr("".join(chars))

  