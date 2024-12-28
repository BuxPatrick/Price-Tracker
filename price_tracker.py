import requests, datetime, time, os, schedule, pandas as pd
from bs4 import BeautifulSoup
import smtplib, ssl

def track_prices():
    url = 'https://www.bose.com/p/headphones/bose-quietcomfort-ultra-headphones/QCUH-HEADPHONEARN.html?dwvar_QCUH-HEADPHONEARN_color=DIAMOND+60TH+EDITION&quantity=1'
    html_text = requests.get(url).text
    soup=BeautifulSoup(html_text,'html.parser')
    
    price = soup.find('span',{'class':'value'}).text

    price = price[1:]

    time_retrieved = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    test_string = time_retrieved + ", " + price

    file_name = r'price_tracker.txt'
    
    with open(file_name,"a") as f:
        f.write(test_string + '\n')
        f.close()

    if sum(1 for line in open(file_name)) == 1:
        pass
    else:  
        price_list = open(file_name,"r").read().split()
        price_difference = round(float(price_list[-1]) - float(price_list[-4]),2)
        
        if price_difference != 0:
            
            if price_difference > 0:
                email_message_info = ['increased']
            elif price_difference < 0:
                email_message_info = ['decreased']
                
            email_message_info.append(abs(price_difference))
            
            email = open(r'email.txt').read()
            password=open(r'password.txt').read()
            
            port = 465
            smtp_server = "smtp.gmail.com"
            sender_email = email
            receiver_email = email

            subject = "Price has {}".format(email_message_info[0])
            
            email_body = "The price has {} by {} The new price is {}. Go check it out here: {}""".format(email_message_info[0],
                                                                                                         email_message_info[1],
                                                                                                         float(price),
                                                                                                         url)
            
            message = 'Subject: {}\n\n{}'.format(subject,email_body)

            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(email, password)
                server.sendmail(sender_email, receiver_email, message)

schedule.every(5).seconds.do(track_prices)

while True:
    schedule.run_pending()
    time.sleep(1)