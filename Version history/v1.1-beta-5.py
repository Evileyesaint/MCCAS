import requests,time

#  version: v1.1-beta-5

def initializ(cookie):   #初始化,定义全局请求头(get_headers)
    global get_headers   
    get_headers = {
        'Cookie' : cookie,
        'Host' : 'gxcme.jiastudy.cn',
        'Referer' : 'http://gxcme.jiastudy.cn/my/index.html',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    }

def get_classid():  #获得课程信息
    get_classid_url = 'http://gxcme.jiastudy.cn/teach_class/my/learning/class?termCode=20-21-1&page=1&size=24'
    get_classid_list = requests.get(url=get_classid_url,headers=get_headers)
    class_list = (get_classid_list.json())['body']['records']   ##调用json返回字典
    course_title_list = []    #初始化所有信息列表
    course_id_list = []
    course_teaching_list = []
    print('{} {}\t{:<20}\t{:>20}\t\t{:}\t{:<10}'.format('序号','状态','课程名称','课程ID','任课老师','班级'))
    for i in range(9):
        class_info = class_list[i]
        course_title = class_info['course']['title']
        course_title_list.append(course_title)
        course_id = class_info['id']
        course_id_list.append(course_id)
        course_teaching = class_info['teaching']
        course_teaching_list.append(course_teaching)
        course_teacher = class_info['mainTeacher']['name']
        class_id = class_info['name']
        print(' {5:}  |{4}|\t{0:30}\t{1:}\t{2}\t\t{3:<10}'.format(course_title,course_id,course_teacher,class_id,course_teaching,i))
    print('========================================================')
    return course_teaching_list,course_id_list,course_title_list
    ### 返回包含列表的元组，0是状态，1是课堂id，2是课程名称


def get_user():   #获得学生信息
    get_user_url = "http://gxcme.jiastudy.cn/users/current"
    get_user = ((requests.get(url=get_user_url,headers=get_headers)).json())['body']
    user_name = get_user['name']
    user_userid = get_user['username']
    user_lasttime = get_user['userProfile']['lastLogTime']
    print("欢迎:{}\t学号:{}\t最后日志时间:{}".format(user_name,user_userid,user_lasttime))


def judge(all_info):       ##判断是否有在上课课堂,有的话直接进入课堂，没有即手动选择
    state = all_info[0]
    course_id = all_info[1]
    course_title = all_info[2]
    pd = True in state
    if pd:
        s = state.index(True)
        print('检测到【'+course_title[s]+'】正在上课，正在进入...')
        cid=course_id[s]
        return cid
    else:
        print("没有检测到正在上课的课程，切换选择模式")
        select_id = int(input('请选择你需要进入的课堂，输入序号即可|:'))
        cid = course_id[select_id]
        return cid

def join_course(cid):   ##进入课程，注意这里不是授课课堂里面，而是外面！
    get_course_url = 'http://gxcme.jiastudy.cn/teach_class/'+str(cid)+'/lesson/my/task/schedule'
    get_course_info = requests.get(url=get_course_url,headers=get_headers).json()
    schedule_list = get_course_info['body']
    courseId_list = []    #初始化，课堂ID列表
    status_list = []      #初始化，课堂状态列表
    coursetitle_list = [] #初始化，课堂名称列表
    print('=============================================================')
    get_info_url = 'http://gxcme.jiastudy.cn/teach_class/'+str(cid)+'/head_info'
    class_info = requests.get(url=get_info_url,headers=get_headers).json()
    title = class_info['body']['name']
    classromeid = class_info['body']['className']
    studentNum = class_info['body']['studentNum']
    print('欢迎来到【{}】\t班级:{}\t学生人数:{}'.format(title,classromeid,studentNum))
    print('{}   {}\t{:<20}\t{:<20}'.format('序号','状态','课堂ID','课堂名称'))
    s = -1
    for i in schedule_list:
        i = i   #无意义，防止错误代码高亮Ow<
        s = s+1
        x = schedule_list[s]
        courseId = x['id']
        courseId_list.append(courseId)    
        status = x['status']['desc']
        status_list.append(status)
        coursetitle = x['name']
        coursetitle_list.append(coursetitle)
        print('{:3}  |{}|\t{}\t{}'.format(s,status,courseId,coursetitle))
    print('========================================================')
    return status_list,courseId_list,coursetitle_list
    ### 返回包含列表的元组，0是状态，1是课堂id，2是课程名称


