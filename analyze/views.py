from django.shortcuts import render, redirect
from .forms import *
import pandas as pd
import xlrd
import csv
import numpy as np
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
import os
from .models import *
from itertools import zip_longest
from xlrd import XLRDError

"""
ADD TO REVIEW LIST GLOBAL FUNCITON
"""
def add_to_review(request, slug):
    if request.user.is_superuser:
        aFile  = File.objects.get(slug=slug)
        reviewlist = ReviewList.objects.get(id=1)
        if not aFile in reviewlist.fileInstance.all():
            reviewlist.fileInstance.add(aFile)
        return redirect("analyze:superuser_den")
    else:
        return redirect("analyze:myfiles")

def remove_from_review(request, slug):
    if request.user.is_superuser:
        aFile = File.objects.get(slug=slug)
        review = ReviewList.objects.get(id=1)
        if aFile in review.fileInstance.all():
            review.fileInstance.remove(aFile)
        return redirect("analyze:superuser_den")
    else:
        return redirect("analyze:myfiles")

def review_list(request):
    if request.user.is_superuser:
        allrevs = ReviewList.objects.get(id=1)
        context = {
            'allrevs': allrevs
        }
        return render(request, 'analyze/review_list.html', context)
# home page of the website
def home(request):
    q = request.GET.get('query')
    if q:
        if request.user.is_authenticated and request.user.is_superuser:
            allFiles = File.objects.all().order_by('-uploaded_on')
            files = allFiles.filter(Q(name__icontains=q) | Q(user__username__icontains=q) | Q(id__icontains=q))
            return render(request, 'analyze/search_results.html', {'files': files, 'query':q})

        elif request.user.is_authenticated:
            userobj = User.objects.get(username=request.user)
            allFiles = File.objects.filter(user=userobj).order_by('-uploaded_on')
            files = allFiles.filter(Q(name__icontains=q) | Q(user__username__icontains=q) | Q(id__icontains=q))
            return render(request, 'analyze/search_results.html', {'files': files, 'query':q})
        else:
            return redirect("accounts:login")
    context = {

    }   
    return render(request, 'analyze/index.html', context)

"""
MAIN FUNCTION TO COMPARE EXCEL FILES
"""
# compare two excel files
def compare_excel(file1, file2):
    ex1 = str(file1)[str(file1).index("."):]
    ex2 = str(file2)[str(file2).index("."):]

    if ex1 == ex2:
        if ex1 == '.xls' or ex1 == '.xlsx':
            try:
                rb1 = xlrd.open_workbook(file1)
                rb2 = xlrd.open_workbook(file2)

                sheet1 = rb1.sheet_by_index(0)
                sheet2 = rb2.sheet_by_index(0)
                
                results = []
                for rownum in range(max(sheet1.nrows, sheet2.nrows)):

                    if rownum < sheet1.nrows:
                        try:
                            row_rb1 = sheet1.row_values(rownum)
                            row_rb2 = sheet2.row_values(rownum)
                            
                            for colnum, (c1, c2) in enumerate(zip_longest(row_rb1, row_rb2)):
                                if c1 != c2:
                                    text = ("Row {} Col {} - {} != {}".format(rownum+1, colnum+1, c1, c2))
                                    results.append(text)
                        except:
                            results.append("Error")
                    else:
                        text = ("Row {} missing".format(rownum+1))
                        results.append(text)
                return results
            except XLRDError as e:
                print("Unsupported file format")
        elif ex1 == '.csv' or ex2 == '.csv':
            # compare csv files
            with open(file1, 'r') as t1, open(file2, 'r') as t2:
                fileone = t1.readlines()
                filetwo = t2.readlines()

                for line in filetwo:
                    if line not in filetwo:
                        print(line)
    else:
        print("Can't compare two different files")
        results = ["Can't Compare two different files with different extensions. "]
        return results

