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
                if message.key == 'V1001_GOOD':
                    response = wechat.response_text(content=u'永康医院（原永康市红十字会医院），始建于1952年，是一家集急救、医疗、预防、康复保健、科研和教学为一体的以专科为特色的市直属二级乙等综合性医院，是社保、医保、农保及各商业保险公司定点医院，是残疾人等级鉴定体检定点医院。医院先后荣获爱婴医院、中国红十字会优秀冠名医院、省扶残助残爱心城市建设先进单位、省级卫生先进单位等荣誉。是永康市外来民工孕产妇分娩定点医院，市白内障复明工程免费手术定点医院。医院核定床位200张，职工280余人。开设急诊科、内科、外科、妇产科、眼科、口腔科等20多个专科科室，其中以眼科、口腔科、妇产科为主，眼科是永康市重点学科。配备有进口CT机、佳能DR、口腔全景机、阿洛卡彩超、电子胃镜、腹腔镜、阴道镜、锐扶刀、眼科A/B超、玻璃体超声乳化切割一体机、眼底造影机、OCT、全自动综合验光仪等仪器设备。在市卫计局和联想集团的领导下，医院立足“办一所医院、树一方品牌”的宗旨，以大五官、妇产科为先导，大内科、大外科齐头并进，加强发展老年病防治和康复医疗服务，全面提升医疗技术和服务水平，力争打造一所老百姓身边的好医院。服务时间：普通门诊：上午8:00—11:30；下午13:30—17:00 （夏令时：14:00—17:30；急诊：24小时服务')
                else:
                    response = wechat.response_text(content=u'自定义菜单点击事件')
            elif message.type == 'view':
                response = wechat.response_text(content=u'自定义菜单跳转链接事件')
            elif message.type == 'templatesendjobfinish':
                response = wechat.response_text(content=u'模板消息事件')

    return HttpResponse(response)
