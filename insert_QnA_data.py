from flask.globals import request
def insert_MCQ_QnA(varVal,answer):
        ans=list(list())
        for var in range(varVal):
            choiceVal = request.form.getlist('value'+str(var))
            right = request.form.getlist('value'+str(var))
            for choiceNo in range(len(choiceVal)): 
                answer.append(var)
                print answer
                answer.append(choiceNo)
                answer.append(choiceVal[choiceNo])
                if right[choiceNo]==1:
                    answer.append('correct')
                    print answer
                else:
                    answer.append('wrong')
                    print answer
                ans.append(answer)
                answer=[]
        return ans
            
        
    