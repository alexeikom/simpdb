#-------------------------------------------------------------------------------
#           Simple DataBaser
#-------------------------------------------------------------------------------
import os
import prettytable as pt

bases_dir="c:\\dbases\\"
curbase_title = 'C U R R E N T  B A S E : '
menu_limit = '+++++++++++++++++++++++++++'
main_menu_str = "'>c'   create db\n"\
                "'>a'   append record to db\n"\
                "'>p'   print db\n"\
                "'>r'   remove record\n"\
                "'>sa'  set active db\n"\
                "'>q'   quit\n"
no_match_fo_str = "no matching db found!\nPress enter to continue.\n"
bad_inp_str = "bad input!\nPress enter to continue.\n"
enter_db_nam_str = "enter db name:"

# globals
dbname = None
workf = None


def create_db(dbn, *args):
    global dbname,workf
    dbname = dbn

    workf=bases_dir+dbn+".csv"
    csvf=open(workf,'w+')
    write_db(csvf, args[0])
    csvf.close()


def write_db(csvf, *args):
    len_a = len(args[0])
    csvf.seek(0)
    for t in range(len_a):
        csvf.write(str(args[0][t]))
        if len_a!=(t+1):
            csvf.write(',')
    csvf.write('\n')


def csv_line_to_lst(csvf):
    line = csvf.readline()
    cnt=0
    tmp_arg=''
    arglst=[]
    while 1:
        if line[cnt]==',':
            arglst.append(tmp_arg)
            tmp_arg=''
        elif line[cnt]=='\n':
            arglst.append(tmp_arg)
            break
        else:
            tmp_arg+=line[cnt]
        cnt+=1
    return arglst


def get_db_len(csvf):
    curr = csvf.tell()
    csvf.seek(0)
    c=csvf.readlines()
    csvf.seek(curr)
    return len(c)-1


def concat_col(*args):
    pos_vec=[0 for k in range(len(args))]
    p=''
    while 1:
        cnt=0
        for t in args:
            cur_pos = t[pos_vec[cnt]:].find('\n')
            if cur_pos==-1:
                break
            p+=t[pos_vec[cnt]:pos_vec[cnt]+cur_pos-1]
            pos_vec[cnt]+=(cur_pos+1)
            cnt+=1
        if cur_pos==-1:
            break
        p+=args[-1][pos_vec[-1]-2]+'\n'
    return p+p[:p.find('\n')]


def rem_lines(csvf, s, r):
    csvf.seek(0)
    c=csvf.readlines()
    for k in s:
        c[k+1]='-REM--'
    for k in range(len(r)):
        if k%2:
            continue
        while r[k+1]>=r[k]:
            r[k]+=1
            c[r[k]]='-REM--'
    new_c=[]
    for k in c:
        if k!='-REM--':
            new_c.append(k)
    return new_c


def parse_inp(strng):
    ranges=[]
    singles=[]
    prev_num=''
    range_det = 0
    for s in range(len(strng)):
        if strng[s]!='-' and strng[s]!=',' and strng[s]!=' ':
            prev_num+=strng[s]
        elif strng[s]=='-':
            if range_det:
                print "error!"
                return
            range_det=1
            ranges.append(int(prev_num))
            prev_num=''
        elif strng[s]==',':
            if range_det:
                ranges.append(int(prev_num))
                range_det=0
            else:
                singles.append(int(prev_num))
            prev_num=''
    if prev_num!='':
        if range_det:
            ranges.append(int(prev_num))
        else:
            singles.append(int(prev_num))
    return singles,ranges


def main_menu():
    return raw_input(menu_limit+'\n'+main_menu_str+menu_limit+'\n'+curbase_title+str(dbname)+'\n')


def r_menu():
    global workf, dbname
    if not dbname:
        tt=raw_input("enter db name or >m for main menu:")
        if tt=='>m':
            return
        if (tt+'.csv') in os.listdir(bases_dir):
            dbname=tt
            workf=bases_dir+tt+".csv"
        else:
            tt=raw_input(no_match_fo_str)
            return

    tt=raw_input("enter line number(s) to remove (for ex: 6, 1-5, 1,3,7) or >m for main menu:")
    if tt=='>m':
        return
    s,r=parse_inp(tt)
    csvf = open(workf,'r')
    lines=rem_lines(csvf,s,r)
    csvf.close()
    csvf = open(workf,'w')
    csvf.writelines(lines)
    csvf.close()


def c_menu():
    tt=raw_input("enter db name or >m for main menu:")
    if tt=='>m':
        return

    cnt=0
    ttl_lst=[]
    while 1:
        t=raw_input("enter title <%d> or enter to finish:"%cnt)
        if t=='':
            if cnt==0:
                t=raw_input("no titles supplied.\nAborting.\nPress enter for main menu")
                break
            else:
                create_db(tt,tuple(ttl_lst))
                break
        ttl_lst.append(t)
        cnt+=1


def p_menu():
    global workf, dbname
    if not dbname:
        tt=raw_input(enter_db_nam_str)
        if (tt+'.csv') in os.listdir(bases_dir):
            dbname=tt
            workf=bases_dir+tt+".csv"
        else:
            tt=raw_input(no_match_fo_str)
            return

    csvf = open(workf,'r')
    db_len = get_db_len(csvf)
    tb = pt.from_csv(csvf)
    ser = pt.PrettyTable()
    ser.add_column('ser #',range(db_len))
    t1=ser.get_string()
    t2=tb.get_string()
    print concat_col(t1,t2)
    csvf.close()


def a_menu():
    global dbname, workf
    if not dbname:
        tt=raw_input(enter_db_nam_str)
        if (tt+'.csv') in os.listdir(bases_dir):
            workf=bases_dir+tt+".csv"
            dbname = tt
        else:
            tt=raw_input(no_match_fo_str)
            return

    csvf = open(workf,'a+')
    args = csv_line_to_lst(csvf)
    new_args=[]
    for k in range(len(args)):
        if len(new_args)>k:
            continue
        j=raw_input("enter"+" '"+args[k]+"' (%s more left!):"%(len(args)-1-k))
        col = j.find(',')
        while col != -1:
            new_args.append(j[:col])
            j=j[col+1:]
            col = j.find(',')
        new_args.append(j)
    # precaution over too much inputs
    if len(new_args)>len(args):
        new_args=new_args[:len(args)]
    write_db(csvf,tuple(new_args))
    csvf.close()


def sa_menu():
    global dbname,workf
    tt=raw_input(enter_db_nam_str)
    if (tt+'.csv') in os.listdir(bases_dir):
        workf=bases_dir+tt+".csv"
        dbname = tt
    else:
        tt=raw_input(no_match_fo_str)


def main():
    t = main_menu()
    if t=='>c':
        c_menu()
        main()
    elif t=='>a':
        a_menu()
        main()
    elif t=='>p':
        p_menu()
        main()
    elif t==">r":
        r_menu()
        main()
    elif t==">sa":
        sa_menu()
        main()
    elif t!='>q':
        tt=raw_input(bad_inp_str)
        main()



if __name__ == '__main__':
    main()
