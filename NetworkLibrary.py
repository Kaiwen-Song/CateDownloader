import requests
import json
from re import *
import mechanize
import getpass
from lxml import html
import os
from requests.auth import HTTPBasicAuth
import requests

Cate_URL = "https://cate.doc.ic.ac.uk/"
Download_Dir = "/Downloads"
Notes_Type = "showfile"
Cate_Year_URL = "https://cate.doc.ic.ac.uk/timetable.cgi?keyt={}:1:{}:{}"

Course_String_Html = "//Module text()"

def format_cate_string(class_code, year, username):
    return Cate_Year_URL.format(class_code, year, username)

def get_year_of_access():
    return raw_input("Enter the year of access:")

def parse_note_module(agent, url):
    page = agent.open(url).read()
    tree = html.fromstring(page)
    return tree.xpath(Course_String_Html)

def get_class_code():
    return raw_input("Enter your class code:")

def get_term():
    return raw_input("Which term would you like to access:")

def create_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def are_notes(href):
    return parse_href_type(href) == Notes_Type

def parse_href_type(href):
    return href.split(".")[0]

def get_user_credentials():
    username =  raw_input('Enter your college user name:')
    password = getpass.getpass('Enter your password:')
    return username, password

def download_file(agent, directory, file_url, file_name):
    agent.retrieve(Cate_URL+file_url, file_name)
    print(file_name)

#on the main cate page finds the link to the course notes page and download every link
def download_notes_for_course(agent, directory, course_code, href):
    print("Downloading notes for course code {}".format(course_code))
    agent.open(href)
    links = agent.links()
    for link in links:
        if are_notes(link.url):
             print(link.url)
            # download_file(agent, directory, link.url, link.text)

