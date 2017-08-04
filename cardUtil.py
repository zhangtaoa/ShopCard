#coding=utf-8


############ 获取 xml 报文中节点的值 ###############
def get_node_value(instr="",node_name="None", rfind = 0):
    if instr == None:
        return ""
    s1 = "<%s>"%node_name
    s2 = "</%s>"%node_name
    if rfind == 0:
        f1 = instr.find(s1)
        if f1 == -1:
            return ""
        f1 = f1 + len(s1)
        f2 = instr.find(s2)
        if f2 == -1 or f1>=f2:
            return ""
        return instr[f1:f2]
    else:
        f1 = instr.rfind(s1)
        if f1 == -1:
            return ""
        f1 = f1 + len(s1)
        f2 = instr.rfind(s2)
        if f2 == -1 or f1>=f2:
            return ""
        return instr[f1:f2]
####################################################


def parse_head(instr=""):
    if instr == None:
       return None,None

    BipCode = get_node_value(instr, "BIPCode")
    if BipCode == "":
       return None,None

    ActivityCode = get_node_value(instr, "ActivityCode")
    if ActivityCode == "":
       return None,None
    
    return BipCode,ActivityCode
    