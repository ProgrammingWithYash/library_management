# create database library_management;
# use library_management;
# create table books (id INT PRIMARY KEY AUTO_INCREMENT, book_name VARCHAR(255), author VARCHAR(255), total INT, subject VARCHAR(255));
# create table issue (id INT PRIMARY KEY AUTO_INCREMENT, st_name VARCHAR(255), book_id VARCHAR(255), issue_date TIMESTAMP, issued_for_days TIMESTAMP);


from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

import mysql.connector as sql

from datetime import datetime
from datetime import timedelta
import dateparser


con = sql.connect(host='localhost', user='root',
                  passwd='1234', database='library_management')

c = con.cursor()
d = con.cursor()


def index(request):

    c.execute('select * from books')

    arr = []
    i = 0
    for x in c:
        arr.append([i + 1])
        for y in x:
            arr[i].append(y)

        i += 1

    template = loader.get_template('index.html')
    context = {
        'title': 'View Books',
        'books': arr,
        'page': 'books'
    }

    return HttpResponse(template.render(context, request))


def issued(request):

    c.execute('select i.id, st_name, i.book_id, issue_date, issued_for_days, b.id, b.book_name from issue i, books b where b.id = i.book_id')

    arr = []
    i = 0

    mycursor = c
    for x in mycursor:
        arr.append([i + 1])

        leftdays = datetime.strptime(
            (x[3] + timedelta(days=x[4])).strftime('%d %B, %Y'), '%d %B, %Y') - datetime.now()

        arr[i].extend([x[0], x[1], x[2], x[3].strftime('%d %B, %Y'), x[4],
                      x[5], x[6], (x[3] + timedelta(days=x[4])).strftime('%d %B, %Y'), str(leftdays)[0:2]])

        # d.execute('select * from books')

        # for a in d:
        #     print(a)
        #     if a[0] == x[2]:
        #         arr[i].append(a[0], a[1])

        i += 1

    c.execute('select * from books')

    book_arr = []
    i = 0
    for x in c:
        book_arr.append(x[0])

        i += 1

    print(arr)

    template = loader.get_template('index.html')
    context = {
        'title': 'View Books',
        'issued': arr,
        'books': book_arr,
        'page': 'issued'
    }

    return HttpResponse(template.render(context, request))


def add(request):

    c.execute('select i.id, st_name, i.book_id, issue_date, issued_for_days, b.id, b.book_name from issue i, books b where b.id = i.book_id')

    arr = []
    i = 0

    mycursor = c
    for x in mycursor:
        arr.append([i + 1])

        leftdays = datetime.strptime(
            (x[3] + timedelta(days=x[4])).strftime('%d %B, %Y'), '%d %B, %Y') - datetime.now()

        arr[i].extend([x[0], x[1], x[2], x[3].strftime('%d %B, %Y'), x[4],
                      x[5], x[6], (x[3] + timedelta(days=x[4])).strftime('%d %B, %Y'), str(leftdays)[0:2]])

        # d.execute('select * from books')

        # for a in d:
        #     print(a)
        #     if a[0] == x[2]:
        #         arr[i].append(a[0], a[1])

        i += 1

    c.execute('select * from books')

    book_arr = []
    i = 0
    for x in c:
        book_arr.append(x[0])

        i += 1

    template = loader.get_template('add_book.html')
    context = {
        'title': 'Add a Book',
        'issued': arr,
        'books': book_arr,
        'page': 'add',
        'id': 0,
        'name': "",
        'author': "",
        'total': "",
        'subject': "",
    }

    return HttpResponse(template.render(context, request))


@csrf_exempt
def addInsert(request):
    name = request.POST['name']
    author = request.POST['author']
    total = request.POST['total']
    subject = request.POST['subject']

    if (request.POST['type'] == "insert"):
        c.execute(
            f"insert into books (book_name, author, total, subject) values ('{name}', '{author}', {total}, '{subject}')")
    else:
        c.execute(
            f"update books set book_name = '{name}', author = '{author}', total = {total}, subject = '{subject}' where id = {request.POST['id']}")

    con.commit()

    return HttpResponse("Hello world!")


def issue(request):

    c.execute('select i.id, st_name, i.book_id, issue_date, issued_for_days, b.id, b.book_name from issue i, books b where b.id = i.book_id')

    arr = []
    i = 0

    mycursor = c
    for x in mycursor:
        arr.append([i + 1])

        leftdays = datetime.strptime(
            (x[3] + timedelta(days=x[4])).strftime('%d %B, %Y'), '%d %B, %Y') - datetime.now()

        arr[i].extend([x[0], x[1], x[2], x[3].strftime('%d %B, %Y'), x[4],
                      x[5], x[6], (x[3] + timedelta(days=x[4])).strftime('%d %B, %Y'), str(leftdays)[0:2]])

        # d.execute('select * from books')

        # for a in d:
        #     print(a)
        #     if a[0] == x[2]:
        #         arr[i].append(a[0], a[1])

        i += 1

    c.execute('select * from books')

    book_arr = []
    i = 0
    for x in c:
        book_arr.append([x[0], x[1]])

        i += 1

    template = loader.get_template('add_book.html')
    context = {
        'title': 'Issue a Book',
        'issued': arr,
        'books': book_arr,
        'page': 'issue',
        'datetoday': datetime.now().strftime('%d-%m-%Y'),
        'id': 0,
        'name': "",
        'author': "",
        'total': "",
        'subject': "",
    }

    return HttpResponse(template.render(context, request))


