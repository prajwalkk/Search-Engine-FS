from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from uicsearch.forms import SearchForm
from analyse_query import analyse_query, initialize_objects
from PageRanker import page_rank

# Create your views here.


class HomeView(TemplateView):

    def background_process():
        print('initializing')
        initialize_objects()
        print("done")


    def get(self, request):
        print("GET")
        query = request.GET.get('query', '')
        option = request.GET.get('result_size', 10)
        pagerank_flag = True if int(
            request.GET.get('eval_func', '0')) == 1 else False
        if '' in (query, option, pagerank_flag):
            import threading
            t = threading.Thread(target=background_process, args=(), kwargs={})
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
