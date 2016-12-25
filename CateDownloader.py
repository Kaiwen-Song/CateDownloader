from NetworkLibrary import *
import argparse
#get the directory and login in formation from the user

#get the year and courses the user wishes to download

#create and navigate to the directory

#downlaod the files to the corresponding directory

Download_Path = "~/Downloads"
Download_Folder = Download_Path + "/Cate_Stuff"

parser = argparse.ArgumentParser()
parser.add_argument("-all")
args = parser.parse_args()
credentials = get_user_credentials()
#modules_to_download = get_modules_to_download()
# year = get_year_of_access()
# class_code = get_class_code()
year = "2015"
class_code = "c3"
# cate_url = format_cate_string(class_code, year, credentials['username'])
# print(cate_url)
course_map = parse_cate_for_course_codes(credentials, year, class_code)
print(course_map)
create_directory(Download_Folder)
distribute_download_from_cate_homepage(credentials, Download_Folder, course_map)