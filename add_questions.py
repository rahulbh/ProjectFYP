# FOR QnA Table 
# questionno: Primary Key
# questiongroup: The group that question belongs to
# questiontype: ENUM: Question Type can be MCQ, MCMR,
# SA, FIB
# remarks: Comments about the question for inference
# maxmarks: Maximum marks for the question
# coursecode: Foreign Key

# FOR MCQMR Table
# questionno: Primary and Foreign Key
# ques: 2D Array explained below
# description: Stem of the Question
# ans: 2D Array explained below
# partialmarks: Partial marks for each correct value in
# Multiple response type questions. Value is 0 if
# Question Type MCQ

# FOR ques field of MCQMR
# hasparam: 1 if question has Parameters, otherwise 0
# variationno: Variation Number of question
# paramno: Parameter Number of the specific Variation
# paramtype: Can be text or image
# paramvalue: Value of parameter. Name of image in case
# parameter is image

# For ans field of MCQMR
# variationno Variation Number of question
# choiceno Choice Number
# choicevalue Value of Choice
# isanswer Value is 1 if the respective choice is correct,
# otherwise its 0

addques=[{"questionno":901,"questiongroup":"General Science","description":"This question does not relate to the image! Suppose that you plucked %%P%% apples,and Steve took away three. How many apples do you have?"\
            ,"ques":[['1','0','0','text','five'],['1','1','0','text','six']],"ans":[['0','0','10','0'],['0','1','11','0'],['0','2','2','1'],['0','3','13','0'],['0','4','14','0'],['1','0','21','0'],\
                                                                      ['1','1','22','0'],['1','2','23','0'],['1','3','24','0'],['1','4','All of the Above','0'],['1','5','None of the Above','1']],"remarks":"Hello 801"},\
                {"questionno":902,"questiongroup":"General Science","description":"What's the value of Resistance of LDR? %%P%% "\
            ,"ques":[['1','0','0','image','LDR-circuit-improved.png']],"ans":[['0','0','10 ohm','0'],['0','1','15 ohm','1'],['0','2','15 ohm','0'],['0','3','20 ohm','0']],"remarks":"Hello 802"}];

