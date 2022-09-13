<<<<<<< HEAD
from bs4 import BeautifulSoup
import requests
import json

def GetSkill(Skills):
    i = 0
    arr = []

    for skill in Skills:
        if 'Cooldown' in skill:
            arr.append(Skills[i:i+4])
            return arr
        arr.append(skill)
        i = i + 1
def npformat(np_info):
    np_info = np_info[2:]
    try:
        np_text = {
        'base':np_info[0],
        'rank': np_info[np_info.index('Rank')] +' '+np_info[np_info.index('Rank')+2],
        'type': np_info[np_info.index('Noble Phantasm Type')] + ' '+np_info[np_info.index('Noble Phantasm Type')+2],
        'Hits': np_info[np_info.index('Hits')] + ' '+np_info[np_info.index('Hits')+2],
        'Scaling': np_info[np_info.index('NP Level')+6:np_info.index('Overcharge Effect')],
        'Effect': np_info[np_info.index('Effect'):np_info.index('Effect')+2]
        
    }
    except:
        np_text = {
        'base':np_info[0],
        'rank': np_info[np_info.index('Rank')] +' '+np_info[np_info.index('Rank')+3],
        'type': np_info[np_info.index('Noble Phantasm Type')] + ' '+np_info[np_info.index('Noble Phantasm Type')+3],
        'Hits':'Support NP',
        'Scaling': np_info[np_info.index('NP Level')+6:np_info.index('Overcharge Effect')],
        'Effect': np_info[np_info.index('Effect'):np_info.index('Effect')+2]
    }
        
    upgradeindex = [np_info.index(i) for i in np_info if 'Upgrade' in i]
    if len(upgradeindex) != 0:
        np_text['Overcharge Effect'] = np_info[np_info.index('Overcharge Effect'):upgradeindex[0]]
        np_text['Upgrade'] = npformat(np_info[upgradeindex[0]:])
    else:
        np_text['Overcharge Effect'] = np_info[np_info.index('Overcharge Effect'):]

    return np_text


def GetServant(url):
    html_text = requests.get('https://fategrandorder.fandom.com/wiki/'+url)
    print(url)
    soup = BeautifulSoup(html_text.text,'lxml')

    #retriving stats
    servantinfo = soup.find('div',class_="ServantInfoStatsWrapper")
    servantdic = {}
    for line in servantinfo.text.splitlines():
        if line != '' and 'Japanese Name:' not in line and 'Hits' not in line:
            arr = line.split(':')
            try: 
                servantdic.update({arr[0].strip():arr[1].strip()})
            except:
                print('exception occured')
                continue
    servantlist = {int(servantdic["ID"]):servantdic}
    #retriving art
    servantart = soup.find_all('img',class_='pi-image-thumbnail')
    art = []
    for element in servantart:
        art.append(element['src'])
    servantlist[int(servantdic["ID"])]['art'] = art


    #retriving skills
    AllSkills = {}
    skills= []
    skills_html = soup.find('div',class_='tabber wds-tabber')
    filteredskills = skills_html.text.replace('Level\n\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10','').splitlines()[2:]

    for line in filteredskills:
        if line !='':
            skills.append(line.strip())
    i=0
    skill_num = 1
    for skill in skills:
        if 'Available from' in skill or 'Unlocks after' in skill:
            AllSkills[skill_num] = GetSkill(skills[i:])
            skill_num = skill_num + 1
        if 'Upgrades after' in skill:
            AllSkills[skill_num-1].append(GetSkill(skills[i:]))
        i = i+1

    servantlist[int(servantdic["ID"])]['skills'] = AllSkills
    
    #getting noble phantasms
    if url == 'Beast_IV':
        servantlist[int(servantdic["ID"])]['NP'] = 'None'
        return servantlist
        
    np = soup.find('h2',text ='Noble Phantasm').find_next('div',class_='tabber wds-tabber')
    np_name = np.caption.b.text
    np_ftext = np.caption.b.find_next('b').text
    np_text = {'name':np_name,'ftext':np_ftext}
    np_info = []
    for text in np.text.splitlines():
        if text != '':
            np_info.append(text.strip())
    if 'Old' in np_info[len(np_info)-1] or 'Costume' in np_info[len(np_info)-1] or 'Stage' in np_info[len(np_info)-1]:
        np_info.pop()
    np_text.update(npformat(np_info))    
        
    servantlist[int(servantdic["ID"])]['NP'] =np_text
    return servantlist


def GetList():
    html_text = requests.get('https://fategrandorder.fandom.com/wiki/Servant_List_by_ID#1_~_100')
    soup = BeautifulSoup(html_text.text,'lxml')
    soup.prettify()

    page = soup.find('div', class_="tabber wds-tabber")
    table = page.find('tbody')

    links = page.find_all('a',href=True)
    output = ''
    for servant in links:
        if servant != '':
            output += servant.text.strip() +'\n'
    output = output.replace(" ","_").replace('Edit','')[40:]
    output = output.replace('\n\n','\n').replace('\n\n','\n').splitlines()
    return output


ServantList = GetList()
completelist = {}
i=1
for servant in ServantList:
    if servant == 'Hyde': #hyde has two entries so we skip one, both link to the same page
        continue
    if servant == 'Solomon' and i==152:
        servant = 'Solomon_(True)'
    completelist.update(GetServant(servant))
    try:
        completelist[i]['AKA'] = completelist[i]['AKA'] + ", "+ servant.replace('_',' ')
    except:
        completelist[i]['AKA'] = servant.replace('_',' ')
    i = i + 1
