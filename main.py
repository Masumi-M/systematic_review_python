import numpy as np
import pandas as pd

text_path = "./output/hit_num.txt"

# Import Data
scp_raw = pd.read_csv('./scopus.csv')
wos_raw = pd.read_excel('./wos.xls')
pub_raw = pd.read_csv('./pubmed.csv')

print("=== Raw ===")
scp_preproc = scp_raw.copy()
scp_preproc = scp_preproc.loc[:, ['著者名', 'タイトル', '出版年',
                                  '出版物名', 'DOI', '抄録', '著者キーワード', '索引キーワード', '本文言語', '文献タイプ', '出版段階', '情報源', 'リンク']]
                                  
wos_preproc = wos_raw.copy()
wos_preproc = wos_preproc.loc[:, [
    'Authors', 'Article Title', 'Publication Year', 'Source Title', 'DOI', 'Abstract', 'Author Keywords', 'Keywords Plus', 'Language', 'Document Type', 'Research Areas', 'WoS Categories']]
    
pub_preproc = pub_raw.copy()
pub_preproc = pub_preproc.loc[:, ['Authors', 'Title', 'Publication Year', 'Journal/Book', 'DOI']]

print("=== Before 2019 ===")
scp_preproc_bef19 = scp_preproc.copy()
wos_preproc_bef19 = wos_preproc.copy()
pub_preproc_bef19 = pub_preproc.copy()

scp_preproc_bef19 = scp_preproc_bef19[scp_preproc_bef19['出版年'] < 2020]
wos_preproc_bef19 = wos_preproc_bef19[wos_preproc_bef19['Publication Year'] < 2020] 
pub_preproc_bef19 = pub_preproc_bef19[pub_preproc_bef19['Publication Year'] < 2020]

print("scopus: " + str(len(scp_preproc_bef19)))
print("wos: " + str(len(wos_preproc_bef19)))
print("pubmed: " + str(len(pub_preproc_bef19)))

with open(text_path, mode='w') as f_hitnum:
    f_hitnum.write("scopus: " + str(len(scp_preproc_bef19)) + "\n")
    f_hitnum.write("wos: " + str(len(wos_preproc_bef19)) + "\n")
    f_hitnum.write("pubmed: " + str(len(pub_preproc_bef19)) + "\n\n") 

total_1 = len(scp_preproc_bef19) + len(wos_preproc_bef19) + len(pub_preproc_bef19)
print("Total (1 - raw): " + str(total_1))
with open(text_path, mode='a') as f_hitnum:
    f_hitnum.write("Total (1 - raw): " + str(total_1) + "\n")

# 2. Preprocessing - Duplicate Removal
scp_preproc_bef19 = scp_preproc_bef19.rename(columns={'著者名': 'Authors','タイトル': 'Title','出版年':'Publication Year', '出版物名':'Journal/Book', '抄録':'Abstract', '著者キーワード':'Author Keywords', '索引キーワード':'Keywords Plus', '本文言語':'Language','文献タイプ':'Document Type'})
wos_preproc_bef19 = wos_preproc_bef19.rename(columns={'Article Title': 'Title', 'Source Title':'Journal/Book'})

data_merge = pd.concat([scp_preproc_bef19, wos_preproc_bef19, pub_preproc_bef19])
data_merge['Title_Lower'] = data_merge['Title'].str.lower()
data_merge = data_merge.drop_duplicates(['DOI'], keep='first')
data_merge = data_merge.drop_duplicates(['Title_Lower'], keep='first')
total_2 = len(data_merge)
print("Total (2 - duplicate removal): " + str(total_2))
with open(text_path, mode='a') as f_hitnum:
    f_hitnum.write("Total (2 - duplicate removal): " + str(total_2) + "\n")

def show_list(col_name):
    col_list = data_merge[col_name].values
    col_list = np.sort(col_list)
    print(col_list)
# show_list('Language')
# show_list('Document Type')

# 3. Exclusion based on title and abstracts
data_merge_xls_master = data_merge.loc[:, ['Publication Year', 'Title', 'Abstract', 'Authors', 'Journal/Book', 'Language', 'DOI', 'Document Type', 'Research Areas', '出版段階','Author Keywords','Keywords Plus', '情報源', 'リンク']]
data_merge_xls_check = data_merge.loc[:, ['Publication Year', 'Title', 'Abstract']]
data_merge_xls_check['include'] = 0
data_merge_xls_check['exclude'] = 0
data_merge_xls_check['note'] = ''

xlsx_path_master = './output/master.xlsx'
xlsx_path_check = './output/check.xlsx'
data_merge_xls_master.to_excel(xlsx_path_master, sheet_name='masterdata')
data_merge_xls_check.to_excel(xlsx_path_check, sheet_name='check_data')

print("===== Download Xlsx Done. =====")
