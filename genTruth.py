def proc(exp,dict):
    while "(" in exp:
        i1=exp.index("(")
        i=1
        i2=i1
        while i>0:
            i2+=1
            if exp[i2]=="(":
                i+=1
            if exp[i2]==")":
                i-=1
        tmp=exp[i1:i2+1]
        exp=exp.replace(tmp,str(proc(tmp[1:-1],dict)),1)
    next=""
    for a in exp:
        if a in dict:
            next+=str(dict[a])
        else:
            next+=a
    nex=""
    bool=False
    for a in range(len(next)-1,-1,-1):
        if next[a]=="'":
            bool=True
        else:
            if next[a] in "01" and bool:
                nex="01"["10".find(next[a])]+nex
            else:
                nex=next[a]+nex
            bool=False
    l=["00","01","10"]
    change=True
    while change:
        change=False
        for pat in l:
            if nex.count(pat)>0:
                change=True
                nex=nex.replace(pat,"0")
    l=["11"]
    change=True
    while change:
        change=False
        for pat in l:
            if nex.count(pat)>0:
                change=True
                nex=nex.replace(pat,"1")
    l=["0+0"]
    change=True
    while change:
        change=False
        for pat in l:
            if nex.count(pat)>0:
                change=True
                nex=nex.replace(pat,"0")
    l=["1+1","0+1","1+0"]
    change=True
    while change:
        change=False
        for pat in l:
            if nex.count(pat)>0:
                change=True
                nex=nex.replace(pat,"1")
    return int(nex)

def binary(digits):
    l=[]
    o=[]
    import copy
    for a in range(digits):
        l.append(0)
    for a in range(2**digits):
        o.append(copy.copy(l))
        l[-1]+=1
        for a in range(digits-1,-1,-1):
            if l[a]==2:
                l[a]=0
                l[a-1]+=1
    return o

def invertExpression(exp):
    #this operation is so fucking strange i had to make a seperate fucking function just for it
    #this step inverts every single term
    s=""
    for a in exp:
        if not a in "'+()" and not a in s:
            s+=a
    nex=""
    for i in range(len(exp)):
        if exp[i]!="'":
            nex+=exp[i]
        if exp[i] in s:
            if i==len(exp)-1 or exp[i+1]!="'":
                nex+="'"
    exp=""
    for i in range(len(nex)-1):
        exp+=nex[i]
        if nex[i]!="+" and nex[i+1] in s:
            exp+="?"
    exp+=nex[-1]
    exp="("+exp+")"
    exp=exp.replace("+",")(")
    exp=exp.replace("?","+")
    return exp

def notVar(var):
    #returns inverse of a single variable
    if len(var)==2:
        return var[:1]
    return var+"'"

def betterFind(string,substring):
    out=[]
    for a in range(len(string)-len(substring)+1):
        if string[a:a+len(substring)]==substring:
            out.append(a)
    return out

class invalidExpression(Exception):
    pass

class termDat:
    def __init__(self,item):
        self.terms=[]
        for ind in range(len(item)-(item[-1]=="'")):
            if item[ind]!="'":
                self.terms.append(item[ind])
                if ind!=len(item)-1 and item[ind+1]=="'":
                    self.terms[-1]+="'"
    def toString(self):
        out=""
        for item in self.terms:
            out+=item
        return out
    def removeTerms(self,terms):
        for term in terms:
            self.terms.remove(term)
        if self.terms==[]:
            self.terms=["1"]
    def addTerms(self,termItem):
        for term in termItem.terms:
            if not term in self.terms:
                self.terms.append(term)
    def is1(self):
        return self.terms==["1"]
    def is0(self):
        return self.terms==["0"]
    def checkRepeats(self):
        for i1 in range(len(self.terms)):
            for i2 in range(len(self.terms)):
                if i1!=i2 and self.terms[i1]==self.terms[i2]:
                    oldstr=self.toString()
                    v=self.terms.pop(i1)
                    return (v,oldstr,oldstr.replace(v,"",1))
        return None
    def checkInverts(self):
        for term in self.terms:
            if len(term)==1 and term+"'" in self.terms:
                oldstr=self.toString
                self.terms=["0"]
                return (term+","+term+"'",oldstr,"0")
        return None
    def remove(self,term):
        if term in self.terms:
            self.terms.remove(term)
            return True
        return False
    def equals(self,termObj):
        if len(termObj.terms)==len(self.terms):
            for a in self.terms:
                if not a in termObj.terms:
                    return False
            return True
        return False

