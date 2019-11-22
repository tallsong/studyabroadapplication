from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.template import  RequestContext,loader
from .models import Universty
# Create your views here.
def index(request):
    print('11')
    university_list = Universty.objects.order_by('id')
    print(type(university_list))
    university_list=', '.join(u.name for u in university_list)
    template = loader.get_template('index.html')
    context = {
        'universitylist': "havard",
        'university_list':university_list,
    }
    print(type(university_list))
    return render(request, 'index.html', context)  
    #页面重定向：服务器不返回页面，而是告诉浏览器再去请求其他的url。
    # return render(request,'index.html')

def ajax(request):
    for i in request.META:
        print(request.META[i])
    return HttpResponse("okkkkkkkkkkkkkk"+str(request.body)+request.get_host()+request.get_full_path())




def detail(request, question_id):
    return HttpResponse("You're looking at university %s." % university_id)



