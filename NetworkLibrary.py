import mechanize
import getpass
from lxml import html
import os
import multiprocessing as mp

Cate_URL = "https://cate.doc.ic.ac.uk/"
Download_Dir = "/Downloads"
Notes_Type = "showfile"
Cate_Year_URL = "https://cate.doc.ic.ac.uk/timetable.cgi?keyt={}:{}:{}:{}"

Module_Page_Type = "notes"
Course_String_Html = "//Module text()"
terms = range(1,7)

def format_cate_string(class_code, year, username):
    return Cate_Year_URL.format(class_code, year, username)

def get_user_credentials():
    username =  raw_input('Enter your college user name:')
    password = getpass.getpass('Enter your password:')
    return {'username':username, 'password':password}

def get_year_of_access():
    return raw_input("Enter the year of access:")

def get_class_code():
    return raw_input("Enter your class code:")

def create_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def are_notes(href):
    return parse_href_type(href) == Notes_Type

def parse_href_type(href):
    return href.split(".")[0]

def download_file_from_url(agent, file_url, save_dir, file_name):
    agent.retrieve(Cate_URL+file_url, save_dir +"/"+ file_name)
    print(file_name)

def is_module_page(href):
    return parse_href_type(href) == Module_Page_Type

def parse_term_page(agent, url):
    cc_map = {}
    agent.open(url)
    links = filter(lambda link:is_module_page(link.url), agent.links())
    for link in links:
        html_str = agent.open(link.url).read()
        tree = html.fromstring(html_str)
        headers = tree.xpath('//b')[1].text.split(':')
        cc = headers[0]
        course_title = headers[1]
        cc_map[cc] = {"course title": course_title, "url": Cate_URL+link.url}
    return cc_map

def parse_cate_for_course_codes(credentials, year, class_code):
    agent = mechanize.Browser()
    agent.add_password(Cate_URL, credentials['username'], credentials['password'])
    cc_map = {}
    for term in terms:
        print(term)
        term_url = Cate_Year_URL.format(year,str(term), class_code, credentials['username'])
        codes = parse_term_page(agent, term_url)
        cc_map.update(codes)
    return cc_map

#on the main cate page finds the link to the course notes page and download every link
def download_all_from_module_page(credentials, module_page_url, download_dir, course):
    p = mp.current_process()
    save_to_dir = download_dir + "/" + course
    create_directory(save_to_dir)
    print("current process is working on module {}".format(p.name))
    agent = mechanize.Browser()
    agent.add_password(Cate_URL, credentials['username'], credentials['password'])
    agent.open(module_page_url)
    links = filter(lambda link: are_notes(link.url), agent.links())
    for link in links:
        print(link.url, link.text)
        download_file_from_url(agent, link.url, save_to_dir, link.text)
    print("finished grabbing all the notes for module {}".format(p.name))
    p.terminate()


def distribute_download_from_cate_homepage(credentials, download_dir, cc_map):
    #builds a dictionary of cate number to course code
    jobs = []
    #match all notes directory href and add the mapping to dictionary
    for module in cc_map:
        #for each module that needs to be downloaded, spawns a new process and an agent to download
        title = cc_map[module]['course title']
        url = cc_map[module]['url']
        p = mp.Process(target = download_all_from_module_page,
                       args=(credentials, url, download_dir, module + title),name=module + title)
        jobs.append(p)
        p.start()
    #spawn a new process that goes and download the notes from each modules requested
