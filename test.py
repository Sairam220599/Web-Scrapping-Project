from bs4 import BeautifulSoup
import requests
import csv
import re
import pandas as pd
import matplotlib.pyplot as plt



c_names = []
c_addr = []
c_webaddr = []
c_emailaddr = []
c_ContactNumber = []
c_TPOname = []
c_TPOnumber = []
c_district = []
c_region = []
c_status = []



region = ['Amravati', 'Aurangabad' , 'Mumbai', 'Nagpur', 'Nashik', 'Pune']

for i in range(6):
    page_link = "http://dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=" + str(i+1) + "&RegionName=" + region[i]

    page = requests.get(page_link)

    soup = BeautifulSoup(page.content,'html.parser')

    table = soup.find('table',{"class": "DataGrid"})

    college_tags = table.findChildren('td')

    link_tags = []
    links = []
    i = 3

    while True:
        if(i<=len(college_tags)):
            name = college_tags[i].text
            if "Engineering" in name or "Technology" in name or "Technical" in name or "Technological" in name:
                link_tags.append(college_tags[i-1])
        else:
            break
        i = i + 3


    print(link_tags)

    for tag in link_tags:
        a_tag = tag.find('a',{'href': re.compile("^frm")})
        links.append('http://dtemaharashtra.gov.in/' + a_tag.get('href'))

    for link in links:

        college = requests.get(link)
        #print(links[i])

        soup = BeautifulSoup(college.content,'html.parser')
        print(soup)

        college_details = soup.find('table',{'class':'AppFormTable'})

        name_details = college_details.find('span',{"id": "ctl00_ContentPlaceHolder1_lblInstituteNameEnglish"})
        region_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblRegion"})
        addr_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblAddressEnglish"})
        district_details = college_details.find('span', {"id" : "ctl00_ContentPlaceHolder1_lblDistrict"})
        webaddr_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblWebAddress"})
        email_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblEMailAddress"})
        ContactNum_details = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblPersonalPhoneNo"}).getText().split()
        TPO_name = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblRegistrarNameEnglish"})
        TPO_number = college_details.find('span',{"id": "ctl00_ContentPlaceHolder1_lblOfficePhoneNo"}).getText().split()
        status1 = college_details.find('span', {"id": "ctl00_ContentPlaceHolder1_lblStatus1"})

        if name_details.text!="" and addr_details.text!="" and district_details.text!="" and webaddr_details.text!="" and email_details.text!="" and ContactNum_details[0].isnumeric() and TPO_name.text!="" and TPO_number[0].isnumeric():

            c_names.append(name_details.text)
            c_region.append(region_details.text)
            c_addr.append(addr_details.text)
            c_district.append(district_details.text)
            c_webaddr.append(webaddr_details.text)
            c_emailaddr.append(email_details.text)
            c_ContactNumber.append(ContactNum_details[0])
            c_TPOname.append(TPO_name.text)
            c_TPOnumber.append(TPO_number[0])
            c_status.append(status1.text)



college_data = {'College Name':c_names,'Region': c_region,'Address':c_addr, 'District':c_district ,'Website':c_webaddr, 'Email address':c_emailaddr, 'Contact Number': c_ContactNumber, 'TPO name': c_TPOname, 'TPO contact number':c_TPOnumber, 'Status':c_status}

df = pd.DataFrame(college_data)

df.to_csv('college.csv', index = False, header=True)

Region = df.groupby('Region').count()['College Name']

plt.pie(Region, labels=Region.index , autopct='%1.1f%%')
plt.set_title('No. of Colleges per Region.')

plt.show()