def judge_course(all_info):  ##判断是否有在上课课程,有的话直接进入课程，没有即手动选择
    state = all_info[0]
    course_id = all_info[1]
    course_title = all_info[2]
    pd = '投屏中' in state
    if pd:
        s = state.index('投屏中')
        print('检测到【'+course_title[s]+'】正在上课，正在进入...')
        crid=course_id[s]
        return crid           #crid即是classroome id，课堂id  |  cid是class id是课程id
    else:
        print("没有检测到正在上课的课堂，切换选择模式")
        select_id = int(input('请选择你需要进入的课程，输入序号即可|:'))
        crid = course_id[select_id]
        return crid

def join_classroom(cid,crid):      #进入课堂里面，需要课程id和课堂id
    try:   #检测是否有上课内容
        classroom_url = 'http://gxcme.jiastudy.cn/teach_class/'+str(cid)+'/lesson/'+str(crid)+'/learn/chapter_task'
        classroome_get = (requests.get(url=classroom_url,headers=get_headers).json())['body']
        kz = classroome_get[1]['children']  #课中
        s = -1
        taskTypeName_list = []  #类型
        title_list = []         #名称
        taskid_list = []        #任务id
        taskStatus_list = []    #状态
        print('=============================================================')
        print('序号   状态\t类型\t任务ID\t\t\t名称')
        for i in kz:
            s = s+1
            i = i
            x = kz[s]
            taskid = x['id']      #！！！beta1.4后采用获取id方式
            taskid_list.append(taskid)
            title = x['title']
            title_list.append(title)
            taskTypeName = x['taskTypeName']
            taskTypeName_list.append(taskTypeName)
            taskStatus = x['taskStatus']['desc']
            taskStatus_list.append(taskStatus)
            print('{}    |{}|\t{}\t{}\t{}'.format(s,taskStatus,taskTypeName,taskid,title))
        return taskTypeName_list,taskStatus_list,taskid_list
    except:
        print('=======没有找到上课内容=======')
        return None
    ### 返回包含列表的元组，0是类型，1是状态，2是任务id  


##与join_classroom同理，但是不会反馈任何提醒，用于动态更新任务状态
def join_classroom_refresh(cid,crid): 
    try:   #检测是否有上课内容
        classroom_url = 'http://gxcme.jiastudy.cn/teach_class/'+str(cid)+'/lesson/'+str(crid)+'/learn/chapter_task'
        classroome_get = (requests.get(url=classroom_url,headers=get_headers).json())['body']
        kz = classroome_get[1]['children']  #课中
        s = -1
        taskTypeName_list = []  #类型
        title_list = []         #名称
        taskid_list = []        #任务id
        taskStatus_list = []    #状态
        for i in kz:
            s = s+1
            i = i
            x = kz[s]
            taskid = x['id']      #！！！beta1.4后采用获取id方式
            taskid_list.append(taskid)
            title = x['title']
            title_list.append(title)
            taskTypeName = x['taskTypeName']
            taskTypeName_list.append(taskTypeName)
            taskStatus = x['taskStatus']['desc']
            taskStatus_list.append(taskStatus)
        return taskTypeName_list,taskStatus_list,taskid_list
    except:
        time.sleep(1.5)
        print('=======没有找到上课内容,等待刷新=======')
        return None
    ### 返回包含列表的元组，0是类型，1是状态，2是任务id


