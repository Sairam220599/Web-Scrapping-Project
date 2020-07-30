#-----------Importing necessary libraries/packages-----------
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#------------Intializing the lists required to store details------------
clg_names = []
clg_addr = []
clg_webaddr = []
clg_emailaddr = []
clg_ContactNumber = []
clg_TPOname = []
clg_TPOnumber = []
clg_district = []
clg_region = []
clg_regiontype = []
clg_status = []
clg_autostatus = []


region = ['Amravati', 'Aurangabad' , 'Mumbai', 'Nagpur', 'Nashik', 'Pune']

#-----------Gathering region wise links-----------

print("Please wait. System is scrapping details for you.")
for i in range(6):
    page_link = "http://dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=" + str(i+1) + "&RegionName=" + region[i]

    page = requests.get(page_link)

    #-----------Scrapping each region page-------------
    soup = BeautifulSoup(page.content,'html.parser')

    table = soup.find('table',{"class": "DataGrid"})

    college_tags = table.findChildren('td')

    link_tags = []
    links = []
    i = 3

    #------------finding tags which have engineering colleges URLs and storing them-------------
    while True:
        if(i<=len(college_tags)):
            name = college_tags[i].text
            if "Engineering" in name or "Technology" in name or "Technical" in name or "Technological" in name:
                link_tags.append(college_tags[i-1])
        else:
            break
        i = i + 3

    #------------Storing all the URLs of colleges in a list------------
    for tag in link_tags:
        a_tag = tag.find('a',{'href': re.compile("^frm")})
        links.append('http://dtemaharashtra.gov.in/' + a_tag.get('href'))

    #-----------Extracting details of college and storing them in a list----------
    for link in links:

        college = requests.get(link)

        #-----------Scrapping each college page.--------------
        soup = BeautifulSoup(college.content,'html.parser')


        college_details = soup.find('table',{'class':'AppFormTable'})

        name_details = college_details.find('span',{"id": "ctl00_ContentPlaceHolder1_lblInstituteNameEnglish"})
        region_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblRegion"})
        addr_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblAddressEnglish"})
        district_details = college_details.find('span', {"id" : "ctl00_ContentPlaceHolder1_lblDistrict"})
        regiontype_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblRegionType"})
        webaddr_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblWebAddress"})
        email_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblEMailAddress"})
        ContactNum_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblPersonalPhoneNo"}).getText().split()
        TPO_name = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblRegistrarNameEnglish"})
        TPO_number = college_details.find('span',{"id": "ctl00_ContentPlaceHolder1_lblOfficePhoneNo"}).getText().split()
        status1 = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblStatus1"})
        status2 = college_details.find('span', {"id" : "ctl00_ContentPlaceHolder1_lblStatus2"})

        #----------checking for null data------------
        if name_details.text!="" and addr_details.text!="" and district_details.text!="" and webaddr_details.text!="" and email_details.text!="" and ContactNum_details[0].isnumeric() and TPO_name.text!="" and TPO_number[0].isnumeric():

            clg_names.append(name_details.text)
            clg_region.append(region_details.text)
            clg_regiontype.append(regiontype_details.text)
            clg_addr.append(addr_details.text)
            clg_district.append(district_details.text)
            clg_webaddr.append(webaddr_details.text)
            clg_emailaddr.append(email_details.text)
            clg_ContactNumber.append(ContactNum_details[0])
            clg_TPOname.append(TPO_name.text)
            clg_TPOnumber.append(TPO_number[0])
            clg_status.append(status1.text)
            clg_autostatus.append(status2.text)


#-----------Converting the lists into a dictionary-----------
college_data = {'College Name':clg_names,'Region': clg_region, 'Region Type':clg_regiontype ,'Address':clg_addr, 'District':clg_district ,'Website':clg_webaddr, 'Email address':clg_emailaddr, 'Contact Number': clg_ContactNumber, 'TPO name': clg_TPOname, 'TPO contact number':clg_TPOnumber, 'Status':clg_status, 'Autonomous Status': clg_autostatus}

#-----------Converting the dictonary into a dataframe----------
df = pd.DataFrame(college_data)

#-----------storing the dataframe as csv file locally-----------
df.to_csv('college_file.csv', index = False, header=True)

print("Thank you for your patience!!!")
print("Your csv file is ready.")

#-----------Visualization Section------------
fig1 ,ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

#-----------Visualizing No. of colleges region wise------------
Region = df.groupby('Region').count()['College Name']

ax1.pie(Region, labels=Region.index , autopct='%1.1f%%')
ax1.set_title('No. of Colleges Region wise.')

#-----------Visualizing Colleges by their autonomous status------------
Auto_By_Region = df.groupby(['Region','Autonomous Status']).count()['College Name']

auto = []
non_auto = []
for i in range(len(Auto_By_Region)):
    if(i%2==0):
        auto.append(Auto_By_Region[i])
    else:
        non_auto.append(Auto_By_Region[i])

x = np.arange(len(Region.index))
width = 0.35

rect1 = ax2.bar(x - width/2, auto, width, label='Autonomous')
rect2 = ax2.bar(x + width/2, non_auto, width, label='Non Autonomous')
ax2.legend()
ax2.set_xticks(x)
ax2.set_xticklabels(Region.index)
ax2.set_ylabel('No. of Colleges')
ax2.set_title('No. of Autonmous vs non-Autonomous per Region')

#-----------function to label the no. of colleges on the bar chart-------------
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax2.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel(rect1)
autolabel(rect2)

fig2.tight_layout()
plt.show()