class expression:
    def __init__(self,inString):
        if "(" in inString or ")" in inString:
            raise(invalidExpression(inString))
        self.terms=[]
        for item in inString.split("+"):
            self.terms.append(termDat(item))
    def toString(self):
        out=self.terms[0].toString()
        for n in self.terms[1:]:
            out+="+"+n.toString()
        return out
    def checkDivOuts(self):
        import copy
        lst=copy.copy(self.terms[0].terms)
        for a in self.terms[1:]:
            for b in copy.copy(lst):
                if not b in a.terms:
                    lst.remove(b)
        return lst
    def divide(self,items):
        for v in self.terms:
            v.removeTerms(items)
    def multiply(self,terms):
        #terms is list of term items
        import copy
        lst=copy.copy(self.terms)
        self.terms=[]
        for v1 in lst:
            for v2 in terms:
                temp=copy.deepcopy(v1)
                temp.addTerms(v2)
                self.terms.append(temp)
    def recurs(self):
        import copy
        for term in copy.copy(self.terms):
            val=len(self.checkDivOuts())
            self.terms.remove(term)
            nv=len(self.checkDivOuts())
            if len(self.terms)>2:
                yield from self.recurs()
            import copy
            yield (nv,copy.copy(self.terms))
            self.terms.append(term)
    def fitDivOuts(self):
        before=len(self.checkDivOuts())
        divs=0
        num=999
        exp1=[]
        import copy
        for solve in self.recurs():
            temp=min([len(v.toString()) for v in solve[1]])
            if solve[0]>divs:
                exp1=copy.copy(solve[1])
                num=temp
                divs=solve[0]
            elif solve[0]==divs and temp<num:
                exp1=copy.copy(solve[1])
                num=temp
                divs=solve[0]
        if divs<=before:
            return False
        exp2=copy.copy(self.terms)
        for a in copy.copy(exp2):
            if a in exp1:
                exp2.remove(a)
        texp1=expression("a")
        texp1.terms=copy.copy(exp1)
        texp2=expression("a")
        texp2.terms=copy.copy(exp2)
        return (texp1,texp2)
    def applyIdentityLaws(self,full=True):
        lst=[]
        for a in self.terms:
            lst.append(a.toString())
        if full:
            if True in [v.is1() for v in self.terms]:
                oldstr=self.toString()
                self.terms=[termDat("1")]
                return ["identity rule 1",oldstr,oldstr,"1"]
            for i in range(len(self.terms)):
                if self.terms[i].is0():
                    oldstr=self.toString()
                    temp=self.terms.pop(i)
                    return ["identity rule 2",temp,oldstr,self.toString()]
            for a in range(len(lst)):
                for b in range(len(lst)):
                    if a!=b and lst[a]==lst[b]:
                        oldstr=self.toString()
                        self.terms.pop(a)
                        return ["indeponent rule 1",lst[a],oldstr,self.toString()]
            for a in lst:
                temp=invertExpression(a)[1:-1]
                if temp in lst:
                    oldstr=self.toString()
                    self.terms=[termDat("1")]
                    return ["complement rule 1",a+","+temp,oldstr,self.toString()]
        for a in lst:
            if "1" in a:
                rep=a
                wit=rep.replace("1","")
                oldstr=self.toString()
                return ["identity rule 3",rep,oldstr,self.toString().replace(rep,wit)]
        for a in lst:
            if "0" in a:
                oldstr=self.toString()
                return ["identity rule 4",a,oldstr,oldstr.replace(a,"0")]
        for item in self.terms:
            oldstr=self.toString()
            v=item.checkInverts()
            if v!=None:
                return ["complement rule 2",v[0],oldstr,self.toString()]
        for item in self.terms:
            oldstr=self.toString()
            v=item.checkRepeats()
            if v!=None:
                return ["indeponent rule 2",v[0],oldstr,self.toString()]
        return None
    def applyComplexLaws(self):
        oldstr=self.toString()
        for a in self.terms:
            if len(a.terms)==1:
                bool=False
                newTerm=a.terms[0]
                if len(newTerm)==1:
                    newTerm+="'"
                else:
                    newTerm=newTerm[:1]
                for b in self.terms:
                    n=b.remove(newTerm)
                    if n:
                        bool=True
                if bool:
                    return [1,newTerm,oldstr,self.toString()]
        return None
    def __contains__(self,term):
        temp=termDat(term)
        for a in self.terms:
            if a.equals(temp):
                return True
        return False
    def replace(self,indexingTerm,writeTerm):
        temp=termDat(indexingTerm)
        write=termDat(writeTerm)
        for a in range(len(self.terms)):
            if self.terms[a].equals(temp):
                self.terms[a]=write
    def weirdCheck(self):
        for term in self.terms:
            for item in term.terms:
                newval=notVar(item)
                for term2 in self.terms:
                    if not term.equals(term2):
                        for item2 in term2.terms:
                            if item2==newval:
                                #HEY WE CAN APPLY THIS STUPID FUCKING RULE
                                oldstr=self.toString()
                                idk=(term.toString()+term2.toString())
                                if len(newval)>len(item):
                                    idk=idk.replace(newval,"").replace(item,"")
                                else:
                                    idk=idk.replace(item,"").replace(newval,"")
                                if idk in self:
                                    self.replace(idk,"0")
                                    return ["consensus theorem ",idk,oldstr,self.toString()]
        return None
