import pymysql
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import pandas as pd


"""""""""""""""""""""""连接数据库"""""""""""""""""""""""

db = pymysql.connect(host='localhost',
                     user='root',
                     password='1203421016',
                     database='zjut_evaluation')
cursor = db.cursor()


"""""""""""""""""""""""设置主界面内容"""""""""""""""""""""""

# 设置主界面
root = tk.Tk()
# 设置标题
root.title('浙江工业大学教师满意度评价系统(主界面)')
# 设置窗口大小
root.geometry("500x600")
# 设置窗口是否可变True：可变，False：不可变
root.resizable(width=True, height=True)
# 提示语句
root_tip = tk.Label(root, text='请选择进入哪种界面\n请不要同时打开多个副界面\n内容仅为作业使用\n与实际情况并不相符', font=('华文仿宋', 20), fg='blue')
root_tip.place(x=50, y=30, width=400, height=120)


"""""""""""""""""""""""增加评价数据"""""""""""""""""""""""

# 查询添加的教师与课程是否是原有的以及是否重复
def mysql_add_check(atid, bcid, csid):
    cursor.execute('select distinct tid from teacher')
    resulttid = cursor.fetchall()
    cursor.execute('select distinct cid from course')
    resultcid = cursor.fetchall()
    cursor.execute('select sid, cid, tid from evaluation')
    resulttcs = cursor.fetchall()
    flagtid = 0
    for i in range(len(resulttid)):
        if atid in resulttid[i]:
            flagtid = 1
    flagcid = 0
    for i in range(len(resultcid)):
        if bcid in resultcid[i]:
            flagcid = 1
    flagtcs = 1
    for i in range(len(resulttcs)):
        if atid in resulttcs[i] and  bcid in resulttcs[i] and csid in resulttcs[i]:
            flagtcs = 0
    if flagtid and flagcid and flagtcs:
        return True
    else:
        return False

# 向数据库增加数据
def mysql_add_data(a, b, c, d, e, f):
    cursor.execute('select max(eid) from evaluation')
    eid = cursor.fetchone()[0]
    nexteid = str(int(eid) + 1).zfill(6)
    sql = "insert into evaluation values(%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (nexteid, a, b, c, d, e, f))
    db.commit()

# 进入增加界面
def add_data():
    # 产生一个在root界面之上的界面，并设置基本数据
    ad_wd = tk.Toplevel()
    ad_wd.title('欢迎增加教师评价数据(副界面)')
    ad_wd.geometry("700x500")
    ad_wd.resizable(width=True, height=True)

    # 设置提示
    ad_tip = tk.Label(
        ad_wd, text='打*必填，提交后无法修改，只能增加库中原有的课程与教师',
        font=('华文仿宋', 16))
    ad_tip.place(x=85, y=5, width=550, height=60)

    # 学生学号
    lb_sid = tk.Label(ad_wd, text="*学生学号:", font=('华文楷体', 14))
    lb_sid.place(x=10, y=60, width=100, height=30)
    en_sid = tk.Entry(ad_wd)
    en_sid.place(x=120, y=60, width=300, height=30)
    # 课程编号
    lb_cid = tk.Label(ad_wd, text="*课程编号:", font=('华文楷体', 14))
    lb_cid.place(x=10, y=120, width=100, height=30)
    en_cid = tk.Entry(ad_wd)
    en_cid.place(x=120, y=120, width=300, height=30)
    # 教师编号
    lb_tid = tk.Label(ad_wd, text="*教师编号:", font=('华文楷体', 14))
    lb_tid.place(x=10, y=180, width=100, height=30)
    en_tid = tk.Entry(ad_wd)
    en_tid.place(x=120, y=180, width=300, height=30)
    # 评价内容-教学水平
    lb_equality = tk.Label(ad_wd, text="*教学水平:", font=('华文楷体', 14))
    lb_equality.place(x=10, y=250, width=100, height=30)
    cm_equality = ttk.Combobox(ad_wd,
                               values=('教学水平高', '教学水平较高',
                                       '教学水平中等', '教学水平较低',
                                       '教学水平低'),
                               state='readonly')
    cm_equality.place(x=120, y=250, width=120, height=30)
    # 思想教育
    lb_eidea = tk.Label(ad_wd, text="*思想教育:", font=('华文楷体', 14))
    lb_eidea.place(x=10, y=320, width=100, height=30)
    cm_eidea = ttk.Combobox(ad_wd,
                            values=('思想教育频繁', '思想教育较频繁',
                                    '思想教育较少', '思想教育基本没有'),
                            state='readonly')
    cm_eidea.place(x=120, y=320, width=120, height=30)
    # 课程难度
    lb_edifficult = tk.Label(ad_wd, text="*课程难度:", font=('华文楷体', 14))
    lb_edifficult.place(x=10, y=390, width=100, height=30)
    cm_edifficult = ttk.Combobox(ad_wd,
                                 values=('课程难度大', '课程难度中等',
                                         '课程难度小'),
                                 state='readonly')
    cm_edifficult.place(x=120, y=390, width=120, height=30)

    # 提交按钮
    def commit_confirm():
        # 判断是否为空
        if not(en_sid.get() and en_cid.get() and en_tid.get() and cm_equality.get() and cm_eidea.get() and cm_edifficult.get()):
            mb.showerror(title='很抱歉', message='有内容为空')
        else:
            # 判断增加的教师编号和课程编号是否原有与重复
            if mysql_add_check(en_tid.get(), en_cid.get(), en_sid.get()):
                mysql_add_data(en_tid.get(), en_sid.get(), en_cid.get(
                ), cm_equality.get(), cm_eidea.get(), cm_edifficult.get())
                mb.showinfo(title='恭喜', message='提交成功')
            else:
                mb.showerror(title='很抱歉', message='输入的教师编号或课程编号不是系统中原有的，或您已提交过对该课程该老师的评价')
    commit_button = tk.Button(ad_wd,
                              text='提交',
                              font=('华文楷体', 14),
                              command=commit_confirm)
    commit_button.place(x=525, y=200, width=120, height=90)

    # 返回按钮
    def back():
        ad_wd.destroy()
    back_button = tk.Button(ad_wd,
                            text='返回',
                            font=('华文楷体', 14),
                            command=back)
    back_button.place(x=525, y=350, width=120, height=90)

    ad_wd.mainloop()

