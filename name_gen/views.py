from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.template import loader, RequestContext

from name_gen.models import NGram
import pickle
import name_generator

# Create your views here.
def home(request):
    ngram_files = NGram.objects.all()

    # Load
    with open('ngrams/unigram_counts.pickle', 'rb') as handle:
        unigram_counts = pickle.load(handle)
    with open('ngrams/bigram_counts.pickle', 'rb') as handle:
        bigram_counts = pickle.load(handle) 
    with open('ngrams/trigram_counts.pickle', 'rb') as handle:
        trigram_counts = pickle.load(handle)
    with open('ngrams/fourgram_counts.pickle', 'rb') as handle:
        fourgram_counts = pickle.load(handle)   
    with open('ngrams/fivegram_counts.pickle', 'rb') as handle:
        fivegram_counts = pickle.load(handle)   

    weights = [1,3,5,7,10]

    candidate_name = name_generator.generate_name(weights, unigram_counts, bigram_counts, trigram_counts, fourgram_counts, fivegram_counts)

    template = loader.get_template('name_gen.html')
    context = RequestContext(request, {
        'candidate_name': candidate_name,
    })
    return HttpResponse(template.render(context))