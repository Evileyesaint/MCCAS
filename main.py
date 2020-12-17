########请在下面填写账号和密码#########
uid = ''            #账号
pws = ''            #密码
########例如######
# uid = 'abc001'    #账号
# pws = 'abcded'    #密码

#  version: v1.2-beta-1

import base64
import json
import requests
import os
import time

def Initialize(uid,pws):
    if uid=='' and pws=='':
        print('未检测到账号和密码,请查看是否配置好？')
        print('打开脚本,在第二第三行填写好密码再运行')
        quit()
    else:
        return ''
def get_classid():  #获得课程信息
    get_classid_url = 'http://gxcme.jiastudy.cn/teach_class/my/learning/class?termCode=20-21-1&page=1&size=24'
    get_classid_list = s.get(url=get_classid_url)
    class_list = (get_classid_list.json())['body']['records']   ##调用json返回字典
    x = len(class_list)
    course_title_list = []    #初始化所有信息列表
    course_id_list = []
    course_teaching_list = []
    print('{} {}\t{:<20}\t{:>20}\t\t{:}\t{:<10}'.format('序号','状态','课程名称','课程ID','任课老师','班级'))
    for i in range(x):
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
    get_user = ((s.get(url=get_user_url)).json())['body']
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

def join_course(cid,s):   ##进入课程，注意这里不是授课课堂里面，而是外面！
    get_course_url = 'http://gxcme.jiastudy.cn/teach_class/'+str(cid)+'/lesson/my/task/schedule'
    get_course_info = s.get(url=get_course_url).json()
    schedule_list = get_course_info['body']
    courseId_list = []    #初始化，课堂ID列表
    status_list = []      #初始化，课堂状态列表
    coursetitle_list = [] #初始化，课堂名称列表
    print('=============================================================')
    get_info_url = 'http://gxcme.jiastudy.cn/teach_class/'+str(cid)+'/head_info'
    class_info = s.get(url=get_info_url).json()
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

def join_classroom(cid,crid,s):      #进入课堂里面，需要课程id和课堂id
    try:   #检测是否有上课内容
        classroom_url = 'http://gxcme.jiastudy.cn/teach_class/'+str(cid)+'/lesson/'+str(crid)+'/learn/chapter_task'
        classroome_get = (s.get(url=classroom_url).json())['body']
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
def join_classroom_refresh(cid,crid,s): 
    try:   #检测是否有上课内容
        classroom_url = 'http://gxcme.jiastudy.cn/teach_class/'+str(cid)+'/lesson/'+str(crid)+'/learn/chapter_task'
        classroome_get = (s.get(url=classroom_url).json())['body']
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
                html_get = s.post(url=url,data=Payload)
                print(html_get.text)
    except:
        time.sleep(1.5)
        print('====没有发现任务，等待更新====')

def base64_api(uname,pwd,img):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64",json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""

