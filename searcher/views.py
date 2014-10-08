#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Create your views here.
#from kombu.transport import django
#from string import join

# from settings import MEDIA_ROOT


## adminactions  ####
#from django.contrib.admin import site
#import adminactions.actions as actions
#
## register all adminactions
#actions.add_to_site(site)
#
##=========================================================================

##=========================================================================


# Photo Admin Methods #######
# @login_required
from accounts import authentication

from djdam.settings import MEDIA_URL

#import searcher.models
from searcher.models import *

### Utility to display Meta info
def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>{0}</td><td>{1}</td></tr>'.format(k, v))
    return HttpResponse('<table>{0}</table>'.format('\n'.join(html)))



## Generic List view of All "Model"'s objects
def object_list(request, model):
    obj_list = model.objects.all()
    template_name = 'searcher/listing/{0}_list.html'.format(model.__name__.lower())
    return render(request, template_name, {'object_list': obj_list})


def search_users_albums_byalbum(request):
    if 'useralbumsearch' in request.GET and request.GET['useralbumsearch']:
        if 'q' in request.GET and request.GET['q']:
            q_album = request.GET['albumid']
            q_user = request.GET['userid']

            results = Product.objects.filter(album__icontains=q_album)
            return render(request, 'search_results.html', {'results': results, 'query': q_album,})


def search_users_albums_bycolorstyle(request):
    if 'useralbumsearch' in request.GET and request.GET['useralbumsearch']:
        if 'q' in request.GET and request.GET['q']:
            q_album = request.GET['albumid']
            q_user = request.GET['userid']

            results = Product.objects.filter(album__icontains=q_album)
            return render(request, 'search_results.html', {'results': results, 'query': q_user,})


@cache_page(60 * 15)
def search_colorstyle(request, q):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        else:
            if len(q) > 9 and q.isdigit():
                errors.append('Please enter a valid Colorstyle.')
            else:
                results = Images.objects.filter(colorstyle__icontains=q)
                #return render(request, 'search_results.html', {'results': results, 'query': q,})
                images = results
                return render(request, 'listing/image_list_page.html', {'images': images, 'query': q, })
    else:
        message = 'You submitted an empty form from views.main using {}.'.format(request.GET['q'])
        return HttpResponse(message)


@cache_page(60 * 15)
def search_brand(request):
#    if 'brandsearch' in request.GET and request.GET['brandsearch']:
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        images = Images.image_select.get_query_set()      ##(photo_date__range=(start_date, end_date))
        results = Product.objects.filter(brand__icontains=q)
        images = []
        for image in images:
            if image.colorstyle == results.colorstyle:
                images.append(image)

        return render(request, 'listing/image_list_page.html', {'results': results, 'images': images, 'query': q,})


# def search_photo_date(request, q):
#     results = ProductionRawZimages.objects.filter(photo_date__icontains=q)
#     return render(request, 'search_results.html', {'results': results, 'query': q})

@cache_page(60 * 15)
def search_photo_date(request, startdate):
    # if 'q' in request.GET and request.GET['q']:
    #     q = request.GET['q']
    if 'startdate' in request.GET and request.GET['startdate']:
        startdate = request.GET['startdate']

        if 'enddate' in request.GET and request.GET['enddate']:
            enddate = request.GET['enddate']
            startend = (startdate, enddate,)

    ##TODO:Convert request.startdate,enddate to py datetime obj

    #if not startend:
    #startend = startdate
    images = Images.image_select.get_query_set()      ##(photo_date__range=(start_date, end_date))
    results = images.filter(photo_date__iexact=startdate)
    #else:
    #    ##TODO:Change to do Range search with End date
    #    images = Images.image_select.get_query_set()      ##(photo_date__range=(start_date, end_date))
    #    results = images.objects.filter(photo_date__range=(start_date, end_date))

    return render(request, 'search_results.html', {'results': results, 'images': results, 'query': startdate,})

    # else:
    #     message = 'Please Do not Enter Anything in text box when searching using dates\n \tPlease remove {} and try again.'.format(request.GET['q'])
    #     return HttpResponse(message)


@cache_page(60 * 15)
def search_keyword(request):
    if 'keywordsearch' in request.GET and request.GET['keywordsearch']:
        if 'q' in request.GET and request.GET['q']:
            q_keyword = request.GET['keyword']
            results = Product.objects.filter(keywords__icontains=q_keyword)
            return render(request, 'search_results.html', {'results': results,
                                                            'query': q_keyword,})


@cache_page(60 * 15)
def main(request):
    """All Queries Get Routed to functions via this regex parser"""
    import re
    regex_datesearch = re.compile(r'.*?[0-9]{4}-[0-3][0-9]-[0-3][0-9]?$')
    regex_colorstyle = re.compile(r'.*?[0-9]{5,9}?$')
    regex_jpg = re.compile(r'.*?[0-9]{9}_[1-6]{1}\.[jpgJPG]{3}$')
    #brands = BrandsLookup.objects.all()
    print dict(request)
    # print brands
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        else:
            if len(q) > 9 and q.isdigit():
                errors.append('Please enter a valid Colorstyle.')
            else:
                if re.findall(regex_colorstyle, q):
                    print q
                    # Render Colorstyle Results
                    resultsimg = Images.objects.filter(
                        colorstyle__icontains=q)
                    resultsdata = Images.objects.filter(
                        colorstyle__icontains=q)
                    return render(request, 'image_results_group.html', {'results': resultsdata,
                                                                        'images': resultsimg,
                                                                        'query': q,})
                #     # search_colorstyle(request,q)
                # elif q in brands:
                #     # Render Brand Results
                #     # search_brand(request, q)
                #     resultsimg = Product.objects.filter(brand__icontains=q)
                #     resultsdata = Product.objects.filter(brand__icontains=q)
                #     return render(request, 'image_results_group.html', {'results': resultsdata, 'query': q,})
                #     #return render(request, 'search_results.html', {'results': resultsdata, 'images': resultsimg, 'query': q},)
                else:
                    try:
                        return render(request, 'search_form.html', {'errors': errors})
                    except:  ## ProductionRawOnfigure.DoesNotExist:
                        print "Search terms not found"
                        pass
    else:
        message = 'You submitted an empty form from views.main using {}.'.format(request.GET['q'])
        return HttpResponse(message)


