from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from wechat_sdk import WechatBasic

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
        if message.type == 'text':
            if message.content == 'wechat':
                response = wechat.response_text(u'^_^')
            else:
                response = wechat.response_text(u'文字')
        elif message.type == 'image':
            response = wechat.response_text(u'图片')
        else:
            response = wechat.response_text(u'未知')

    return HttpResponse(response)
