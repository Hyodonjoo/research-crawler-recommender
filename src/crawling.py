import requests
from bs4 import BeautifulSoup
import json

def crawl_and_save_json(start, end):
    base_url = "https://pubmed.ncbi.nlm.nih.gov/"
    
    data_list = []

    for number in range(start, end):
        url = f"{base_url}{number}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            title_element = soup.find('h1', {'class' : 'heading-title'}).text
            title = title_element.strip() if title_element else ''          
            # authors_list = soup.find_all('a', {'class' : 'full-name'})
            # authors = ','.join(set(author.text for author in authors_list))
            # pmid = soup.find('strong', {'class' : 'current-id'}).text
            #date = soup.find('span', {'class' : 'cit'}).text
            #abstract_element = soup.find('div', {'class' : 'abstract-content selected'}).text
            #abstract = abstract_element.strip() if abstract_element else ''
            try:
                abstract_element = soup.find('div', {'class' : 'abstract-content selected'})
                abstract = abstract_element.text.strip().replace('\n', '').replace('  ', '') if abstract_element else ''
            except AttributeError:
                print(f"Abstract not found for article {number}. Skipping...")
                continue
            #timestamp = "2023-12-01"  

            data_dict = {
                #'searchdate' : timestamp,
                'title': title,
                # 'pmid' : pmid,
                # 'authors': authors,
                #'date': date,
                # 'abstract': abstract
            }

            data_list.append(data_dict)

            progress = (number - start + 1) / (end - start) * 100
            print(f"Progress: {progress:.2f}%")

    # JSON 파일로 저장
    output_data = {"data": data_list}
    with open('output.json', 'w', encoding='utf-8') as json_file:
       json.dump(data_list, json_file, ensure_ascii=False, indent=4)

    # txt 파일로 저장    
    # with open('output.txt', 'w', encoding='utf-8') as txt_file:
    #     for data in data_list:
    #         txt_file.write(f"Title: {data['Title']}\n")
    #         txt_file.write(f"Authors: {data['Authors']}\n")
    #         txt_file.write(f"Abstract: {data['Abstract']}\n")
    #         txt_file.write("\n" + "="*30 + "\n\n")

if __name__ == "__main__":
    start_number = 20002000
    end_number = 20003000

    crawl_and_save_json(start_number, end_number)