def login():
    print('正在尝试获取验证码.....',end='')
    s.get('http://cas.gxcme.edu.cn/cas/login?service=http%3A%2F%2Fgxcme.jiastudy.cn%3A80%2Flogin%2Fca')
    imgs = s.get('http://cas.gxcme.edu.cn/cas/kaptcha?captchaKey=b006faa6-fc31-3a31-9b0a-515c5d2ce9fd1606035656932&amp;v=1606035656932')
    parent = os.path.dirname(os.path.realpath(__file__))  # 从当前文件路径中获取目录
    path = parent + '\img.jpg'    #这里使用\转义符号,可能会警告,其实无影响
    with open(path,"wb") as img:
        img.write(imgs.content)
    code = base64_api(uname='kuaishibie003', pwd='test010203', img=path)
    print('获取成功: '+str(code))
    info = {
        'username' : uid,
        'password' : pws,
        'captcha' : code,
        '_eventId' : 'submit',
        'geolocation' : '',
        'captchaKey' : 'ec3dc2a8-65fb-7637-5949-66bad83e13441606033415583',
        'submit' : '%E7%99%BB%E5%BD%95',
        'execution' : '4b5d894a-611b-479e-ad7e-a314d6762899_ZXlKaGJHY2lPaUpJVXpVeE1pSjkuYkhGclFsVnhWMU5OYVhacVFrOWFkbWx2U2paeFpqWjFkV1o2VG1GeVMxZFJkMDVpYkZGdE1IUkpkRWMzWTBaM1V6TlFTVk5wYm1Zdk5FNVVUMWhoYmtOc2FIbFJNMjFUYlhZcmR5OVNUbTFDVFVaUFQwSlVURGREZEVad00xVnNXRU5xTkRKQmF5OXBRbFE0Y25CVlVHZHJWbTlZTXpnNVJIUnZWVkkyTTJ4RWNHdFJhQ3MyVGxKamRWWlhNemsxZWtOdE5XNHZRazh5TUhSV1dIcHpaVTVpYkU5d04zUXJTMkV2TVZvemVtNHhWVmR5YlRCdVREVXdaVlk0TlhWVk1tZzVjbHBXTUhRMVNYVnNha1JRVTNvcmQzVjBWRzE1UW1jNGN6RTVPVkZMT1ZSR1NrNHJUbWgyVFVWcmRHdDNVbGhYU0d4aVUyWndOMGs0Wm5nM1VqTnZiVXB2VUdKemFrVjNPVGxzZWpCWmVGWk5XSGRCYzAxR056ZFNiVmN2Um1GVFVYWkdkVVpDZVd3MmMzVjBWSFpVYWpRdll6ZFlTVnAxYVRCRVlrcHVUMDh3U2tRMFIxWTJSVzk1Ynl0Qk5uaEpTMVI0VEUwMmVYZGxNbU0zWXpSS1ZFcGpUMUk0WVhsWmMydEtPVEl4Y0ZKWU9EUnJRbWR4YVRSNVJIZ3diWEZTVlZOaVJHbHhhMVpQZFVoSmRVVnlZMjFpT1RGQ05teEhjVkpvVldKV01rbFRXall6TVhKNWNYVlpOMFV6V0hOM2RGRjJabkZESzB0V0t6aFpTMDFEWldKM0wzTk5PRGxFVTJaNFNrSnpZMmxKUVdrMU9UUllkR0V4V0dSSVFXbG5UWGxGT1RWQmVIcE1NMGRIVWpOMk1XaHRRemgzWmtsVWNpdDBhVkV3TkZFd2RGSllPRkl5YzFwWlpWWklNbmhXV21WNmJtZHpSSG8yYzJjemNEVTVkRU55WmtwdmNVZzBjRVpvVUZSRll5OUVSVXhsWTJ0Nk1UbFVWRWhWYTNjNU5XWnNiVU5rV0VVd1JpdDJNM05yZFVNelYwUkRhRFpDU1hGU1pISmpVbEp0TmtrMVJDOU1SbG8zTW1kT1NuRjNaazVVYkZkNk0zQmtiRlpqYlRabWJXNXBkRW92WjJSUmJISnBhbEJMV21OamFEQndkRlZNZWtGMGRGRTVRVnAyVVZoVU4zUkpjSGxZVUZObFVFVkRZak5UU1RGa1dFUnRhR2hFT1hoUmF5dG9hV00yVkUxSFJrZzJibEJqVmtReFIzVk9XRWwxYjJkTmRGUlVSRFpsVVRCdGVEZHBRVFYzWjBoc2VVcHhjbTF5Y0hWcE5tNUZUbTlGYVROVVFtRXphazAzU1RkNVVFWnZkVk5EWmpOMGVUazFjWHBtTURkcmMyNUpiRXBqTkhGVFlsZDNSME5VYVVKWGVXUlBUVTlwUTFKMVNVOW5kbWRRVDBVNFUzVmlSR2R2UzJGS2FtaE1SMnRWYnpsNGVsWmtNalZqUzFrclFXSk1ibXh5T1daSVl5OTJjWE5OYUZab1VVaDNUMEphZDBocmEzSjBTV05OY0hwVFdXVnNPVEJvYWxKUkszSXpUVkExVlRKeFZGbG5Ra0poVVhRek4wWmpiR1ZvYkRWa1IySlpLMWh5WjBaM1RWQXZjVWg1TW1ORlIzVlpVSE55ZUd4MVlsQm9NRWxGU1hGT1R6WTFZV28yTnpWcVFuQnpkMW8wV1hVeGVXdFRUVkl2U2xSemJHMUdjVEJOZHpVMmJXRXpOV1U1UjBsdlUzRTJOMVI1UjI1cVIxRjZaMEpLYlROdWRXRk9aRkY1TkVFMFRuUkVWRmxFV0dWNlFUUmhiWGxpUTBSemVuQm1PRFJEVjJFeU1Fc3pUVGhJWmlzek9UbEZZV0V4YjBWeVNFczJMMDFSTVdJd2MzWk5jV2gwYVVSbVpHRlJlRVpoV25reU9VeG1SMmRNYldsc1kzUlNNbUpST1c1TGFFMUlhR2N3WTNWVVRqZFlRWGhWYTBOSVdHOU9iRUZLV2xscFYwUndNV0pHTWxsemEzZ3ZLME5PU2toMWFubzVVVkZ5ZEZSek1uTXpaR1p4WVVaaGJXUXdhVU00ZVVOd1VFZ3dOMVZyU1ZGbE9VUllXa012WkdjNVUyZHlSekZaWmpOWVNEbExXVFZQUXpaMWJtSTBNVEptVTJWQ1ZqQnBOWEV3VUhFNVVHRnBkVTFJYmxoSlYwRXZSRzVoZFhwMloxUnVUa1JEVlVaTFNHaHFUME5UTTJ4NVVWSlNORmwxU0hWQ2QydG5iVmhLTTNwek9EWldWbkV3TjJWaE1TdG1hbVJNV1VZcmFYRlFVbEp1ZVNzdldFODRiemc1TUZwVE9YSlpWSE40ZUU5NWFqSlhURmRQYVVjNE1IcGhhMlptV0VKTFdIUnNWa05OYW5vMlpuZGxOVTVzT0dkb1JreERRa3RwTkdwSU5ERjRZMFJMT0UxT05tUnBOMjVFWW1kNFowVnllVnBLYjBaamFsWnVXSFYzU0d0VlRWTnVVV28wUTBZdlUwNXhURmxaZUZSblZHWjNVbkkyVjBaclFXeERWblJoYzNWalNWQlRVR3BZTkd0Rk5HeHNRblJoVW1wWmJXTldWVXBQUlRoVWJHTnVhMHBQUWtvd09UbHpSRVJ3V0VRMGVFWnFWVGczWjNKeWIwSkpNU3RXWkVFcmJrc3ZSVTFSY1M5eFYwaDJUMXBVVDJ4SFlsUnhPSFZ1Vm5OTE5WTm1aVWg1YlRCb1pGUlJkSFZRUTFaaGVrdHlPR3Q0T0hKTlF6WjZlVVpLZUdwRmVGTkRSMHhpVnl0RlIzVkZZV3d4ZEhOdVZYZGlXWEVyYVdzeVowYzBUbFpFWW5wS2VrTTROR1ZyTnl0U1FrTTVNVVZ1VEhsM0swRlpjalU1V2pKcGRYTjRVbWxVVEZsV05rZ3hUM0pJVjJVMFEwZHJZM0U1UzFkb2JVaHdaM2h4Y1dselZsZDBhMGRXTmpSRVJYSndMMEkzUmtReVFYQXhURWcxVURoaWVtTndNVUZQVkVGemMzVkxTbXRzZGpCaVdpdFNTaTlJY25Sa2VHYzFURWhSWVhKcmFHcERRa0ZuU0hGdVVIWTBaemRsTW5Gd04yTjRNRWRJUzJSNGVEUTVlRXhQUTNCbk5XZHBVVXd4UlcxM1dHdzNOVkpCV21zMFVFZ3JiV1JTU25sSVVERlZORTE2VVZCM2NtbFJWbVpEVkZWVFEzSjRiMlZtU1U5T09FTm9RbEpUVmtkaVZHNVFOSE00TW5wUlJ6SldRbmxDWVdWSGVXRm1jMHB6TVdOYWNuUmtielpxZW5aME5qTklaR1I0VDBjcmJ6SnBVRE5qZGxoWFQzSnpURnBKYUVWdFkzWTJPVTl3TlhGSFZteHNVek5YU1ZCd2JtcDVRMEZ2WVcwMmVqRTVVRnAwVTJnMFFrc3JORXdyYlcxU1ZXUnpiREYwVml0cFl6QllRVGRvVGtVeVJUVldkVm94T0dSWmVHZDVkRFZRTmtSMVRtcDJTMjR5YXpoclYySnBOV0k1WjJGTmRqSlVZUzlSVlhkUWFuTlliazlFYUhjemMzRTFLMHR0YlVKTmIzZHVaV3BIYTJGck5UUlhPRUZRYUM5bmVuSktOU3NyY2s1YU4zTnlSMWhyTjFWTk9XVlVjRWhUZURWeldVWlRVVVF4YlVWd1RWbFJjVzk0YlU1Qk1XNVRTM3BqS3pCTVRUWnpTVmhSWVU5SFNFOVdWSEpzWjBoVFNIaG1aSFYxV21scU56QXZlV1JOUnpFNWRqSjRjbGhqTmtoWmVtWmpTV2cwZUU1RGFtVkpaemh4SzFoT1UyOUxkV0kwYW5WcGFGVmFSMUYwZVd4MU1EZzFZVXRqV0dWa1VXOVRjVU5EYkRFMVoyVjZjSEpyVFM5V1psZERVVlpXUjBWUGRYbHdUVGRaYlZSVWFuZDFiMmt3YUZwdUwyMTBjMDRyU25vMVFVdFBMMnQ0V25kMFoybE1ha1JMVFdoSFJtWm9PV2hNWTFCdlMwTTVhVXhhV0dadEwzcFBWazl1VWxOdGExTkVPSEYzWVdKUlYwSnVWM0ZyU2pneWQwdDNkM0JZZGxaSUwxRk5ZMHhEUW5SQmJtNTVSazl0YVc1cFp6Z3JhR1JyVUVwQlJYWnBURVJQUTFsblpGVlNkMU5wZW5kRk1tRkxPRVoyZUdWRGVVRnpVRUZEYTJrMU0yWjBRVlpJYnk5dFpsVlpaMnRaYlVSd1NsSkJaVVZvVlZJMFUxVkNOM2h0WXpWTU0wNHljMVpFTTFkRllWbGphVGRsV1VGWFVGbFZiMHBFT1hReU1IUnNORUo0ZURsSVFXa3laM016WlhBd1owbHpTVko1VERFMWJtOUxVRFZ4WldWVk4wODBiekpoUmtONU1YaGlhMHAyU3paRVpUQnBOMDFuTlZWMWVYUjJUMUpPUlROVGJDdHpNSEkzWXpOT0wwdEVkR3h0UVVOelZVVmtja05vU2xNeFMyczFOVE5DUzB4bFltVkdTV3BVUjFKRE5FZzJhSE13TjNOdVJYQjBOa2xoY0dvemRUVmxNbXRsTUM5T1IzVjJjMUZ3YVdoQ2VrWkhZVEJUYjJ0d1QxWkhWSFptVDJKdVozVldiVUpTZDJFdmIyNTZZMVl4VWt3d2FXMXpUa1JVT0ZvMlVreEhiamhNVldocFpUTnFablpFU2twb1VqaFlRa3B4Vm5FdldHWjROMlJLZEhCSVlqaE5VSE13YzBOelV6Um9XV3BvZDFaaVJYSTBSbFJxVmpndlJVbzNWRTVTVVRaTWNqbFlPVTV4YVRKM1RqTnBXVkJFT0ZsdWQxcG9VemhKY1RobVJqSkZNRTlTVkRBMFFXbDFSWFpXWlVKTlJrNUVkamxuUzFNNU5FeFlTR1JSYWprMVNEZDZTV0pQYTJaUU1IVnNUWGhxVWpKaVFUTTVOVGRqVTA5WVRrMUlkV1p3ZGtsNmVpOVJkRGR4VHpneGNHWjRSRTVSV1hKaGNqUnZhWHBKUTNCUVVTOXFSRzl3UVdKSGRraDNkRTh3UVVWTWIzaG9PR1F2TjJaNVQySmlZM294TUVJd1JqWjVkWGxXUkcxa0wyUjNWVGd3UzA5c1lWSmpOMkpYUTBGS09WWTRWa292VVVodWVHeDFNRzB6U1RCVWJFWkVaVUZPVVdONlZVcGFSVk01YTFkb1JtdEtkVFJPY0hRemVFVkxOMUZ5WWpjemJsazFWUzl0VURRNU5rdGpkMWRrTWxjNFMwVXhUa3RoVmlzM2VYWTBOekpqTDNSRGNqaHVWMlY1ZW5GUFdURTNZVFpsYWtwU2FIQTRXRU5NWjFWNlZYbGhlR1pQUmk5VmJHUkdUR0l3UzAxb1JrMUtRVnBDYm01NVVYbGlja293WTA1TlRuQmxNVTkxYlU5bVZrRnhkR3RFYTFoelJVSllabXRWWTFWVE9WQjRhV3R4UTJGU1owVkRhRFJPZEdnMGNrZzRiM1poVEZOS1VtNHhNelV2VFZsWGIzbFpXbTVJZDJNdllYcDBiMDFRSzNwTldrOWxNblpyWW1kSGIxRkZXbFV5TTB0WFduWlRVV0ZRTHpGVWNIcDRUemhYT0RJMVNUWm1WR012TlZKdWF6SkZkbkp0YjIxUllUUTFTRXg1VlRWYWIwNW9hVTlDVUUxcmJWWjJVRGRvVld0RGNWZFhVMDB3VW1abFMwRmhiM0ExVVZwRmNta3JSM0ZKTDBNNVJVOVZRMGd5U2xkbVRtWXpTWG9yVUZGSGQySjNZM0V3V2tNdmVVUjBaVXQyVldkclVuYzFVV1FyYzJkbFZrSnFaR2R2Vm01aE5reHFTVTVLYVZGdlYzSklOVlkwUmxvM1oybHZha3BKYml0Tk5YTkZjQzlMZW1saGRFNVhVR2d6VUc5cFNXd3pRbGwwTWxOV1owRkhPSEpZV1dKWWFIRmFXR3hyUXpaeGExWnBaV1ZGV1RReVJsQTNhMVV5ZFROTVlXUkdWemRQYm0xRlkxQXplVU16VVdaeU5EUnhSSGxtWVhFck9ESnpQUS5EdGhUMFNpT0h6Qy1HN1JMVWE3WWtYMGhlOUhLdkhIVW9DYVZNazJGbFFJZksyWU9iSVdESmFqRG8xX0xCWmU2RWdfN3JWTWNaR0VIS1BJU0JIVkljZw==',
        }

    print('正在尝试登录........',end='')

    s.post(url='http://cas.gxcme.edu.cn/cas/login?service=http%3A%2F%2Fgxcme.jiastudy.cn%3A80%2Flogin%2Fcas',data=info)   
    z = s.get('http://gxcme.jiastudy.cn/users/current')
    print('Done!')

def main():
    global s
    s = requests.session()
    print('========欢迎使用机电云课堂脚本,当前版本为:v1.2-beta-1=========')
    Initialize(uid,pws)
    login()
    print('=====================Initializing==========================')
    try:
        get_user()         #获得学生信息
        all_info = get_classid()   
        cid=judge(all_info)
        info = join_course(cid,s)
        crid = judge_course(info)
        classroom_info = join_classroom(cid,crid,s)
        judge_class_info(classroom_info)
        while 1:
            tackid_refresh = judge_class_info_refresh(join_classroom_refresh(cid,crid,s))
            answer_race_refresh(tackid_refresh)
    except:
        print('===Error! 也许是验证码错误或者session失效===')

if __name__=='__main__':
    main()