# 进入增加界面的按钮
add_data_button = tk.Button(root,
                            text='进行教师评价(仅学生)',
                            font=('华文楷体', 14),
                            command=add_data)
add_data_button.place(x=145, y=200, width=200, height=60)


"""""""""""""""""""""""查询评价数据"""""""""""""""""""""""

# 向数据库查询符合条件的数据
def mysql_search_data(a, b, c, d):
    # 判断输入的是教师编号还是姓名
    if len(a) == 0:
        tidsql = 'true'
    else:
        if a.isdigit():
            tidsql = "(evaluation.tid in (select tid from teacher where tid like '%s'))" % str('%' + a + '%')
        else:
            tidsql = "(evaluation.tid in (select tid from teacher where tname like '%s'))" % str('%' + a + '%')
    # 判断输入的是课程编号还是姓名
    if len(b) == 0:
        cidsql = 'true'
    else:
        if b[1:].isdigit():
            cidsql = "(evaluation.cid in (select cid from course where cid like '%s'))" % str('%' + b + '%')
        else:
            cidsql = "(evaluation.cid in (select cid from course where cname like '%s'))" % str('%' + b + '%')
    # 判断课程学分
    if len(c) == 0:
        ccreditsql = 'true'
    else:
        ccreditsql = "(evaluation.cid in (select cid from course where ccredit = '%s'))" % c
    # 判断教师性别
    if d == '不作要求':
        tsexsql = 'true'
    else:
        tsexsql = "(evaluation.tid in (select tid from teacher where tsex = '%s'))" % d
    # 查询语句
    sql = "select evaluation.tid, evaluation.cid, evaluation.equality, evaluation.eidea, evaluation.edifficult from evaluation where %s and %s and %s and %s" % (tidsql, cidsql, ccreditsql, tsexsql)
    cursor.execute(sql)
    result = cursor.fetchall()
    result_show = pd.DataFrame(result)
    result_show.columns = ['教师编号', '课程编号', '教学水平', '思想教育', '课程难度']
    result_show.to_excel('inquiry_result.xlsx')

# 进入查询界面
def search_data():
    sd_wd = tk.Toplevel()
    sd_wd.title('欢迎查询教师评价数据(副界面)')
    sd_wd.geometry("700x500")
    sd_wd.resizable(width=True, height=True)

    # 设置提示
    sd_tip = tk.Label(sd_wd, text='可任选条件，空白默认对该条件不进行筛选，性别必选', font=('华文仿宋', 16))
    sd_tip.place(x=95, y=5, width=500, height=60)

    # 教师编号或姓名
    lb_tidname = tk.Label(sd_wd, text="教师编号或姓名:", font=('华文楷体', 14))
    lb_tidname.place(x=10, y=60, width=150, height=30)
    en_tidname = tk.Entry(sd_wd)
    en_tidname.place(x=170, y=60, width=150, height=30)
    # 课程编号或名称
    lb_cidname = tk.Label(sd_wd, text="课程编号或名称:", font=('华文楷体', 14))
    lb_cidname.place(x=10, y=120, width=150, height=30)
    en_cidname = tk.Entry(sd_wd)
    en_cidname.place(x=170, y=120, width=150, height=30)
    # 课程学分
    lb_ccredit = tk.Label(sd_wd, text="课程学分:", font=('华文楷体', 14))
    lb_ccredit.place(x=10, y=180, width=100, height=30)
    en_ccredit = tk.Entry(sd_wd)
    en_ccredit.place(x=120, y=180, width=150, height=30)
    # 教师性别
    lb_tsex = tk.Label(sd_wd, text="*教师性别:", font=('华文楷体', 14))
    lb_tsex.place(x=10, y=250, width=100, height=30)
    cm_tsex = ttk.Combobox(sd_wd,
                           values=('F',
                                   'M',
                                   '不作要求'),
                           state='readonly')
    cm_tsex.place(x=120, y=250, width=120, height=30)

    # 查询按钮
    def inquiry_confirm():
        mysql_search_data(en_tidname.get(), en_cidname.get(),
                          en_ccredit.get(), cm_tsex.get())
        mb.showinfo(title='恭喜', message='查询成功，内容会出现在同一文件夹下的inquiry_result.xls中')
    inquiry_button = tk.Button(sd_wd,
                               text='查询',
                               font=('华文楷体', 14),
                               command=inquiry_confirm)
    inquiry_button.place(x=525, y=200, width=120, height=90)

    # 返回按钮
    def back():
        sd_wd.destroy()
    back_button = tk.Button(sd_wd,
                            text='返回',
                            font=('华文楷体', 14),
                            command=back)
    back_button.place(x=525, y=350, width=120, height=90)
    sd_wd.mainloop()