###################################################################################################
###################################################################################################
#=========================================================================
# Previous Day's Browse Views -- Top Navi Dropdown
# first 3 only return results to views below it that render

###################################################################################################
###################################################################################################

@cache_page(60 * 15)
def query_previous_week(modelname):
    from datetime import timedelta
    from django.utils import timezone
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - \
        timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)
    results = modelname.objects.filter(
        photo_date__gte=monday_of_last_week, photo_date__lt=monday_of_this_week)
    return results

###################################################################################################
###################################################################################################

@cache_page(60 * 15)
def query_current_week(modelname):
    from datetime import timedelta
    from django.utils import timezone
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - \
        timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)
    results = modelname.objects.filter(photo_date__gte=monday_of_this_week)
    return results


###################################################################################################
###################################################################################################

@cache_page(60 * 15)
def query_yesterday(modelname):
    from datetime import timedelta
    from django.utils import timezone
    yesterday = timezone.now().date() - timedelta(days=1)
    monday_of_last_week = yesterday - \
        timedelta(days=(yesterday.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)
    results = modelname.objects.filter(photo_date__gte=yesterday)
    return results


###################################################################################################
###################################################################################################
# begin rendering funx #
##################### Paginator ###########################
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def yesterday_fashion_selects(request):
    results = query_yesterday(PushPhotoselects)
    results = results.filter(file_path__contains="eFashion")
    images = results
    paginator = Paginator(results, 27) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    return render(request, 'image/image_results.html', {'results': results, 'images': images, })


###################################################################################################
###################################################################################################

def yesterday_still_selects(request):
    results = query_yesterday(PushPhotoselects)
    results = results.filter(file_path__contains="aPhoto")
    images = results
    paginator = Paginator(results, 27) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    return render(request, 'image/image_results.html', {'results': results, 'images': images, })


###################################################################################################
###################################################################################################

@cache_page(60 * 15)
def yesterday_fashion_outtakes(request):
    results = query_yesterday(ProductionRawZimages)
    results = results.filter(file_path__icontains="CR2")
    images = results
    paginator = Paginator(results, 27) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    return render(request, 'image/image_results.html', {'results': results, 'images': images, })


###################################################################################################
###################################################################################################
# Weekly Browse Views -- Top Navi Dropdown
def weeks_fashion_outtakes(request):
    results = query_current_week(ProductionRawZimages)
    results = results.filter(file_path__icontains="CR2")
    images = results
    paginator = Paginator(results, 27) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    return render(request, 'image/image_results.html', {'results': results, 'images': images, })

###################################################################################################
###################################################################################################

@cache_page(60 * 15)
def lastweeks_fashion_outtakes(request):
    results = query_previous_week(ProductionRawZimages)
    results = results.filter(file_path__contains="CR2")
    images = results
    paginator = Paginator(results, 27) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    #return render(request, 'listing/image_list_page.html', {'results': results, 'images': images,})
    return render(request, 'image/image_results.html', {'results': results, 'images': images})

###################################################################################################
###################################################################################################

@cache_page(60 * 15)
def weeks_still_selects(request):
    results = query_current_week(PushPhotoselects)
    results = results.filter(file_path__contains="aPhoto")
    images = results
    paginator = Paginator(results, 27) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    return render(request, 'image/image_results.html', {'results': results, 'images': images,})

###################################################################################################
###################################################################################################

def weeks_fashion_selects(request):
    results = query_current_week(PushPhotoselects)
    results = results.filter(file_path__contains="eFashion")
    images = results
    paginator = Paginator(results, 27) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    return render(request, 'image/image_results.html', {'results': results, 'images': images,})

###################################################################################################
###################################################################################################

@cache_page(60 * 15)
def lastweeks_still_selects(request):
    results = query_previous_week(PostReadyOriginal)
    results = results.filter(file_path__contains="Still")
    images = results
    paginator = Paginator(results, 27) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    #return render(request, 'listing/image_list_page.html', {'results': results, 'images': images,})
    return render(request, 'image/image_results.html', {'results': results, 'images': images})


###################################################################################################
###################################################################################################

@cache_page(60 * 15)
def lastweeks_fashion_selects(request):
    results = query_previous_week(PostReadyOriginal)
    results = results.filter(file_path__contains="Fashion")
    images = results
    paginator = Paginator(results, 27) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)
    return render(request, 'image/image_results.html', {'results': results, 'images': images, })


    #return render(request, 'listing/image_list_page.html', {'results': results, 'images': images, })


###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################
# Single Image View  #####
def image(request, pk):
    """Image page."""
    return render_to_response("image/image_single.html", dict(image=Zimages1Photoselects.objects.get(pk=pk),
                                                          user=request.user,
                                                          backurl=request.META["HTTP_REFERER"],
                                                          media_url=MEDIA_URL),)



###################################################################################################
###################################################################################################

from searcher.forms import ImportCropUploadForm


