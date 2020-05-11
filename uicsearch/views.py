from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from uicsearch.forms import SearchForm
from analyse_query import analyse_query, initialize_objects
from PageRanker import page_rank

# Create your views here.
# Extremely bad code with no design patterns or code standards implemented. 
# was created in a hurry. Sorry if you got confused


class HomeView(TemplateView):

    def __init__(self):
        self.thread_init = 0
        self.thread_post_init = 0

    def background_process(self,request):
        print('initializing')
        self.thread_init = 1
        initialize_objects()
        print("done, reloading")
        self.thread_post_init = 1
        if request.method == 'GET':
            self.get(request)
        else:
            self.post(request)

    def get(self, request):
        print("GET")
        query = request.GET.get('query', '')
        option = request.GET.get('result_size', 10)
        pagerank_flag = True if int(
            request.GET.get('eval_func', '0')) == 1 else False
        if '' in (query, option, pagerank_flag):
            if(self.thread_init == 0 and self.thread_post_init == 0):
                import threading
                t = threading.Thread(target=self.background_process, args=(request,), kwargs={})
                t.setDaemon(True)
                t.start()
            form = SearchForm()
            print("Def Page")
            return render(request=request,
                          template_name='uicsearch/base_generic.html',
                          context={'form': form})
        else:
            form = SearchForm(request.GET)
            link_list, doc_list, cossim_list, pagerank_list, expanded_queries = analyse_query(
                query, option, pagerank_flag)
            if (link_list =="None"  or doc_list == "None"  or cossim_list == "None"  or pagerrank_list == "None"  or expanded_queries == "None" ):
                args = {
                    'form': form,
                    'data': 'Please wait. The objects are initializing. Atleast 5 minutes are needed at most. The page will refresh automatically',
                    
                }
                return render(request=request,
                          template_name='uicsearch/index_wait.html',
                          context=args)
            args = {
                'form': form,
                'data': zip(link_list, doc_list, cossim_list, pagerank_list),
                'expanded_queries': expanded_queries
            }
            return render(request=request,
                          template_name='uicsearch/index.html',
                          context=args)

    def post(self, request):
        if request.method == 'POST':
            # print(request.POST)
            form = SearchForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                option = form.cleaned_data['result_size']
                pagerank_flag = True if int(
                    form.cleaned_data['eval_func']) == 1 else False
                link_list, doc_list, cossim_list, pagerank_list, expanded_queries = analyse_query(
                    query, option, pagerank_flag)
                if (link_list =="None"  
                or doc_list == "None"  
                or cossim_list == "None"  
                or pagerank_list == "None" 
                or expanded_queries == "None" ):
                    args = {
                        'form': form,
                        'data': 'Please wait. The objects are initializing. Atleast 5 minutes are needed at most. The page will refresh automatically'
                    }
                    return render(request=request,
                            template_name='uicsearch/index_wait.html',
                            context=args)                    
        args = {'form': form,
                'data': zip(link_list, doc_list, cossim_list, pagerank_list),
                'expanded_queries': expanded_queries
                }

        return render(request=request,
                      template_name='uicsearch/index.html',
                      context=args)


class PageRankView(ListView):
    def get(self, request):
        page = request.GET.get('page', 1)
        pageranks_list = sorted(tuple(dict(page_rank()).items()
                                      ), key=lambda X: X[1], reverse=True)
        paginator = Paginator(pageranks_list, 20)
        try:
            pageranks = paginator.page(page)
        except PageNotAnInteger:
            pageranks = paginator.page(1)
        except EmptyPage:
            pageranks = paginator.page(paginator.num_pages)

        return render(request=request, template_name='uicsearch/pagerank.html', context={'pageranks': pageranks})