"""
CREATE COMPARE GROUPS
"""
def create_compare_group(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = CompareGroupForm(request.POST or None)
            if form.is_valid():
                d = form.save(commit=False)
                d.save()
                return redirect("analyze:comparelist")
        else:
            form = CompareGroupForm()
        return render(request, 'analyze/create-compare.html', {'form': form})
    return redirect("analyze:home")

def comparelist(request):
    if request.user.is_authenticated and request.user.is_superuser:
        comparelists = Compare.objects.all().order_by('-date')
        return render(request, 'analyze/comparelist.html', {'comparelists': comparelists})
    else:
        return redirect("analyze:home")

def get_results(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        testcase = Compare.objects.get(id=id)
        # get two files
        file1 = testcase.file1
        file2 = testcase.file2

        # compare these two files
        results = compare_excel(file1.efile.path, file2.efile.path)
        return render(request, 'analyze/compareResult.html', {'results': results, 'testcase': testcase})
    else:
        return redirect("accounts:login")
# edit comparelist
def edit_compare_list(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        compareobj = Compare.objects.get(id=id)
        if request.method == 'POST':
            form = CompareGroupForm(request.POST, instance=compareobj)
            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                return redirect("analyze:comparelist")
        else:
            form = CompareGroupForm(instance=compareobj)
        return render(request, 'analyze/edit-compare.html', {'form': form, 'compareobj': compareobj})
    else:
        return redirect("analyze:home")
# delete comparelist
def delete_compare_list(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        compareobj = Compare.objects.get(id=id)
        compareobj.delete()
        return redirect("analyze:comparelist")
    else:
        return redirect("analyze:home")
# upload file
"""
THIS FUNCTION HANDLES THE FILE UPLOAD USING THE UPLOADFILEFORM
"""
def upload_file(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                f = form.save(commit=False)
                f.user = request.user
                f.save()
                return redirect("analyze:myfiles")
        else:
            form = UploadFileForm()
        return render(request, 'analyze/upload.html', {'form': form, 'msg': 'Upload'})

"""
THIS IS THE LIST OF ALL THE FILES OF THE LOGGED IN USERS
"""
def my_files(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)

        files = File.objects.filter(user=user).order_by('-uploaded_on')

        context = {
            'files': files
        }
        return render(request, 'analyze/myfiles.html', context)
    else:
        return redirect("accounts:login")
"""
THIS IS A TEST FUNCTION NOT USED.
"""
def csv_from_excel(path):
    wb = xlrd.open_workbook(path)
    sh = wb.sheet_by_name('Sheet1')
    namec = str(path).replace(".xlsx", ".csv")
    print(namec)
    new_path = open(namec, 'w')
    wr = csv.writer(new_path, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    new_path.close()
    return new_path

"""
CHECK THE UPLOADED FILE FOR THE EXTENSION AND RETURN ALL THE DATA FROM THE FILE
THIS FILE IS OPEN TO CHANGE
"""
def read_sheet(filepath, extension):
    if extension == '.xlsx' or extension == '.xls':
        print("reading from xlss")
        # data_xls = pd.read_excel(filepath, 'Sheet1', index_col=None)
        # namec = str(filepath).replace(".xlsx", ".csv")
        # data_xls = data_xls.to_csv(namec, encoding='utf-8', index=False)

        # # print("Reading From xlsx")
        # # df = pd.ExcelFile(filepath)
        # # sheets = df.sheet_names
        # # df1 = df.parse(sheets)
        # # n = df.parse(0)
        # # print(n)
        workbook = xlrd.open_workbook(filepath)
        sheet = workbook.sheet_by_index(0)
 
        data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
        return data, extension
    elif extension == '.csv':
        # df = pd.read_csv(filepath, error_bad_lines=False)
        # data = list(df.columns.values)
        # return data, extension
        with open(filepath, 'r') as csvfile:
            content  = csv.reader(csvfile, delimiter=',')
            data = []
            for c in content:
                data.append(c)
            return data, extension

"""
FILE DETAILS FOR THE UPLOADED FILES.
THE FUNCTION IS GENERATED BASED ON THE EXTENSION TYPE
"""
def file_details(request, slug):
    if request.user.is_authenticated or request.user.is_superuser:
        efile = File.objects.get(slug=slug)

        # check the extension
        check1 = str(efile.efile.url)
        # select the ext from the fullstop
        extension = check1[check1.index("."):]
        data, extension = read_sheet(efile.efile.path, extension)
        # try:
        #     df = pd.read_csv(efile.efile.path, error_bad_lines=False)
        #     print(len(df.columns))
        #     print(list(df.columns.values))
        # except:
        #     new_path = csv_from_excel(efile.efile.path)
        #     df = pd.read_csv(new_path, error_bad_lines=False)
        #     print(df)
        #     # df = pd.read_excel(efile.efile.path, sheet_name=None, error_bad_lines=False)
        #     # print(df.columns)
        #     # df2 = pd.DataFrame(df, columns=df.keys())

        #     # print(df2)

        context = {'efile': efile, 'data': data, 'extension': extension}
        return render(request, 'analyze/filedetails.html', context)
    else:
        return redirect("accounts:login")
"""
DOWNLOAD FILE BASED ON THE FILE PATH
"""
def download(request, path):
    if request.user.is_authenticated:
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    else:
        return redirect("accounts:login")
"""
PRINT THE EXCEL FILE
"""
def print_file(request, filepath):
    try:
        os.startfile(filepath, "print")
        print("Printing " + filepath)
        return redirect("analyze:myfiles")
    except:
        print("Not Supported OS")
        return redirect("analyze:myfiles")
"""
THIS IS FOR SUPERUSER OR ADMINISTRATOR TO DISPLAY ALL THE FILES IN THE WEBSITE
OPEN TO CHANGE
"""
def superuser_den(request):
    if request.user.is_superuser:
        reviews = ReviewList.objects.get(id=1)
        files = File.objects.all().order_by('-uploaded_on')
        allUsers = User.objects.all()
        context = {
            'files': files,
            'allUsers': allUsers,
            'reviews': reviews
        }
        return render(request, 'analyze/su.html', context)
    else:
        return redirect("analyze:home")

"""
EDIT FILE
"""
def edit_file(request, slug):
    if request.user.is_authenticated or request.user.is_superuser:
        fileE = File.objects.get(slug=slug)
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES, instance=fileE)
            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                return HttpResponseRedirect("/myfiles/%s" %slug)
        else:
            form = UploadFileForm(instance=fileE)
        return render(request, 'analyze/upload.html', {'form': form, 'msg': 'Edit File'})
    else:
        return redirect("analyze:myfiles")

"""
DELETE FILE
"""
def delete_file(request, slug):
    if request.user.is_authenticated or request.user.is_superuser:
        fileobj = File.objects.get(slug=slug)
        fileobj.delete()
        return redirect("analyze:myfiles")
    else:
        return redirect("analyze:myfiles")

