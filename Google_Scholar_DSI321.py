#!/usr/bin/env python
# coding: utf-8

# # Google Scholar : Title

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH='./chromedriver'
driver = webdriver.Chrome(PATH)

driver.get("https://scholar.google.com/")
print(driver.title)


# In[ ]:


#enter Thammasat University
search_box = driver.find_element_by_name('q')
search_box.send_keys("Thammasat University", Keys.ENTER)


# In[ ]:


driver.implicitly_wait(3)


# In[ ]:


#click use profile for: Thammasat University 
select_2 = driver.find_element_by_css_selector('div.gs_ob_inst_r')
select_2.find_element_by_css_selector('a').click()


# In[ ]:


#create dataframe to contain data
import pandas as pd

df = pd.DataFrame(
    {
        'user_ID':[],
        'name':[],
        'affiliation':[]
    })


# In[ ]:


while 1:
    
    for i in driver.find_elements(By.CSS_SELECTOR, 'div.gs_ai_t'): #loop to collect data each profile
        author = i.find_element_by_css_selector('a') #collect author name
        aff = i.find_element_by_css_selector('div.gs_ai_aff') #collect affiliation
        print(
            author.get_attribute('href').split('=')[-1], #User_ID
            author.text,
            aff.text
        )
        #append in dataframe
        df = df.append( 
        {
            'user_ID' : author.get_attribute('href').split('=')[-1],
            'name' : author.text,
            'affiliation' : aff.text
        }
        , ignore_index=True
        )
    #wait
    driver.implicitly_wait(3)
    #click next page
    x=driver.find_element_by_css_selector('#gsc_authors_bottom_pag > div > button.gs_btnPR.gs_in_ib.gs_btn_half.gs_btn_lsb.gs_btn_srt.gsc_pgn_pnx')
    x.click()


# In[ ]:


#save into CSV file
df.to_csv('DataSet1.csv')


# # Google scholar: Paper

# In[ ]:


#create dataframe to contain data
df = pd.DataFrame(
    {
        'title': [],
        'authors': [],
        'publication_date': [],
        'description': [],
        'cite_by': []
    })


# In[ ]:


xpath = 2 #define xpath

while True:
    for person in driver.find_elements(By.CSS_SELECTOR, 'h3.gs_ai_name'): #loop to click each profile
        xpath = str(xpath)
        driver.find_element_by_xpath('//[@id="gsc_sa_ccl"]/div['+xpath+']/div/div/h3/a').click()

        while 1:
            for j in driver.find_elements(By.XPATH, '//*[@id="gsc_a_b"]'): #loop in page that contain all paper per profile
                for x in driver.find_elements(By.CSS_SELECTOR, 'td.gsc_a_t'): #loop to click each paper 
                    x.find_element_by_css_selector('a').click()
                    for i in driver.find_elements(By.ID, 'gsc_ocd_bdy'): #loop in window that contain data
                        
                        # title มี 2 ที่
                        if i.find_element_by_id('gsc_vcd_title').text == None: #option1 to collect title
                            title = i.find_element_by_css_selector('a.gsc_vcd_title_link').text,
                        else: #option2 to collect title
                            title = i.find_element_by_id('gsc_vcd_title').text,

                        
                        author = i.find_element_by_css_selector('div.gsc_vcd_value').text #collect author data
                        publication_date = i.find_element_by_xpath('//*[@id="gsc_vcd_table"]/div[2]/div[2]').text, #collect PD. data
                        # description มี 2 ที่
                        if i.find_element_by_class_name('gsh_small').text == None: #option1 to collect des.
                            description = i.find_element_by_class_name('gsh_csp').text,
                        elif i.find_element_by_class_name('gsh_small').text != None: #option2 to collect des.
                            description = i.find_element_by_class_name('gsh_small').text,    
                        cite_by = i.find_element_by_class_name('gsc_vcd_value').text #collect cite_by data

                        df = df.append( #append data in data frame that we crated
                            {
                                'title': title,
                                'authors': author,
                                'publication_date': publication_date,
                                'description': description,
                                'cite_by': cite_by
                            }, ignore_index=True
                        )
                     
                    #click close window that show data each paper
                    close_title = driver.find_element_by_xpath('//*[@id="gs_md_cita-d-x"]').click() 
            break

        xpath = int(xpath)
        xpath += 1 #increae xpath
        driver.implicitly_wait(3)
        driver.back()


# In[ ]:


#save into CSV file
df.to_csv('DataSet2_.csv')


# # จัดรูปให้อยู่ใน 1NF form

# In[ ]:


#create new dataframe to contain data
new_table = pd.DataFrame(columns=['title','authors','publication_date','description','cite_by'])
#read file
df = pd.read_csv('DataSet2.csv')
#define rows=0
rows = 0
#loop to reform data
for index, row in df.iterrows():
    for token in row['authors'].split(','):
        new_table.loc[rows]=[row['title'],token,row['publication_date'],row['description'],row['cite_by']]
        rows += 1
#save to CSV file
new_table.to_csv('new_paper.csv')

