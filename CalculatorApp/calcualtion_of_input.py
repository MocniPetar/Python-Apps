class calculate:

    def Main_Function(input_):
        
        def parentheses_calculation(list_par,input_c):
            opr,val,p_m_ = [],[],[]
            result1 = 0
            result_1 = 0
            for i in range(list_par[0]+1,list_par[1]):
                if input_c[i] == "+" or input_c[i] == "-" or input_c[i] == "*" or input_c[i] == "/":
                    opr.append(input_copy[i])
                    opr_pos.append(i)
                    if input_c[i] == "+" or input_c[i] == "-":
                        p_m_.append(input_c[i])
                        p_m_pos_.append(i)
                else:
                    val.append(float(input_c[i]))

            new_list_ = []
            i_plus_ = []
            for i in range(len(val)-1):
                if opr[i] == '*':
                    result_1 = val[i] * val[i+1]
                    new_list_.append(result_1)
                    i_plus_.append(val[i+1])
                elif opr[i] == '/': 
                    result_1 = val[i] / val[i+1]
                    result_1 = round(result_1,3)
                    new_list_.append(result_1)
                    i_plus_.append(val[i+1])
                else:
                    new_list_.append(val[i])
            else:
                new_list_.append(val[i+1])
                for i in range(len(i_plus_)):
                    new_list_.remove(i_plus_[i])
                    val = new_list_   

            e=0
            for i in range(len(val)):
                if result1 == 0:
                    result1 = val[i]
                else:
                    if p_m_[e] == "+":
                        result1 += val[i]
                    elif p_m_[e] == "-":
                        result1 -= val[i] 
                    e+=1

            start = 0
            end = 0
            for i in range(len(val_pos)):
                if val_pos[i] == list_par[0]+1:
                    start = i
                elif val_pos[i] == list_par[1]-1:
                    end = i+1
            values[start:end] = [result1]
            val_pos[start:end] = [0]
    
        def plus_minus_removal_from_parentheses(p_m,p_m_pos_,p_m_pos):
            A=0
            p_list = []
            for i in range(len(p_m_pos)):
                if A < len(p_m_pos_):
                    if p_m_pos[i] == p_m_pos_[A]:
                        A+=1
                    else:
                        p_list.append(p_m[i])
                else:
                    p_list.append(p_m[i])
            return p_list

        def operator_removal(operators_c,opr_p,operators_p):
            B=0
            opr_list = []
            for i in range(len(operators_pos)):
                if B < len(opr_p):
                    if operators_pos[i] == opr_p[B]:
                        B+=1
                    else:
                        opr_list.append(operators_c[i])
                else:
                    opr_list.append(operators_c[i])
            return opr_list
        
        d, e, result, result_, p_m, input_copy, values, operators = 0, 0, 0, 0, [], [], [], []
        for i in range(len(input_)):
            if input_[i] == "+" or input_[i] == "*" or input_[i] == "-" or input_[i] == "/":
                input_copy.append(input_[d:i])
                input_copy.append(input_[i])
                d=i+1
            elif input_[i] == "(" or input_[i] == ")":
                input_copy.append(input_[d:i])
                input_copy.append(input_[i])
                d=i+1
        else:
            input_copy.append(input_[d:])

        help_list = []

        for i in range(len(input_copy)):
            if input_copy[i] != '':
                help_list.append(input_copy[i])
        input_copy = help_list

        parentheses = []
        parentheses_col = []
        a=0
        val_pos = []
        p_m_pos = []
        operators_pos = []
        for i in range(len(input_copy)):
            if input_copy[i] == "+" or input_copy[i] == "-" or input_copy[i] == "*" or input_copy[i] == "/":
                operators.append(input_copy[i])
                operators_pos.append(i)
                if input_copy[i] == "+" or input_copy[i] == "-":
                    p_m.append(input_copy[i])
                    p_m_pos.append(i)
            elif input_copy[i] == '(' or input_copy[i] == ')':
                parentheses_col.append(i)
                if a == 1:
                    parentheses.append(parentheses_col)
                    parentheses_col = []
                    a=0
                else:
                    a+=1
            else:
                values.append(float(input_copy[i]))
                val_pos.append(i)
                
        if values != [] and operators != []:
            
            if parentheses != None:
                p_m_pos_ = []
                opr_pos = []
                for i in range(len(parentheses)):
                    parentheses_calculation(parentheses[i],input_copy)

                p_m_copy = list(p_m)
                operators_copy = list(operators)

                p_m = plus_minus_removal_from_parentheses(p_m_copy,p_m_pos_,p_m_pos)
                operators = operator_removal(operators_copy,opr_pos,operators_pos)

            I=0
            while I != len(operators)-1:
                if ((operators[I] == "*" or operators[I] == "/") and (operators[I+1] == "*" or operators[I+1] == "/")):
                    opr_list_elements = []
                    opr_list = []
                    d=0
                    i=0
                    a=0
                    while i != len(operators)-1:            
                        col = []
                        col_1 = []
                        if ((operators[i] == "*" or operators[i] == "/") and (operators[i+1] == "*" or operators[i+1] == "/")):                
                            a=i
                            while (((operators[a] == "*" or operators[a] == "/") and (operators[a+1] == "*" or operators[a+1] == "/")) and a < (len(operators)-2)):
                                col.append(operators[a])
                                col_1.append(a)
                                a+=1
                            else:
                                col.append(operators[a])
                                col_1.append(a)
                                i=a
                            if (a == len(operators)-2 and (operators[a+1] == "*" or operators[a+1] == "/")):
                                col.append(operators[a+1])
                                col_1.append(a+1)
                            opr_list.append(col)
                            opr_list_elements.append(col_1)
                        i+=1
                    b = None
                    results_save = []
                    positions_ = []
                    for i in range(len(opr_list)):            
                        b=None
                        col_values = []
                        for j in range(len(opr_list[i])):                
                            if b == None:                    
                                if opr_list[i][j] == "*":
                                    b = values[opr_list_elements[i][j]] * values[opr_list_elements[i][j]+1]
                                    col_values.append(opr_list_elements[i][j])
                                    col_values.append(opr_list_elements[i][j]+1)
                                else:
                                    b = values[opr_list_elements[i][j]] / values[opr_list_elements[i][j]+1]
                                    col_values.append(opr_list_elements[i][j])
                                    col_values.append(opr_list_elements[i][j]+1)
                            else:                    
                                if opr_list[i][j] == "*":
                                    b = b * values[opr_list_elements[i][j]+1]
                                    col_values.append(opr_list_elements[i][j]+1)
                                else:
                                    b = b / values[opr_list_elements[i][j]+1]
                                    col_values.append(opr_list_elements[i][j]+1)
                        positions_.append(col_values[::len(col_values)-1])
                        results_save.append(b)
                    finale_values = []
                    a=0
                    i=0
                    while i < len(values):            
                        if i != positions_[a][0]:
                            finale_values.append(values[i])
                        elif i == positions_[a][0]:
                            finale_values.append(results_save[a])
                            i=positions_[a][1]
                            if a != len(positions_)-1:
                                a+=1
                        i+=1
                    else:
                        values = list(finale_values)
                    i=0
                    opr_ = []
                    array = []
                    a=0
                    while i != len(operators)-1:
                        if ((operators[i] == "*" or operators[i] == "/") and (operators[i+1] == "*" or operators[i+1] == "/")):
                            array.append(i)
                            array.append(i+1)
                        i+=1
                    set_ = set(array)
                    opr_ = list(set_)
                    opr_.sort()

                    a=0
                    i=0
                    new_opr_list = []
                    Check_0 = False
                    Check = opr_[0]
                    for i in range(len(operators)):
                        if Check == i and i == 0:
                            Check_0 = True
                        if Check_0 == True:
                            if a != len(operators)-1:
                                if i == opr_[a]:
                                    a+=1
                                else:
                                    new_opr_list.append(operators[i])
                            else:
                                new_opr_list.append(operators[i])
                        else:
                            if a < len(opr_):
                                if i == opr_[a]:
                                        a+=1
                                else:
                                    new_opr_list.append(operators[i])
                            else:
                                new_opr_list.append(operators[i])
                    else:
                        operators = new_opr_list
                    break
                I+=1

            new_list = []
            i_plus = []
            for i in range(len(values)-1):
                if operators[i] == '*':
                    result_ = values[i] * values[i+1]
                    new_list.append(result_)
                    i_plus.append(values[i+1])
                elif operators[i] == '/': 
                    result_ = values[i] / values[i+1]
                    result_ = round(result_,3)
                    new_list.append(result_)
                    i_plus.append(values[i+1])
                else:
                    new_list.append(values[i])
            else:
                new_list.append(values[i+1])
                for i in range(len(i_plus)):
                    new_list.remove(i_plus[i])
                    values = new_list

            e=0
            for i in range(len(values)):
                if result == 0:
                    result = values[i]
                else:
                    if p_m[e] == "+":
                        result += values[i]
                    elif p_m[e] == "-":
                        result -= values[i] 
                    e+=1

            result = round(result,3)
            return result