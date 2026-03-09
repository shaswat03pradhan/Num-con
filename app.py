from flask import Flask,render_template,request,url_for
import questions
app=Flask(__name__)

hist=[]

def b2d(A:str):
    y,ans,temp,l1=2,0,0,[]
    for j in range(len(A)):
        l1.append(y**j)
    for k in range(len(A)-1,-1,-1):
        ans=ans+(int(A[k])*l1[temp])
        temp+=1
    return ans 
def o2d(A:str):
    y,ans,temp,l1=8,0,0,[]
    for j in range(len(A)):
        l1.append(y**j)
    for k in range(len(A)-1,-1,-1):
        ans=ans+(int(A[k])*l1[temp])
        temp+=1
    return ans 
def h2d(A:str):
    y,temp,ans,l1=16,0,0,[]
    d={"A":10,"B":11,"C":12,"D":13,"E":14,"F":15}
    for j in range(len(A))  :
        l1.append(y**j)
    for k in range(len(A)-1,-1,-1):
        if A[k].isalpha():
            ans=ans+(d[A[k]]*l1[temp])
        else:
            ans=ans+(int(A[k])*l1[temp])
        temp+=1
    return ans

def d2d(A:str):
    return int(A)

def d2b(ans):
    z,l=2,[]
    while ans>=1:
        b=ans%z
        l.append(b)
        ans=ans//z
    for i in range(len(l)-1,-1,-1):
        ans=ans*10+l[i]
    return(ans)
def d2o(ans):
    z,l=8,[]
    while ans>=1:
        b=ans%z
        l.append(b)
        ans=ans//z
    for i in range(len(l)-1,-1,-1):
        ans=ans*10+l[i]
    return(ans)
def d2h(ans):
    z,l,o=16,[],''
    while ans>=1:
        b=ans%z
        l.append(b)
        ans=ans//z
    d2={10:"A",11:"B",12:"C",13:"D",14:"E",15:"F"}
    for i in range(len(l)-1,-1,-1):
        if l[i]>=10:
            o+=str(d2[l[i]])
        else:
            o+=str(l[i])
    return(o)

@app.route("/", methods=['POST','GET'])
def index():
    css_=url_for('static', filename='style.css')
    if request.method=="GET":
        icon=url_for('static', filename='icon.png')
        return render_template("index.html",css=css_,ic=icon)
    A=request.form.get("input")
    fr=request.form.get("from")
    to=request.form.get("to")
    ANS=0
    
    if "from" not in request.form or "to" not in request.form:
        ANS="INVALID SELECTION!"
    if A=="":
        ANS="INVALID INPUT!"
        
    if fr=='2':
        if A.isnumeric():
            for i in '23456789':
                if i in A:
                    ANS="INVALID INPUT!"
                    break
        else:
            ANS="INVALID INPUT!"
    elif fr=='8':
        if A.isnumeric() and '8' not in A and '9' not in A:
            pass
        else:
            ANS="INVALID INPUT!"
    elif fr=='10':
        if A.isnumeric():
            pass
        else:
            ANS="INVALID INPUT!"
    elif fr=="16":
        if A.isalnum():
            for i in 'GHIJKLMNOPQRSTUVWXYZ':
                if i in A.upper():
                    ANS="INVALID INPUT!"
                    break
        else:
            ANS="INVALID INPUT!"
    if ANS!="INVALID INPUT!" and ANS!="INVALID SELECTION!":
        if fr=="2":
            temp,fr=b2d(A),"Binary"
        elif fr=="8":
            temp,fr=o2d(A),"Octal"
        elif fr=="10":
            temp,fr=d2d(A),"Decimal"
        elif fr=="16":
            temp,fr=h2d(A.upper()),"Hexa decimal"
        if to=="2" and type(ANS)==int:
            ANS,to=d2b(temp),"Binary"
        elif to=="8"and type(ANS)==int:
            ANS,to=d2o(temp),"Octal"
        elif to=="10"and type(ANS)==int:
            ANS,to=d2d(temp),"Decimal"
        elif to=="16"and type(ANS)==int:
            ANS,to=d2h(temp),"Hexa decimal"
        hist.append({"input_no":A.upper(),"from":fr,"to":to,"result":ANS})
        A=A+"→"
    else:
        A=""
    css_=url_for('static', filename='style.css')
    icon=url_for('static', filename='icon.png')
    return render_template("index.html", ans=ANS,css=css_,ic=icon,q=A)

@app.route("/history", methods=['POST','GET'])
def history():
    if request.method=="POST":
        hist.clear()
    icon=url_for('static', filename='icon.png')
    return render_template("history.html", Table=hist[::-1],ic=icon)

@app.route("/quiz", methods=['POST','GET'])
def quiz():
    Questions=questions.ques()
    if request.method=="POST":
        sco=0
        l=[]
        qs=(request.form.get("QUESTIONS"))
        for i in request.form:
            if i[0]=="A":
                no=int(i[1:])-1
                if request.form.get(i) == qs[no]:
                    sco+=1
        if sco==10:
            msg="WOW! Perfect 10🎉🎉"
        elif sco>=7:
            msg="Good job!👏"
        elif sco>=4:
            msg="Nice,Try doing better next time...😊"
        else:
            msg="Nice try,but needs improvement..😢"
        icon=url_for('static', filename='icon.png')
        return render_template("result.html",score=sco,temper=qs,message=msg,ic=icon)
    ans=""
    for j in Questions:
        ans+=j["cor_ans"]
    icon=url_for('static', filename='icon.png')
    return render_template("quiz.html",ques=Questions,anss=ans,ic=icon)

if __name__=="__main__":
    app.run(debug=True)