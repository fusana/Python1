import logging;logging.basicConfig(level=logging.INFO)

import asyncio,os,json,time
#asyncio是并发的一种方式，异步IO，当发起一个IO操作，却不用等它结束，可以继续做其他事情，当他结束时，你会得到通知。
from datetime import datetime

from aiohttp import web

def index(request):
	#定义http响应的body
	resp=web.Response(body=b'<h1>Awesome</h1>')
	resp.content_type='test/html;charset=utf-8'
	return resp  

#@装饰符类似于回调函数，把其他函数作为自己的入参，此处等价于asyncio.coroutine(init(loop))
@asyncio.coroutine
def init(loop):
	#init是一个协程
	app=web.Application(loop=loop)
	app.router.add_route('GET','/',index)
	srv=yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)
	#这里调用loop.create_server协程，并且用yield来接收它返回的参数
	logging.info('server started at http://127.0.0.1:9000...')
	return srv

loop=asyncio.get_event_loop()
#获取EventLoop
loop.run_until_complete(init(loop))
#把协程对象交给loop.run_until_complete,执行coroutine
#run_until_complete是一个阻塞调用，直到协程运行结束，它才返回
loop.run_forever()
