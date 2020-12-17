import requests,time

#  version: v1.1-beta-1

def get_classid(cookie):  #获得课程信息
    get_classid_url = 'http://gxcme.jiastudy.cn/teach_class/my/learning/class?termCode=20-21-1&page=1&size=24'
    get_headers = {
        'Cookie' : cookie,
        'Host' : 'gxcme.jiastudy.cn',
        'Referer' : 'http://gxcme.jiastudy.cn/my/index.html',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    }
    get_classid_list = requests.get(url=get_classid_url,headers=get_headers)
    ck = get_classid_list.cookies
    print(ck)
    class_list = (get_classid_list.json())['body']['records']   ##调用json返回字典
    coures_id_list = []

    print('{}\t{:<20}\t{:<20}\t{}\t{:<10}'.format('状态','课程名称','课程ID','任课老师','班级'))
    for i in range(9):
        class_info = class_list[i]
        course_title = class_info['course']['title']
        course_id = class_info['courseId']
        course_isRecommend = class_info['course']['isRecommend']
        course_teacher = class_info['mainTeacher']['name']
        class_id = class_info['name']
        coures_id_list.append(course_id)
        print('|{4}|\t{0:<20}\t{1:>}\t{2}\t\t{3:<10}'.format(course_title,course_id,course_teacher,class_id,course_isRecommend))  
    return coures_id_list

def get_user(cookie):   #获得学生信息
    get_user_url = "http://gxcme.jiastudy.cn/users/current"
    get_headers = {
        'Cookie' : cookie,
        'Host' : 'gxcme.jiastudy.cn',
        'Referer' : 'http://gxcme.jiastudy.cn/my/index.html',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    }
    get_user = ((requests.get(url=get_user_url,headers=get_headers)).json())['body']
    user_name = get_user['name']
    user_userid = get_user['username']
    user_lasttime = get_user['userProfile']['lastLogTime']
    print("欢迎:{}\t学号:{}\t最后日志时间:{}".format(user_name,user_userid,user_lasttime))


print('========欢迎使用机电云课堂脚本,当前版本为:v1.1-beta-1=========')
cookie = ('SESSION='+str(input('请输入cookie:')))
print('=====================Initializing==========================')
get_user(cookie)
get_classid(cookie)
time.sleep(50)