@csrf_exempt
def issueInsert(request):
    name = request.POST['stName']
    author = request.POST['book']
    total = dateparser.parse(request.POST['issuedOn'])
    subject = request.POST['issuedFor']

    if (request.POST['type'] == "insert"):
        c.execute(
            f"insert into issue (st_name, book_id, issue_date, issued_for_days) values ('{name}', '{author}', '{total}', '{subject}')")
    else:
        c.execute(
            f"update issue set st_name = '{name}', book_id = '{author}', issue_date = '{total}', issued_for_days = '{subject}' where id = {request.POST['id']}")

    # c.execute(
        # f"insert into issue (st_name, book_id, issue_date, issued_for_days) values ('{name}', '{author}', '{total}', '{subject}')")

    con.commit()

    return HttpResponse("Hello world!")


@csrf_exempt
def bookdelete(request):
    id = request.POST['id']
    c.execute(f"delete from books where id = {id}")
    con.commit()
    c.execute(f"delete from issue where book_id = {id}")
    con.commit()

    print(f"delete from books where id = {id}")

    return HttpResponse("Hello world!")


@csrf_exempt
def issuedelete(request):
    id = request.POST['id']
    c.execute(f"delete from issue where id = {id}")
    con.commit()

    print(f"delete from issue where id = {id}")

    return HttpResponse("Hello world!")


def addEdit(request):

    c.execute('select i.id, st_name, i.book_id, issue_date, issued_for_days, b.id, b.book_name from issue i, books b where b.id = i.book_id')

    arr = []
    i = 0

    mycursor = c
    for x in mycursor:
        arr.append([i + 1])

        leftdays = datetime.strptime(
            (x[3] + timedelta(days=x[4])).strftime('%d %B, %Y'), '%d %B, %Y') - datetime.now()

        arr[i].extend([x[0], x[1], x[2], x[3].strftime('%d %B, %Y'), x[4],
                      x[5], x[6], (x[3] + timedelta(days=x[4])).strftime('%d %B, %Y'), str(leftdays)[0:2]])

        # d.execute('select * from books')

        # for a in d:
        #     print(a)
        #     if a[0] == x[2]:
        #         arr[i].append(a[0], a[1])

        i += 1

    bookid = request.GET['id']

    # print(f'select * from books where id={bookid}')
    c.execute(f'select * from books where id={bookid}')

    book_arr = []
    i = 0
    for x in c:
        book_arr.extend([x[0], x[1], x[2], x[3], x[4]])

        i += 1

    template = loader.get_template('add_book.html')
    context = {
        'title': 'Add a Book',
        'issued': arr,
        'books': book_arr,
        'page': 'addEdit',
        'id': book_arr[0],
        'name': book_arr[1],
        'author': book_arr[2],
        'total': book_arr[3],
        'subject': book_arr[4],
    }

    return HttpResponse(template.render(context, request))


def issueEdit(request):

    c.execute('select i.id, st_name, i.book_id, issue_date, issued_for_days, b.id, b.book_name from issue i, books b where b.id = i.book_id')

    arr = []
    i = 0

    mycursor = c
    for x in mycursor:
        arr.append([i + 1])

        leftdays = datetime.strptime(
            (x[3] + timedelta(days=x[4])).strftime('%d %B, %Y'), '%d %B, %Y') - datetime.now()

        arr[i].extend([x[0], x[1], x[2], x[3].strftime('%d %B, %Y'), x[4],
                      x[5], x[6], (x[3] + timedelta(days=x[4])).strftime('%d %B, %Y'), str(leftdays)[0:2]])

        # d.execute('select * from books')

        # for a in d:
        #     print(a)
        #     if a[0] == x[2]:
        #         arr[i].append(a[0], a[1])

        i += 1

    bookid = request.GET['id']

    print(f'select * from issue where id={bookid}')
    c.execute(f'select * from issue where id={bookid}')

    book_arr = []
    i = 0
    for x in c:
        book_arr.extend([x[0], x[1], x[2], x[3], x[4]])

        i += 1
    
    c.execute('select * from books')

    myarr = []
    i = 0
    for x in c:
        myarr.append([x[0], x[1]])

        i += 1

    print(book_arr)

    template = loader.get_template('add_book.html')
    context = {
        'title': 'Add a Book',
        'issued': arr,
        'books': myarr,
        'page': 'issueEdit',
        'id': book_arr[0],
        'name': book_arr[1],
        'author': int(book_arr[2]),
        'total': book_arr[3].strftime('%d-%m-%Y'),
        'subject': book_arr[4],
    }

    return HttpResponse(template.render(context, request))