#[actiontype,metadata,oldstring,newstring]

def checkActions(string,final=False):
    for i in range(len(string)):
        if string[i]==")":
            if i!=len(string)-1 and not string[i+1] in "()+'":
                #end distribute needs to be moved or itll cause problems
                i1=i+1
                i2=i1
                while i2!=len(string)-1 and not string[i2] in "(+":
                    i2+=1
                i2+=(i2==len(string)-1)
                depth=1
                while depth!=0:
                    i-=1
                    if string[i]==")":
                        depth+=1
                    if string[i]=="(":
                        depth-=1
                newstring=string.replace(string[i:i2],string[i1:i2]+string[i:i1])
                return ["move multiple to left side",string[i1:i2],string,newstring]
    if "(" in string or ")" in string:
        fd=betterFind(string,"(")
        sd=[]
        for startIndex in fd:
            depth=1
            while depth!=0:
                startIndex+=1
                if string[startIndex]=="(":
                    depth+=1
                elif string[startIndex]==")":
                    depth-=1
            sd.append(startIndex)
        for start, stop in zip(fd,sd):
            act=checkActions(string[start+1:stop])
            if act!=None:
                #=====================UPDATE THIS LATER=====================
                before=string[start+1:stop]
                string=string.replace(before,act[3],1)
                act[3]=string
                return act
    #logically this part be called at most 1 recursion level from max depth so we dont have to worry about nested parenthesis
    #check for distributable nots
    if ")'" in string:
        ind2=string.find(")'")
        ind1=ind2-1
        while string[ind1]!="(":
            ind1-=1
        substring=string[ind1+1:ind2]
        newstring=string.replace("("+substring+")'",invertExpression(substring))
        return ["distribute not","("+substring+")'",string,newstring]
    #check for multiplies
    #type 1 multiplies
    if ")(" in string:
        temp=string.find(")(")
        temp=sd.index(temp)
        exp1=string[fd[temp]+1:sd[temp]]
        exp2=string[fd[temp+1]+1:sd[temp+1]]
        bool=False
        if sd[temp+1]!=len(string)-1 and string[sd[temp+1]+1]=="(":
            bool=True
        if fd[temp]!=0 and string[fd[temp]-1]!="+":
            bool=True
        nex=expression(exp1)
        nex.multiply(expression(exp2).terms)
        nex=nex.toString()
        if bool:
            newstring=string.replace("("+exp1+")("+exp2+")","("+nex+")",1)
        else:
            newstring=string.replace("("+exp1+")("+exp2+")",nex,1)
        return ["multiply expressions together","("+exp1+")("+exp2+")",string,newstring]
    #type 2,3 multiplies
    if "(" in string:
        ind1=string.find("(")
        ind2=string.find(")")
        #find distributable
        test=ind1
        while test!=0 and string[test]!='+':
            test-=1
        dist=None
        if (string[test]=="+" and test!=ind1-1) or test==0:
            test-=(test==0)
            dist=string[test+1:ind1]
        if dist!=None:
            exp1=string[ind1+1:ind2]
            nex=expression(exp1)
            #check dist rule
            if dist!="":
                if dist in nex:
                    newstring=string.replace(dist+"("+exp1+")",dist,1)
                    return ["distributive absorbtion law",dist+"("+exp1+")",string,newstring]
                #if len(dist)-(dist[-1]=="'")==1:
                #    ndist=invertExpression(dist)[1:-1]
                #    if ndist in nex:
                #        newstring=string.replace(dist+"("+exp1+")",dist,1)
                #        return ["distributive absorbtion law 2",dist+"("+exp1+")",string,newstring]
                #must distribute
                nex.multiply([termDat(dist)])
                nex=nex.toString()
                newstring=string.replace(dist+"("+exp1+")",nex,1)
                return ["distribute",dist+"("+exp1+")",string,newstring]
            else:
                exp1=string[ind1+1:ind2]
                newstring=string.replace("("+exp1+")",exp1,1)
                return ["remove parenthesis","("+exp1+")",string,newstring]
        else:
            exp1=string[ind1+1:ind2]
            newstring=string.replace("("+exp1+")",exp1,1)
            return ["remove parenthesis","("+exp1+")",string,newstring]
    #at this point there should be no parenthesis in the expression
    #check boolean rules here
    exp=expression(string)
    if "1'" in exp:
        oldstr=exp.toString()
        exp.replace("1'","0")
        return ["invert ","1'",oldstr,exp.toString()]
    if "0'" in exp:
        oldstr=exp.toString()
        exp.replace("0'","1")
        return ["invert ","0'",oldstr,exp.toString()]
    if len(exp.terms)>1:
        simple=exp.applyIdentityLaws()
        if simple!=None:
            return [simple[0],simple[1],string,string.replace(simple[2],simple[3],1)]
        complex=exp.applyComplexLaws()
        if complex!=None:
            return ["absorbtion law",complex[1],string,string.replace(complex[2],complex[3],1)]
        if len(exp.terms)>2:
            test=exp.weirdCheck()
            if test!=None:
                return [test[0],test[1],string,string.replace(test[2],test[3],1)]
    elif len(exp.terms)==1 and len(exp.terms[0].terms)>1:
        simple=exp.applyIdentityLaws(full=False)
        if simple!=None:
            return [simple[0],simple[1],string,string.replace(simple[2],simple[3],1)]
    #check for better arrangements for div outs
    exp=expression(string)
    if len(exp.terms)>2:
        solve=exp.fitDivOuts()
        if solve!=False:
            newstring="("+solve[0].toString()+")+"+solve[1].toString()
            return ["reorder",string,string,newstring]
    #check for div outs
    exp=expression(string)
    lst=exp.checkDivOuts()
    if len(exp.terms)>1 and len(lst)>0:
        #divide out item in lst from expression'
        exp.divide(lst)
        newstring=exp.toString()
        if checkActions(newstring)==None and not final:
            return None
        meta=""
        for a in lst:
            meta+=a
        return ["divide",meta,string,meta+"("+newstring+")"]
    return None