with open('.\\Data\\Data.json','w') as file:
=======
from bs4 import BeautifulSoup
import requests
import json

def GetSkill(Skills):
    i = 0
    arr = []

    for skill in Skills:
        if 'Cooldown' in skill:
            arr.append(Skills[i:i+4])
            return arr
        arr.append(skill)
        i = i + 1
def npformat(np_info):
    np_info = np_info[2:]
    try:
        np_text = {
        'base':np_info[0],
        'rank': np_info[np_info.index('Rank')] +' '+np_info[np_info.index('Rank')+2],
        'type': np_info[np_info.index('Noble Phantasm Type')] + ' '+np_info[np_info.index('Noble Phantasm Type')+2],
        'Hits': np_info[np_info.index('Hits')] + ' '+np_info[np_info.index('Hits')+2],
        'Scaling': np_info[np_info.index('NP Level')+6:np_info.index('Overcharge Effect')],
        'Effect': np_info[np_info.index('Effect'):np_info.index('Effect')+2]
        
    }
    except:
        np_text = {
        'base':np_info[0],
        'rank': np_info[np_info.index('Rank')] +' '+np_info[np_info.index('Rank')+3],
        'type': np_info[np_info.index('Noble Phantasm Type')] + ' '+np_info[np_info.index('Noble Phantasm Type')+3],
        'Hits':'Support NP',
        'Scaling': np_info[np_info.index('NP Level')+6:np_info.index('Overcharge Effect')],
        'Effect': np_info[np_info.index('Effect'):np_info.index('Effect')+2]
    }
        
    upgradeindex = [np_info.index(i) for i in np_info if 'Upgrade' in i]
    if len(upgradeindex) != 0:
        np_text['Overcharge Effect'] = np_info[np_info.index('Overcharge Effect'):upgradeindex[0]]
        np_text['Upgrade'] = npformat(np_info[upgradeindex[0]:])
    else:
        np_text['Overcharge Effect'] = np_info[np_info.index('Overcharge Effect'):]

    return np_text


def GetServant(url):
    html_text = requests.get('https://fategrandorder.fandom.com/wiki/'+url)
    print(url)
    soup = BeautifulSoup(html_text.text,'lxml')

    #retriving stats
    servantinfo = soup.find('div',class_="ServantInfoStatsWrapper")
    servantdic = {}
    for line in servantinfo.text.splitlines():
        if line != '' and 'Japanese Name:' not in line and 'Hits' not in line:
            arr = line.split(':')
            try: 
                servantdic.update({arr[0].strip():arr[1].strip()})
            except:
                print('exception occured')
                continue
    servantlist = {int(servantdic["ID"]):servantdic}
    #retriving art
    servantart = soup.find_all('img',class_='pi-image-thumbnail')
    art = []
    for element in servantart:
        art.append(element['src'])
    servantlist[int(servantdic["ID"])]['art'] = art


    #retriving skills
    AllSkills = {}
    skills= []
    skills_html = soup.find('div',class_='tabber wds-tabber')
    filteredskills = skills_html.text.replace('Level\n\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10','').splitlines()[2:]

    for line in filteredskills:
        if line !='':
            skills.append(line.strip())
    i=0
    skill_num = 1
    for skill in skills:
        if 'Available from' in skill or 'Unlocks after' in skill:
            AllSkills[skill_num] = GetSkill(skills[i:])
            skill_num = skill_num + 1
        if 'Upgrades after' in skill:
            AllSkills[skill_num-1].append(GetSkill(skills[i:]))
        i = i+1

    servantlist[int(servantdic["ID"])]['skills'] = AllSkills
    
    #getting noble phantasms
    if url == 'Beast_IV':
        servantlist[int(servantdic["ID"])]['NP'] = 'None'
        return servantlist
        
    np = soup.find('h2',text ='Noble Phantasm').find_next('div',class_='tabber wds-tabber')
    np_name = np.caption.b.text
    np_ftext = np.caption.b.find_next('b').text
    np_text = {'name':np_name,'ftext':np_ftext}
    np_info = []
    for text in np.text.splitlines():
        if text != '':
            np_info.append(text.strip())
    if 'Old' in np_info[len(np_info)-1] or 'Costume' in np_info[len(np_info)-1] or 'Stage' in np_info[len(np_info)-1]:
        np_info.pop()
    np_text.update(npformat(np_info))    
        
    servantlist[int(servantdic["ID"])]['NP'] =np_text
    return servantlist


def GetList():
    html_text = requests.get('https://fategrandorder.fandom.com/wiki/Servant_List_by_ID#1_~_100')
    soup = BeautifulSoup(html_text.text,'lxml')
    soup.prettify()

    page = soup.find('div', class_="tabber wds-tabber")
    table = page.find('tbody')

    links = page.find_all('a',href=True)
    output = ''
    for servant in links:
        if servant != '':
            output += servant.text.strip() +'\n'
    output = output.replace(" ","_").replace('Edit','')[40:]
    output = output.replace('\n\n','\n').replace('\n\n','\n').splitlines()
    return output


ServantList = GetList()
completelist = {}
i=1
for servant in ServantList:
    if servant == 'Hyde': #hyde has two entries so we skip one, both link to the same page
        continue
    if servant == 'Solomon' and i==152:
        servant = 'Solomon_(True)'
    completelist.update(GetServant(servant))
    try:
        completelist[i]['AKA'] = completelist[i]['AKA'] + ", "+ servant.replace('_',' ')
    except:
        completelist[i]['AKA'] = servant.replace('_',' ')
    i = i + 1
with open('.\\Data\\Data.json','w') as file:
    json.dump(completelist,file,indent = 4)