def email_image_and_notes(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = MetadataForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #image_id = pk
            #file_path = form.cleaned_data['file_path']
            #select = form.cleaned_data['select']
            #selectnotes = form.cleaned_data['selectnotes']
            #retouchnotes = form.cleaned_data['retouchnotes']

            #stylenotes = form.cleaned_data['stylenotes']
            #modelnotes = form.cleaned_data['modelnotes']
            #editorialnotes = form.cleaned_data['editorialnotes']

            #keywords = form.cleaned_data['keywords']
            #emailnow = form.cleaned_data['emailnow']

            #if emailnow:
            #    sender = form.cleaned_data['sender']
            #    subject = form.cleaned_data['file_path'].split('/')[-10]
            #    message = form.cleaned_data['message']
            #    recipients = ['editorialnotes@bluefly.com']
            #    recipients.append(sender)

            #from django.core.mail import send_mail
            #send_mail(subject, message, sender, recipients)
            ## TODO: Save form data to database www_django.metadata
            return HttpResponseRedirect('/datasaved/') # Redirect after POST
    else:
        form = MetadataForm() # An unbound form
    return render(request, 'edit_metadata.html', {
        'form': form,
    })


###################################################################################################
###################################################################################################
#####
#import searcher.forms
from searcher.forms import UploadAssetForm

def upload(request):
    form = UploadAssetForm(request.POST, request.FILES)
    if not form.is_valid():
        print 'Return some error'
        pass

######################################################################################################
######################################################################################################

# def manage_metadata(request, image_id):
#     image = Image.objects.get(pk=image_id)
#     MetadataInlineFormSet = inlineformset_factory(image, metadata)
#     if request.method == "POST":
#         formset = MetadataInlineFormSet(request.POST, request.FILES, instance=image)
#         if formset.is_valid():
#             formset.save()
#             ##TODO: Add function to process form data and embed in image as well as update DB table
#             return HttpResponseRedirect(image.get_absolute_url())
#     else:
#         formset = MetadataInlineFormSet(instance=image)
#     return render_to_response("manage_metadata.html", {
#         "formset": formset,
#     })


###################################################################################################
###################################################################################################
################## Manage Image URLs Formset
from searcher.models import LocalImageURL, Product, Brand
from searcher.forms import modelformset_factory

def manage_local_image_urls(request):
    LocalImageURLFormSet = modelformset_factory(LocalImageURL)
    if request.method == "POST":
        formset = LocalImageURLFormSet(request.POST, request.FILES,)
                                ## queryset=LocalImageURL.objects.filter(name__startswith='O'))
        if formset.is_valid():
            formset.save()
            # Do something.
    else:
        formset = LocalImageURLFormSet(queryset=LocalImageURL.objects.all())
    return render_to_response("manage/manage_local_image_urls.html", {
        "formset": formset,
    })


###################################################################################################
###################################################################################################
################## Manage Product Formset
from djdam.settings import MEDIA_ROOT
from django.forms.models import inlineformset_factory
#ProductInlineFormSet = inlineformset_factory(Brand, Product)
def get_absolute_url(request):
    if request.method == "POST":
        return "/{0}/{1}/".format(MEDIA_ROOT, request.file_path)

###################################################

def manage_products(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    ProductInlineFormSet = inlineformset_factory(Brand, Product)
    if request.method == "POST":
        formset = ProductInlineFormSet(request.POST, request.FILES, instance=brand)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(brand.get_absolute_url())
    else:
        formset = ProductInlineFormSet(instance=brand)
    return render_to_response("manage/manage_products.html", {
        "formset": formset,
    })


###################################################################################################
###################################################################################################

from django.shortcuts import redirect
from django.core.mail import mail_admins
from forms import ImageNotesForm


def imagenotes_form(request):
    if request.POST:
        form = ImageNotesForm(request.POST)
        if form.is_valid():
            message = "From: {0} <{1}>\r\nSubject:{2}\t{3}\r\nMessage:\r\n{4}\r\n".format(
                form.cleaned_data['name'],
                form.cleaned_data['email'],
                form.cleaned_data['colorstyle'],
                form.cleaned_data['subject'],
                form.cleaned_data['message']
            )

            mail_admins('ImageNotes Form', message, fail_silently=False)
            if request.is_ajax():
                return render(request, 'base/success.html')
            else:
                return redirect('imagenotes_success')
    else:
        form = ImageNotesForm()

    return render(request, 'forms/imagenotes_form.html', {'form':form})


###################################################################################################
###################################################################################################
## Hires Primary images

from django.views.generic.dates import YearArchiveView, MonthArchiveView, WeekArchiveView, DayArchiveView
from searcher.models import Zimages1Photoselects

class PhotoYearArchiveView(YearArchiveView):
    queryset = PostReadyOriginal.objects.all()
    date_field = "photo_date"
    make_object_list = True
    allow_future = True

###################################################

class PhotoMonthArchiveView(MonthArchiveView):
    queryset = PostReadyOriginal.objects.all()
    date_field = "photo_date"
    make_object_list = True
    allow_future = True

###################################################

class PhotoWeekArchiveView(WeekArchiveView):
    queryset = PostReadyOriginal.objects.all()
    date_field = "photo_date"
    make_object_list = True
    week_format = "%W"
    allow_future = True

###################################################

class PhotoDayArchiveView(DayArchiveView):
    queryset = PostReadyOriginal.objects.all()
    date_field = "photo_date"
    make_object_list = True
    allow_future = True

###################################################################################################
###################################################################################################
############ RAW Onfig Outtakes

class PhotoRawYearArchiveView(YearArchiveView):
    queryset = ProductionRawZimages.objects.all()
    date_field = "photo_date"
    make_object_list = True
    allow_future = True

###################################################

class PhotoRawMonthArchiveView(MonthArchiveView):
    queryset = ProductionRawZimages.objects.all()
    date_field = "photo_date"
    make_object_list = True
    allow_future = True

###################################################

class PhotoRawWeekArchiveView(WeekArchiveView):
    queryset = ProductionRawZimages.objects.all()
    date_field = "photo_date"
    make_object_list = True
    week_format = "%W"
    allow_future = True

###################################################

class PhotoRawDayArchiveView(DayArchiveView):
    queryset = ProductionRawZimages.objects.all()
    date_field = "photo_date"
    make_object_list = True
    allow_future = True


###################################################################################################
###################################################################################################
###################################
#### Images
# from searcher.models import Images, ProductSnapshotLive

def merge_dicts_bycolorstyle(dict1, dict2):
    from collections import defaultdict
    resultsdata = defaultdict(dict)
    for group in (dict1, dict2):
        for fields in group:
            resultsdata[fields['colorstyle']].update(fields)
    return resultsdata


###################################################################################################
###################################################################################################

@cache_page(60 * 15)
def get_all_images_colorstyle(request):
    from searcher.models import Images
    from searcher.models import ProductionRawZimages
    from searcher.models import ProductSnapshotLive as PmData
    import datetime
    results             = ''
    images              = ''
    colorstyle          = ''
    brand               = ''
    photo_date          = ''
    outtakes            = False
    styledata           = ''
    found_style_data    = {}
    colorstyles         = []
    selects_found       = ''
    selects_all         = Images.image_select.get_query_set()



    if request.POST['searchquery']:
        import re

        regex_outtakes      =   re.compile(r'^.*?out$', re.I)
        regex_event         =   re.compile(r'^EV.+?\d{4}$', re.I)
        regex_style         =   re.compile(r'^\d{5,9}$')
        regex_date          =   re.compile(r'^\d{1,2}\W?\d{2}$')
        regex_datefull      =   re.compile(r'^\d{4}-\d{2}-\d{2}$')
        regex_datefullrev   =   re.compile(r'^\d{2}-\d{2}-\d{4}$')
        regex_datemo        =   re.compile(r'^[a-z]{3}\s?\d{2}$', re.I)
        regex_daterange     =   re.compile(r'^\d{4}\b\s\d{4}$')
        regex_multistyle    =   re.compile(r'^\d{9}\W\d{9}.+?')
        regex_brand         =   re.compile(r'^.{3}.*?\W*?.*?$', re.L)
        retest              =   ''
        retest              =   request.POST['searchquery']

        ## retest list regextypes = ['Jun 12', 'Gucci', 'may 17', '09-13', '0115', 'sep13', '302991', '333092101', '1012 1015', '7/21', '02/21', 'Event 3029', 'Tse', 'pucci', '525 america', '12', '333103 902303101', '10 strawberry st.', '7 for All Mankind', '320293102 320302301 320293102 320302301', 'ysl', 'BCBG', 'seventy7', 'Wil33', '720293102,720302301,290293102,420302301', 'Salvatore Ferregammo', 'new york', 'seven for all mankind']        #def testregex(retest):
        if re.findall(regex_style, retest):
            colorstyle = retest

        elif re.findall(regex_event, retest):
            eventid = retest

        elif re.findall(regex_outtakes, retest):
           #print 'colorstyle Found{0}'.format(retest)
           #selects_all = Images.image_outtake.get_query_set()
           selects_all = ProductionRawZimages.objects.get_query_set()
           colorstyle = retest

        elif re.findall(regex_date, retest):
            if len(retest) == 3:
                retest = "0{}".format(retest)
            if int(str(datetime.date.today())[5:7]) <= 02:
                yr = int(str(datetime.date.today())[:4])
                reformated = "{0}-{1}-{2}".format(str(yr),retest[:2],retest[2:])
            else:
                yr = int(str(datetime.date.today())[:4])
                yr = yr - 1
                reformated = "{0}-{1}-{2}".format(yr, retest[:2], retest[2:])

            photo_date = reformated

        elif re.findall(regex_datemo, retest):
            photo_date = retest

        elif re.findall(regex_datefull, retest):
            photo_date = retest

        elif re.findall(regex_daterange, retest):
            startend_date = retest

        elif re.findall(regex_multistyle, retest):
            multistyles = retest

        elif re.findall(regex_brand, retest):
            brand = retest


    try:
        if colorstyle:
            query           = colorstyle
            selects_found   = selects_all.filter(colorstyle__icontains=query)
            try:
                styledata = PmData.objects.get(colorstyle__icontains=query)
                print "success{0}".format(colorstyle)
            except:
                print "failed{0}".format(colorstyle)

        elif photo_date:
            querytmp           = photo_date
            ## Create datetime obj from post str formatted variable
            query           = datetime.datetime.strptime(querytmp, '%Y-%m-%d').date()
            selects_found   =  selects_all.filter(photo_date=query)

            colorstyles = []
            for style in selects_found.values_list('colorstyle', flat=True):
                colorstyles.append(style)
            colorstyles = sorted(set(colorstyles))
            styledata = PmData.objects.get_query_set(colorstyle__in=colorstyles)
            #found_style_data = {}
            #for found in selects_found.values():
            #    datatmp = PmData.objects.get(colorstyle__icontains=found['colorstyle'])
            #    found_style_data['colorstyle'] = found['colorstyle']
            #    found_style_data['styledata'] = datatmp

            try:
                styledata       = PmData.objects.get(colorstyle__icontains=colorstyle)
                print "success{0}".format(photo_date)
            except OSError:
                print "failed{0}".format(photo_date)
    except:
        print "failed{0}".format(request)

    #try:
    #    if request.POST['outtakes']:
    #        outtakes_all = Images.image_outtake.get_query_set()
    #        outtakes_found = outtakes_all.filter(colorstyle__icontains=query)
    #        #selectspush_all = Images.image_select_push.get_query_set()
    #        #selectsthumb_all = Images.image_select_thumb.get_query_set()
    #        from itertools import chain
    #        results = list(chain(outtakes_found, selects_found,))
    #        #results = sorted(
    #        #    chain(outtakes_all, selects_all,),
    #        #    key=lambda instance: instance.photo_date)
    #    else:
    #        results = selects_found
    #except KeyError:
    #    #results = selects_found
    #    pass

    try:
        if brand:
            #query = brand
            styledata = PmData.objects.filter(brand__icontains=brand).values_list('colorstyle',
                                                                                  'po_number',
                                                                                  'vendor_style',
                                                                                  'brand',
                                                                                  'product_type',
                                                                                  'product_subtype',
                                                                                  'color', )
            colorstyles = []
            for style in styledata.values_list('colorstyle', flat=True):
                colorstyles.append(style)
            colorstyles = sorted(set(colorstyles))
            selects_found = selects_all.filter(colorstyle__in=colorstyles)

            #found_style_data = {}
            #for found in selects_found.values():
            #    datatmp = PmData.objects.get(colorstyle__icontains=found['colorstyle'])
            #    found_style_data['colorstyle'] = found['colorstyle']
            #    found_style_data['styledata'] = datatmp
            #    #results =
            #print "brandif data loop"

    except OSError:
        print "failed on Brand"

        ## If cant get specific style's data, get it all
    if not styledata:
        try:
            styledata = found_style_data.items()
        except:
            styledata = PmData.objects.all()

    if not results:
        try:
            results = selects_found
        except KeyError:
            results = selects_found

    images  = results
    return render(request, 'image/image_results.html', {'results': results, 'images': images, 'styledata': styledata, })

###################################################################################################
###################################################################################################
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def get_all_images_outtakes(request):
    from searcher.models import ProductionRawZimages
    from searcher.models import ProductSnapshotLive
    PmData = ProductSnapshotLive.objects.all()
    import datetime
    results             = ''
    images              = ''
    colorstyle          = ''
    brand               = ''
    photo_date          = ''
    outtakes            = False
    styledata           = ''
    found_style_data    = {}
    colorstyles         = []
    selects_found       = ''
    #selects_all         = Images.image_select.get_query_set()
    selects_all = ProductionRawZimages.objects.distinct()

    if request.POST['searchquery']:
        import re

        regex_outtakes      =   re.compile(r'^.*?out$', re.I)
        regex_event         =   re.compile(r'^EV.+?\d{4}$', re.I)
        regex_style         =   re.compile(r'^\d{5,9}$')
        regex_date          =   re.compile(r'^\d{1,2}\W?\d{2}$')
        regex_datefull      =   re.compile(r'^\d{4}-\d{2}-\d{2}$')
        regex_datefullrev   =   re.compile(r'^\d{2}-\d{2}-\d{4}$')
        regex_datefullrevSL =   re.compile(r'^\d{2}/\d{2}/\d{4}$')
        regex_datemo        =   re.compile(r'^[a-z]{3}\s?\d{2}$', re.I)
        regex_daterange     =   re.compile(r'^\d{4}\b\s\d{4}$')
        regex_multistyle    =   re.compile(r'^\d{9}\W\d{9}.+?')
        regex_brand         =   re.compile(r'^.{3}.*?\W*?.*?$', re.L)
        retest              = ''
        retest              =   request.POST['searchquery'] #[:9]

        ## retest list regextypes = ['Jun 12', 'Gucci', 'may 17', '09-13', '0115', 'sep13', '302991', '333092101', '1012 1015', '7/21', '02/21', 'Event 3029', 'Tse', 'pucci', '525 america', '12', '333103 902303101', '10 strawberry st.', '7 for All Mankind', '320293102 320302301 320293102 320302301', 'ysl', 'BCBG', 'seventy7', 'Wil33', '720293102,720302301,290293102,420302301', 'Salvatore Ferregammo', 'new york', 'seven for all mankind']        #def testregex(retest):
        if re.findall(regex_style, retest):
            colorstyle = retest

        elif re.findall(regex_event, retest):
            eventid = retest

        elif re.findall(regex_outtakes, retest):
           #print 'colorstyle Found{0}'.format(retest)
           #selects_all = Images.image_outtake.get_query_set()
           #selects_all = ProductionRawZimages.objects.get_query_set()
           colorstyle = retest

        elif re.findall(regex_datefull, retest):
            if len(retest) == 3:
                retest = "0{}".format(retest)
            if int(str(datetime.date.today())[5:7]) <= 02:
                yr = int(str(datetime.date.today())[:4])
                reformated = "{0}-{1}-{2}".format(str(yr),retest[:2],retest[2:])
            else:
                yr = int(str(datetime.date.today())[:4])
                yr = yr - 1
                reformated = "{0}-{1}-{2}".format(yr,retest[:2], retest[2:])

            photo_date = reformated


        elif re.findall(regex_datemo, retest):
            photo_date = retest

        elif re.findall(regex_datefull, retest):
            photo_date = retest

        elif re.findall(regex_datefullrevSL, retest):
            photo_date = "{0}-{1}-{2}".format(retest[6:],retest[:2], retest[3:5])

        elif re.findall(regex_daterange, retest):
            startend_date = retest

        elif re.findall(regex_multistyle, retest):
            multistyles = retest

        elif re.findall(regex_brand, retest):
            brand = retest

##TODO Match PM data with images to fill brand, po etc in output tables

#    try:
    if colorstyle:
        query           = colorstyle
        selects_found   = selects_all.filter(colorstyle__icontains=query)
        try:
            styledata = PmData.get(colorstyle__icontains=query)
            print "success{0}".format(colorstyle)
        except:
            print "failed{0}".format(colorstyle)

    elif photo_date:
        querytmp           = photo_date
        ## Create datetime obj from post str formatted variable
        query           = datetime.datetime.strptime(querytmp, '%Y-%m-%d').date()
        selects_found   =  selects_all.filter(photo_date=query)

        ## TODO Match/Join Onfigure calendar and capture 1 data tables for output and search by model
        colorstyles = []
        #styledata = {}
        for style in selects_found.values_list('colorstyle', flat=True):
            colorstyles.append(style)
            #colorstyles = sorted(set(colorstyles))

            #i = PmData.get(colorstyle__icontains=style).values()
            #styledata[style] = i
        styledata=PmData.all().filter(colorstyle__in=[colorstyles])

        from itertools import chain
        results_list = list(chain(selects_found, styledata))
        #result_list = sorted(
        #    chain(page_list, article_list, post_list),
        #          key=lambda instance: instance.date_created)
        #c=colorstyles.pop().values()[0]['colorstyle']
        # styledata = {}
        # from collections import defaultdict
        # d = defaultdict(list)
        # for colorstyle in colorstyles:
        #     styledata[colorstyle] = PmData.filter(colorstyle__in=colorstyle)
        #     d[colorstyle] = PmData.filter(colorstyle__icontains=colorstyle)
        # # #found_style_data = {}

        # jl=[v[0] for f,v in d.iteritems()][:]

        #colorstyles = sorted(set(colorstyles))
        #styledata = PmData.objects.all()
        #styledata = []
        #for colorstyle in colorstyles:
        #    styledata.append(PmData.objects.get(colorstyle__icontains=style))
        #found_style_data = {}
        #for found in selects_found.values():
        #    datatmp = PmData.objects.get(colorstyle__icontains=found['colorstyle'])
        #    found_style_data['colorstyle'] = found['colorstyle']
        #    found_style_data['styledata'] = datatmp

        # try:
        #     styledata       = PmData.objects.get(colorstyle__icontains=colorstyle)
        #     print "success{0}".format(photo_date)
        # except OSError:
        #     print "failed{0}".format(photo_date)


    images  = selects_found
    results = results_list
    return render(request, 'image/image_results.html', {'results': results, 'images': images, 'styledata': styledata, 'query': query })

###################################################################################################
###################################################################################################

from django.shortcuts import render
from forms import MetadataForm

def imagenotes_add(request, pkey=''):
    # This view is missing all form handling logic for simplicity of the example
    return render(request, 'forms/imagenotes_form.html',)

###################################################################################################
###################################################################################################

def index(request):
    # This view is missing all form handling logic for simplicity of the example
    return render(request, 'index.html', {'form': MetadataForm()})

###################################################################################################
###################################################################################################

def metadata_edit_file(request, pkey=None):
    from forms import MetadataForm
    image = request.POST['file_path']
    if pkey:
        pass
    else:
        pkey = request.POST['imagepk']
    #colorstyle = request.GET['colorstyle']
    # This view is missing all form handling logic for simplicity of the example
    return render(request,  'image/image_metadata_edit.html',
                  {'form': MetadataForm(), 'image': image})

###################################################################################################
###################################################################################################

## Generic List view of All "Model"'s objects
from searcher.models import SelectedFiles as SelectedFiles
def selected_file_list(request,SelectedFiles):
    #user_name = request.POST['user_id']
    #original_file_path = request.POST['file_path']
    obj_list = SelectedFiles.objects.all()
    template_name = 'searcher/listing/{0}_list.html'.format(SelectedFiles.__name__.lower())
    return render(request, template_name, {'object_list': obj_list})


###################################################################################################
###################################################################################################

## Define Upload Func
from django.template.defaultfilters import slugify

def upload_to(path, attribute):
    def upload_callback(instance, filename):
        return '{0}{1}/{2}'.format(path, unicode(slugify(getattr(instance, attribute))), filename)
    return upload_callback

###################################################################################################
###################################################################################################

def mark_selected(request):
    import datetime
    imagepk     = request.POST['imagepk']
    file_path   = request.POST['file_path']
    #user_id     = request.HTTP_COOKIE['_auth_user_id']
    ipaddress   = request.META['REMOTE_ADDR']
    create_dt   = datetime.date.today()
    colorstyle  = ''
    try:
        session_id  = request.COOKIES['sessionid']
    except KeyError():
        session_id  = 'Guest'
        ## TODO:  either create a session store for selections or/and add the pk and filepath to the mark-select table

    sf = SelectedFiles(source_pk=imagepk,
                       file_path = file_path,
                       ipaddress = ipaddress,
                       session_id = session_id,
                       create_dt = create_dt,)
                       #colorstyle = models.CharField(max_length=255)
    try:
        sf.save()
    except:
        print "Duplicate Entry {0}".format(sf,)
    #    except sqlalchemy.exc.DatabaseError:


    user_index = SelectedFiles.objects.filter(ipaddress__exact=ipaddress) ##.filter(create_dt__gt=create_dt - timedelta(days=7))
    return render(request, 'base/success.html',
                          {'form': MetadataForm(),
                           'imagepk': imagepk,
                           'image': sf,
                           'user_index': user_index})

###################################################################################################
###################################################################################################

def mark_removed(request):
    import datetime
    imagepk     = request.POST['imagepk']
    file_path   = request.POST['file_path']
    #user_id     = request.HTTP_COOKIE['_auth_user_id']
    ipaddress   = request.META['REMOTE_ADDR']
    create_dt   = datetime.date.today()
    colorstyle  = ''
    try:
        session_id  = request.COOKIES['sessionid']
    except KeyError():
        session_id  = 'Guest'

    ## TODO:  either create a session store for selections or/and add the pk and filepath to the mark-select table
    sf = SelectedFiles(source_pk=imagepk,
                       file_path = file_path,
                       ipaddress = ipaddress,
                       session_id = session_id,
                       create_dt = create_dt,)
                       #colorstyle = models.CharField(max_length=255)
    try:
        sf.delete()
    except:
        print "Duplicate Entry {0}".format(sf,)
    #    except sqlalchemy.exc.DatabaseError:


    #from datetime import timedelta as timedelta

    user_index = SelectedFiles.objects.filter(ipaddress__exact=ipaddress) ##.filter(create_dt__gt=create_dt - timedelta(days=7))
    return render(request, 'base/success.html',
                          {'form': MetadataForm(),
                           'imagepk': imagepk,
                           'image': 'Deleted',
                           'user_index': user_index})


###################################################################################################
###################################################################################################

def selected_index(request):
    #user_id     = request.HTTP_COOKIE['_auth_user_id']
    ipaddress = request.META['REMOTE_ADDR']
    #session_id = request.COOKIES['sessionid']
    #create_dt = datetime.date.today()

    user_index = SelectedFiles.objects.filter(
        ipaddress__exact=ipaddress) ##.filter(create_dt__gt=create_dt - timedelta(days=7))
    return render(request, 'base/success.html',
                  {'user_index': user_index})



###################################################################################################
###################################################################################################

import os
from cStringIO import StringIO  # caveats for Python 3.0 apply

##TODO Make function to download selected files as a zip directly from browser and option to email zip
def somezip(request):
    file = StringIO()
    zf = zipfile.ZipFile(file, mode='w', compression=zipfile.ZIP_DEFLATED)
    for fn in os.listdir("/tmp"):
        path = os.path.join("/tmp", fn)
        if os.path.isfile(path):
            try:
                zf.write(path)
            except IOError:
                pass
    zf.close()
    response = HttpResponse(file.getvalue(), mimetype="application/zip")
    response['Content-Disposition'] = 'attachment; filename=yourfiles.zip'
    return response

###################################################################################################
###################################################################################################

def upload_import_crop(request):
    form = ImportCropUploadForm(request.POST, request.FILES)
    file_path=request.FILES['filepath']
    if not form.is_valid():
        print "Form Not Valid"
        # Return some error
        pass

    return render(request, 'base/success.html', {'form': ImportCropUploadForm(), 'image': image})


def upload_crop_preview(request):
    ## TODO:  Script will accept file in POST and display previews of crops and formats based on dropdown list of pre defined magick scripts
    #user_name = request.POST['user_id']
    #original_file_path = request.POST['file_path']
    image = request.POST['file_path']
    return render(request, 'base/success.html', {'form': MetadataForm(), 'image': image})

###################################################################################################

def upload_and_crop(request):
    ## TODO:  Script will accept file in POST and upload to image drop location which will be separate directories performing only certain functions, maybe
    #user_name = request.POST['user_id']
    #original_file_path = request.POST['file_path']
    image = request.POST['file_path']
    return render(request, 'base/success.html', {'form': MetadataForm(), 'image': image})

###################################################################################################
###################################################################################################
#from searcher.forms import UploadFileForm


def handle_uploaded_excel_file(workbk=None):
    import xlrd
    #workbk = sys.argv[1]
    book = xlrd.open_workbook(workbk)##sys.argv[1])
    sh = book.sheet_by_index(0)

    #convWriter = csv.writer(sys.stdout,delimiter=',', dialect='excel')

    numcols=sh.ncols
    outdict = {}
    for rx in xrange(sh.nrows):
        rowdict = {}
        for cx in xrange(sh.ncols):
            rowhead = sh.cell_value(rowx=0,colx=cx)
            rowval = sh.cell_value(rowx=rx,colx=cx)
            rowdict[rowhead] = rowval
            outdict[rx] = rowdict
    return outdict


def compile_outdict_by_rowkeys(outdict):
    from collections import defaultdict
    d = defaultdict(list)
    for r in outdict.items():
        dd = defaultdict(dict)
        for val in r[1].items():
            try:
                if type(val[1]) == float:
                    value = int(val[1])#"{0:.0}".format(val[1])
                    print value
                else:
                    value = val[1]
                #print type(val[1])
                #print r[0],val[0],value
                dd[val[0]]=value
                d[r[0]] = dd
                #print dd
                #csv_write_datedOutfile(lines.encode('ascii', 'replace'))
            except AttributeError:
                pass
    return d


def handle_uploaded_text_file(f):
    with open('output.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

#from django import forms
from xlrd import *
from xlwt import *
from django.http import HttpResponse


def input_merge_list(request):
    form = UploadFileForm(request.POST, request.FILES)
    file_path   = request.FILES['file']
    input_list =  request.POST['input_list']
    if not form.is_valid():
        print 'Form Not Valid'
        # Return some error
        pass

    inputdata = file_path
    wb = Workbook()
    ws0 = wb.add_sheet('0')

    for rx in xrange(20):
        for cx in xrange(20):
            # writing to a specific x,y
            ws0.write(rx, cx, "this is cell %s, %s" % (rx, cx))

        wb.save('output.xls')

    return render(request, 'excel/input_query_list.html', {'form': UploadFileForm(),
                                                           'input_list': input_list ,
                                                           'file_path': file_path})

def import_excel_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_excel_file(request.FILES['file_path'])
            with open('output.xls', 'rbU+') as f:
                outdict = handle_uploaded_excel_file(workbk=f.path.read())
                final = compile_outdict_by_rowkeys(outdict)
            return HttpResponseRedirect('output.xls')
    else:
        form = UploadFileForm()
    return render(request, 'excel/return_download_file.html', {'form': form})

#from forms import ImportStylesMergeForm
def download_merge_file(request):
    #return render(request, 'excel/return_download_file.html', {'form': UploadMergeList(), 'file_path': file_path})
    return HttpResponse(open('output.xls','rbU').read(), mimetype='application/vnd.ms-excel')


from utilities import ExcelResponse


def output_excel_table(request):
    oldpo = 'm'
    objs = ExcelToolData.objects.all()
    return ExcelResponse(objs)

def output_excel_table2(request):
   wb = Workbook()
   ws0 = wb.add_sheet('0')
   for rx in xrange(20):
      for cx in xrange(20):
         # writing to a specific x,y
         ws0.write(rx,cx,"this is cell %s, %s" % (rx,cx))
      wb.save('output.xls')
   return HttpResponse(open('output.xls','rbU').read(), mimetype='application/vnd.ms-excel')

def export_excel_file(request, queryset):
    import xlwt
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=output.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("load_to_tool")

    row_num = 0

    columns = [
        (u"id", 2000),
        (u"colorstyle", 6000),
        (u"vendor_style", 8000),
        (u"po_number", 8000),
        (u"material", 8000),
        (u"bullet_1", 8000),
        (u"bullet_2", 8000),
        (u"bullet_3", 8000),
        (u"bullet_4", 8000),
        (u"bullet_5", 8000),
        (u"bullet_6", 8000),
        (u"bullet_7", 8000),
        (u"bullet_8", 8000),
        (u"bullet_9", 8000),
        (u"short_name", 8000),
        (u"long_description", 8000),
        (u"country_origin", 8000),
        (u"return_policy_id", 8000),
        (u"copy_ready_dt", 8000),
        (u"care_instructions_id", 8000),
        (u"color_group_id", 8000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in queryset:
        row_num += 1
        row = [
            obj.pk,
            obj.colorstyle,
            obj.vendor_style,
            obj.po_number,
            obj.material,
            obj.bullet_1,
            obj.bullet_2,
            obj.bullet_3,
            obj.bullet_4,
            obj.bullet_5,
            obj.bullet_6,
            obj.bullet_7,
            obj.bullet_8,
            obj.bullet_9,
            obj.short_name,
            obj.long_description,
            obj.country_origin,
            obj.return_policy_id,
            obj.copy_ready_dt,
            obj.care_instructions_id,
            obj.color_group_id,
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

# views.py
# @render_to_json
# def upload_image( request, image=None ):
#     if request.method == 'POST':
#         form = forms.UploadMergeList( request.POST, files=request.FILES,instance=file )
#         if form.is_valid():
#             file = form.save()
#             if request.is_ajax():
#                 return [{
#                     "name": os.path.basename(image.file.name),
#                     "size": form.cleaned_data['file'].size,
#                     "type": image.content_type,
#                 }]
#             else:
#                 messages.success( request, _("UploadedImage Uploaded"))
#         else:
#             if request.is_ajax():
#                 return [{
#                     'error': dict([
#                         (k,unicode(v))
#                         for (k,v) in form.errors.items()
#
#                     ]),
#                 }]
#             else:
#                 messages.error( request, _("There was an error uploading your image: %(error)s")%{
#                     'error':unicode(form.errors.items())
#                 })
#     return HttpResponseRedirect(reverse('content'))

###################################################################################################
###############################   UploadFileWithForm   ############################################
###################################################################################################

from .forms import UploadFileForm
from .models import File

# Imaginary function to handle an uploaded file.
from .forms import handle_uploaded_excel_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_excel_file(request.FILES['file_path'])
            #return HttpResponseRedirect('output.xls')
            return HttpResponseRedirect(reverse('searcher.views.upload_file'))
    else:
        form = UploadFileForm()
    #return render_to_response('searcher/return_download_file.html', {'form': form})
    #return render_to_response('excel/return_download_file.html', {'form': form})
        # Load documents for the list page
        files = File.objects.all()

        return render_to_response('excel/return_download_file.html',
            {'files': files,
             'form': form},
            context_instance=RequestContext(request)
        )


###################################################################################################
############################### UploadDocumentWithForm ############################################
###################################################################################################

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def ajax_return_search(request):
    try:
        q = request.POST['input_list']
    except:
        q = request.GET['input_list']
    results = ProductSnapshotLive.objects.get(colorstyle__icontains=q)
    return render_to_response('ajax/search_form.html', {'results': results, 'q':q}, context_instance=RequestContext(request))


def ajax_colorstyle_search(request,q=None,sq=None):
    if not q and not sq:
        try:
            q = request.POST['colorstyle']
            if len(q) > 15:
                q = q.split(',')[:]
            else:
                sq = q

        except:
            q = request.GET['colorstyle']
            if len(q) > 15:
                q = q.split(',')[:]
            else:
                sq = q

    results = {}
    if sq:
        snapshot = ProductSnapshotLive.objects.get(colorstyle__icontains=q)
        results[q] = snapshot
        return render_to_response('ajax/search_form.html',
                                {'results': results, 'q':q},
                                context_instance=RequestContext(request))
    else:
        from collections import defaultdict
        results = defaultdict(list)
        styles = []
        styles = [ styles.append(style) for style in styles if len(style) < 10 and style.isdigit() ]
        snapshot = ProductSnapshotLive.objects.get(colorstyle__in=styles)
        for row in snapshot.iteritems():
            for style in styles:
                if style == row.get('colorstyle'):
                    results[style].append(row)
        return render_to_response('ajax/search_form.html',
                                {'results': results, 'q':styles},
                                context_instance=RequestContext(request))

# def list(request):
#     # Handle file upload
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             newdoc = Document(docfile = request.FILES['docfile'])
#             newdoc.save()

#             # Redirect to the document list after POST
#             return HttpResponseRedirect(reverse('searcher.views.list'))
#     else:
#         form = DocumentForm() # A empty, unbound form

#     # Load documents for the list page
#     documents = Document.objects.all()

#     # Render list page with the documents and the form
#     return render_to_response(
#         'excel/list.html',
#         {'documents': documents, 'form': form},
#         context_instance=RequestContext(request)
#     )