# 进入查询界面的按钮
search_data_button = tk.Button(root,
                               text='查询教师评价',
                               font=('华文楷体', 14),
                               command=search_data)
search_data_button.place(x=145, y=300, width=200, height=60)


"""""""""""""""""""""""删除评价数据"""""""""""""""""""""""

# 查询将删除的记录是否存在的
def mysql_delete_check(a, b):
    cursor.execute('select sid, cid from evaluation')
    result = cursor.fetchall()
    flag = 0
    for i in range(len(result)):
        if a in result[i] and b in result[i]:
            flag = 1
    if flag:
        return True
    else:
        return False

# 对数据库中的数据进行删除
def mysql_delete_data(a, b):
    sql = 'delete from evaluation where sid = %s and cid = %s'
    cursor.execute(sql, (a, b))
    db.commit()

# 进入删除界面
def delete_data():
    dd_wd = tk.Toplevel()
    dd_wd.title('删除教师评价数据(副界面)')
    dd_wd.geometry("700x500")
    dd_wd.resizable(width=True, height=True)

    # 设置提示
    sd_tip = tk.Label(
        dd_wd, text='仅可通过学生学号和课程编号删除对应评价数据(均需填入内容)', font=('华文仿宋', 16))
    sd_tip.place(x=60, y=5, width=600, height=60)

    # 学生学号
    lb_sid = tk.Label(dd_wd, text="学生学号:", font=('华文楷体', 14))
    lb_sid.place(x=10, y=60, width=150, height=30)
    en_sid = tk.Entry(dd_wd)
    en_sid.place(x=170, y=60, width=150, height=30)
    # 课程编号
    lb_cid = tk.Label(dd_wd, text="课程编号:", font=('华文楷体', 14))
    lb_cid.place(x=10, y=120, width=150, height=30)
    en_cid = tk.Entry(dd_wd)
    en_cid.place(x=170, y=120, width=150, height=30)

    # 删除按钮
    def delete_confirm():
        if not (en_sid.get() and en_cid.get()):
            mb.showerror(title='很抱歉', message='有内容为空')
        else:
            # 判断将删除的内容是否原有
            if mysql_delete_check(en_sid.get(), en_cid.get()):
                mysql_delete_data(en_sid.get(), en_cid.get())
                mb.showinfo(title='恭喜', message='删除成功')
            else:
                mb.showerror(title='很抱歉', message='学生学号和课程编号原纪录中没有匹配的')
    delete_button = tk.Button(dd_wd,
                              text='删除',
                              font=('华文楷体', 14),
                              command=delete_confirm)
    delete_button.place(x=525, y=200, width=120, height=90)

    # 返回按钮
    def back():
        dd_wd.destroy()
    back_button = tk.Button(dd_wd,
                            text='返回',
                            font=('华文楷体', 14),
                            command=back)
    back_button.place(x=525, y=350, width=120, height=90)
    dd_wd.mainloop()

# 进入删除界面的按钮
search_data_button = tk.Button(root,
                               text='删除教师评价',
                               font=('华文楷体', 14),
                               command=delete_data)
search_data_button.place(x=145, y=400, width=200, height=60)


"""""""""""""""""""""""退出评价系统"""""""""""""""""""""""

# 退出前删除
def quit_mysql():
    cursor.close()
    db.close()
    root.destroy()

# 退出的按钮
search_data_button = tk.Button(root,
                               text='退出评价系统',
                               font=('华文楷体', 14),
                               command=quit_mysql)
search_data_button.place(x=145, y=500, width=200, height=60)

# 进入消息循环，即显示界面
root.mainloop()
