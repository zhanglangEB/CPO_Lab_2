# Regular expression
   **group name**: oh my nunu     
   **list of group members**: Xin, Wang、Qianwen, Yu   
   **laboratory work number**: 2  
   **variant description**: Regular expression  
# Synopsis
   **Use python to develop a library to implement Regular expression, which must meet the following conditions:** 

   1. Sub variants define which construction you should support:
      \w, \s, \d, \, ^, ., $, *, +, [], [^], {n}, {min,}, {,max}, {min,max}.
   2. Support functions: match, search, sub, split.
   3. Visualization as a finite state machine (state diagram and table). 
   4. You should use default Python logging module to make interpreter work transparent.
   5. Should provide complex examples such as a time parsing, JSON parsing and so on. 

   **To implement this lab,which must to do:**  

   1. Design Input Language,make a discrete-event model of computation.   
   2. On the basis of discrete_event,build the packaged NFA.
   3. Parsed regular expressions.
   4. The parsed regular expression is used to build the NFA.
   5. Using NFA, the regular expression of the function match, search, sub and split
   6.  After finishing programming, you need to verify your library by unit tests and property-based tests. 

   **The following functions should be implemented:**  

   1. match(Try to match a pattern from the beginning of the string.If the match is not successful at the beginning, match() returns none).
   2. search(Scan the entire string and return the first successful match).
   3. sub(Replace matches in string).   
   4. split(The method divides the string according to the substring that can be matched and returns the list).  

# Contribution summary for each group member
   **Qianyu, Wen(github: yqw123)**: Complete the common and discrete_event and regex_fa_construction and the tests of discrete_event and regex_fa_construction.Finish part of the report.   
   **Xin, Wang(github: zhanglangEB)**: Complete the regex_parser and regex_to_nfa and regex_lib and the tests of them.Finish part of the report. 


# Work demonstration 
   1. match  

      ```
      regex = '[0-9]+'
      text = '1324354657'
      self.assertEqual(match(regex, text), (0, len(text)))
      ```

   2. search  

      ```
      regex = '[0-9]+'
      text = 'hello1324354657itmo'
      self.assertEqual(search(regex, text), (5, 15))
      ```

   3. sub  

      ```
      regex = r' #.*$'
      text = '2004-959-559 # this is a phone number'
      self.assertEqual(sub(regex, "", text, 1), '2004-959-559') 
      ```

   4. split 

      ```
      regex = r'\w+'
      text = 'wxx，wxx，wxx，wxx，wxx'
      self.assertEqual(split(regex, text), ['', '，', '，', '，', '，', ''])
      self.assertEqual(split(regex, text, 1), ['', '，wxx，wxx，wxx，wxx'])
      ```

# Conclusion
  First, the regular expression is parsed to find out the meaning and category of each regular expression metacharacter.
  
  Then, according to the results of the analysis, the stack is used to implement the regular expression operation. In the process of operation, the Thompson construction method is used to construct the NFA corresponding to the regular expression.
  
  Finally, using the NFA corresponding to the regular expression to carry out string matching, to achieve match, search, sub, split function.
  
  Regex_FA_Construction is an NFA constructor class repackaged on the basis of discrete_event model, which contains the operation of NFA nodes and matching results.
  
  The regex_parser parses regular expressions, dividing them into operators and operands.
  
  Regex_to_NFA uses the results of Regex_Parser parsed and the Regex_Fa_Construction NFA constructor class implementation to convert the regular expression to the corresponding NFA.
  
  Regex_lib implements match, search, sub, and split functions using the corresponding NFA of regular expressions.