while True:
    exp=""
    while exp=="":
        exp=input("expression:")
    s=""
    for a in exp:
        if not a in "'10+()" and not a in s:
            s+=a
    temp=sorted(s)
    s=""
    for a in temp:
        s+=a
    [print(a,end=" ") for a in s]
    print("")
    bins=binary(len(s))
    dict={}
    sup=""
    pos=""
    zeros={}
    ones={}
    for a in s:
        zeros[a]=[]
        ones[a]=[]
    for bin in bins:
        for b in bin:
            print(b,end=" ")
        print("= ",end="")
        for a in range(len(s)):
            dict[s[a]]=bin[a]
        v=proc(exp,dict)
        print(v)
        for char,ind in zip(s,range(len(s))):
            if bin[ind]==1:
                ones[char].append(v)
            else:
                zeros[char].append(v)
        if v==1:
            sup+="("
            for char in s:
                sup+=(char+"'" if dict[char]==0 else char)
            sup+=")"
        else:
            pos+="("
            for char in s:
                pos+=(char+"'" if dict[char]==1 else char)
                pos+="+"
            pos+=")"
    sup=sup.replace(")(",")+(")
    pos=pos.replace("+)",")")
    print("sum of products: ",sup)
    print("product of sum: ",pos)
    print("irrelevant terms: ",end="")
    for char in s:
        if ones[char]==zeros[char]:
            print(char,end=" ")
    print("\n")
    print("simplification of",exp,"\n")
    history=[]
    simp=exp
    while not simp in history:
        history.append(simp)
        event=checkActions(simp)
        if event!=None:
            simp=event[3]
            if not simp in history:
                print(event[0],":",simp)
                current=simp
    test=checkActions(current,final=True)
    if test!=None:
        print(test[0],":",test[3])
        current=test[3]
    if not "(" in current:
        s=invertExpression(current).replace(")(","")+"'"
        if len(s)<len(current):
            print("invert expression :",s)
            current=s
    print("")
    print(current)
    print("")