def judge_class_info(classroom_info):    #判断是否有抢答任务
    print('=============================================================')
    if classroom_info!=None:
        try:
            taskTypeName_list = classroom_info[0]
            taskTypeName_list.reverse()          
             #把列表翻过来,读第一个即读原最后一个(新任务)    1-5beta版修复只能获得第一个任务的bug
            taskType_w = taskTypeName_list.index('抢答')   #获得相对位置
            taskStatus_list = classroom_info[1]
            taskStatus_list.reverse()                      #列表翻转,获得最新任务位置
            taskStatus_w = taskStatus_list.index('进行中')   #获得相对位置
            taskid_list = classroom_info[2]
            taskid_list.reverse()                           #列表翻转,获得最新任务位置
            pd_taskType = '抢答' in taskTypeName_list       #检测是否有抢答任务
            pd_taskStatus = '进行中' in taskStatus_list     #检测是否有抢答任务
            if pd_taskType and pd_taskStatus and taskType_w==taskStatus_w:    
            #判断是否有抢答任务且位置是否一致，获得后，然后返回tackid
                s = taskType_w
                taskid = taskid_list[s]
                print('获得learn_id',end="")
                print(taskid)
                return None    ##beta1.4直接获得tackid方式
        except:
            print('没有发现正在进行中的抢答任务')
            print('=============================================================')
            return None
    else:
        print('没有发现正在进行中的抢答任务')
        print('=============================================================')
        return None

##与judge_class_info同理，但是不会反馈任何提醒，用于动态更新任务状态
# 1.1-bata-5停用judge_class_info(),使用全局刷新 
def judge_class_info_refresh(classroom_info):    #判断是否有抢答任务
    if classroom_info!=None:
        try:
            taskTypeName_list = classroom_info[0]
            taskTypeName_list.reverse()
            taskType_w = taskTypeName_list.index('抢答')   #获得相对位置
            taskStatus_list = classroom_info[1]
            taskStatus_list.reverse()
            taskStatus_w = taskStatus_list.index('进行中')   #获得相对位置
            taskid_list = classroom_info[2]
            taskid_list.reverse()
            pd_taskType = '抢答' in taskTypeName_list       #检测是否有抢答任务
            pd_taskStatus = '进行中' in taskStatus_list     #检测是否有抢答任务
            if pd_taskType and pd_taskStatus and taskType_w==taskStatus_w:    
            #判断是否有抢答任务且位置是否一致，获得后，然后返回tackid
                s = taskType_w
                taskid = taskid_list[s]
                print('获得任务ID,开始执行  ID：:',end="")
                print(taskid)      
                return taskid     ##beta1.4直接获得tackid方式
            else:
                time.sleep(1)
                print('====没有发现任务，等待更新====')
                return None
        except:
            time.sleep(1)
            print('====没有发现任务，等待更新====')
            return None
    else:
        return None

def answer_race_refresh(tackid_refresh):  #抢答   只抢10次，结束后退出
    try:
        if tackid_refresh!=None:
            url = 'http://gxcme.jiastudy.cn/teach_class/undefined/task/'+tackid_refresh+'/answer-race/student'
            Payload = {}
            for i in range(10):
                i = i
                html_get = requests.post(url=url,headers=get_headers,data=Payload)
                print(html_get.text)
    except:
        time.sleep(1.5)
        print('====没有发现任务，等待更新====')
    
def main():
    print('========欢迎使用机电云课堂脚本,当前版本为:v1.1-beta-5=========')
    cookie = ('SESSION='+str(input('请输入cookie:')))
    print('=====================Initializing==========================')
    try:
        initializ(cookie)  #初始化
        get_user()         #获得学生信息
        all_info = get_classid()   
        cid=judge(all_info)
        info = join_course(cid)
        crid = judge_course(info)
        classroom_info = join_classroom(cid,crid)
        judge_class_info(classroom_info)
        while 1:
            tackid_refresh = judge_class_info_refresh(join_classroom_refresh(cid,crid))
            answer_race_refresh(tackid_refresh)
    except:
        print('===Error! 可能cookie输入错误或者已过期===')


if __name__=='__main__':
    main()