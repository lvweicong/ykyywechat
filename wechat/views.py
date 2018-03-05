from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from wechat_sdk import WechatBasic
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)

# Create your views here.
token = 'lvweicong'
appid = 'wxa9f31456735f1a20'
appsecret = '9daf2d48f10289e79e580eaf066264a0'

#django默认开启csrf防护，这里使用@csrf_exempt去掉防护
@csrf_exempt
def weixin_main(request):
    wechat = WechatBasic(token = token,
                         appid = appid,
                         appsecret = appsecret)
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    body_text = request.body
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        wechat.parse_data(body_text)
        message = wechat.get_message()

        response = None
        if isinstance(message, TextMessage):
            response = wechat.response_text(content=u'文字信息')
        elif isinstance(message, VoiceMessage):
            response = wechat.response_text(content=u'语音信息')
        elif isinstance(message, ImageMessage):
            response = wechat.response_text(content=u'图片信息')
        elif isinstance(message, VideoMessage):
            response = wechat.response_text(content=u'视频信息')
        elif isinstance(message, LinkMessage):
            response = wechat.response_text(content=u'链接信息')
        elif isinstance(message, LocationMessage):
            response = wechat.response_text(content=u'地理位置信息')
        elif isinstance(message, EventMessage):  # 事件信息
            if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                if message.key and message.ticket:  # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
                    response = wechat.response_text(content=u'用户尚未关注时的二维码扫描关注事件')
                else:
                    response = wechat.response_text(content=u'普通关注事件')
            elif message.type == 'unsubscribe':
                response = wechat.response_text(content=u'取消关注事件')
            elif message.type == 'scan':
                response = wechat.response_text(content=u'用户已关注时的二维码扫描事件')
            elif message.type == 'location':
                response = wechat.response_text(content=u'上报地理位置事件')
            elif message.type == 'click':
                if message.key == 'V1001_hospital_introduce':
                    response = wechat.response_text(content=u'永康医院（原永康市红十字会医院），始建于1952年，是一家集急救、医疗、预防、康复保健、科研和教学为一体的以专科为特色的市直属二级乙等综合性医院，是社保、医保、农保及各商业保险公司定点医院，是残疾人等级鉴定体检定点医院。医院先后荣获爱婴医院、中国红十字会优秀冠名医院、省扶残助残爱心城市建设先进单位、省级卫生先进单位等荣誉。是永康市外来民工孕产妇分娩定点医院，市白内障复明工程免费手术定点医院。医院核定床位200张，职工280余人。开设急诊科、内科、外科、妇产科、眼科、口腔科等20多个专科科室，其中以眼科、口腔科、妇产科为主，眼科是永康市重点学科。配备有进口CT机、佳能DR、口腔全景机、阿洛卡彩超、电子胃镜、腹腔镜、阴道镜、锐扶刀、眼科A/B超、玻璃体超声乳化切割一体机、眼底造影机、OCT、全自动综合验光仪等仪器设备。在市卫计局和联想集团的领导下，医院立足“办一所医院、树一方品牌”的宗旨，以大五官、妇产科为先导，大内科、大外科齐头并进，加强发展老年病防治和康复医疗服务，全面提升医疗技术和服务水平，力争打造一所老百姓身边的好医院。服务时间：普通门诊：上午8:00—11:30；下午13:30—17:00 （夏令时：14:00—17:30；急诊：24小时服务')
                elif message.key == 'V1002_hospital_trend':
                    response = wechat.response_text(content=u'我们更名啦！ 2015年5月1日起，原“永康市红十字会医院”正式更名为“永康医院”，名称变更后，医院法律主体地位不变，联系方式、地址保持不变。因医院名称变更给各单位及广大患者带来的不便，我们深感歉意，敬请谅解。特此通告!')
                elif message.key == 'V1003_department_introduce':
                    response = wechat.response_text(content=u'永康医院开设急诊科、内科、呼吸内科、心血管内科、糖尿病专科，肝病专科、外科、肛肠科、骨伤科、男性科、皮肤科、手外科、整形美容科，妇科、产科，儿科生长发育科，眼科、耳鼻喉科、口腔科，中医科、不孕不育科、康复科、肠道门诊、犬伤门诊、健康体检中心、离休干部门诊等诊疗科室。其中眼科、口腔科、妇产科是我市及周边地区规模最大、设备最好、群众最信赖、技术一流的专科治疗中心之一。')
                elif message.key == 'V1005_hospital_culture':
                    response = wechat.response_text(content=u'医院文化：一切为了病人、 一切为了医院、一切为了职工、一切为了工作。')
                elif message.key == 'V2002_zhuyuanxuzhi':
                    response = wechat.response_text(content=u'您好！欢迎您来我院检查治疗，我们将努力为您提供更多的照顾，更好的治疗。同时我们的工作也需要您的理解和支持！谢谢您的配合，祝您早日康复！ 一、住院注意事项：1、保持病房安静整洁卫生，请不要往窗口、阳台外倒水，不要随地吐痰，垃圾及果皮请丢在纸篓内。请不要在走廊 上成群逗留、高声喧哗。 2、为了您和他人的健康和安全，请不要在病区内吸烟、饮酒及使用明火和其他电器。 3、床头上方有呼叫器，在您需要帮助时，可用呼叫器呼叫护士。4、病人的饮食由医师依病情而定。 5、住院期间请您注意安全： （1）请保持卫生间、阳台地面干燥，以免滑倒。请您不要把床摇得太高，以免发生意外。 （2）如您年事已高或身体虚弱或行动不便，务必请家属陪伴不要独自下床活动、入厕等。 （3）病员不得随意外出或在院外住宿，如擅自外出，一切后果自负。 （4）贵重物品如手机、珠宝、现金等请您妥善保管，不要随意放在床头柜、枕头等处，以免遗失，如有遗失责任自负。 （5）请在护士的指导下使用热水袋、电热毯等取暖物，不要擅自使用。 6、请勿接受医院之外药品及治疗品的推销。不可自行邀请外院医师诊治，如需要诊治，您可与主管医师商量。 7、请及时缴费，以免影响您的治疗。 8、在使用空调时，请关闭门窗。请您爱护公物，如有损坏，照价赔偿。 9、在离院前请到住院处结清帐目，有出院带药者请与护士联系。')
                elif message.key == 'V3001_connectus':
                    response = wechat.response_text(content=u'医院地址：永康市胜利街前花园2号\n交通路线：旁边有大润发商场，华联商厦、佳香基、丽中宾馆、中国银行、建设银行、农业银行和民主小学。公交车路线：丽州中路永康医院站牌（K3、K13、H01），九铃东路铃川路口站牌（K2、K16），南苑路南苑一弄站牌（K6、K8、K17）等路线均能到达。\n\n医院总机：0579-87143966\n\n传真号码：0579-87143100 \n\n急救电话：0579-87143999  87143120 \n\n专家预约电话：15372989120')
                else:
                    response = wechat.response_text(content=u'自定义菜单点击事件')
            elif message.type == 'view':
                response = wechat.response_text(content=u'自定义菜单跳转链接事件')
            elif message.type == 'templatesendjobfinish':
                response = wechat.response_text(content=u'模板消息事件')

    return HttpResponse(response)
