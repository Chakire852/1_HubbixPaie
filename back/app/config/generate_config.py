import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section('BDSettings')
config_file.add_section('APILegifrance')
config_file.add_section('APPSettings')

# ADD SETTINGS TO SECTION
config_file.set('BDSettings', 'hostname', 'sql481.main-hosting.eu')
config_file.set('BDSettings', 'username', 'u680597973_dalexmuro')
config_file.set('BDSettings', 'password', 'X77HlxDx$')
config_file.set('BDSettings', 'database', 'u680597973_projectia3wa')
config_file.set('BDSettings', 'dbengine', 'mysql+pymysql')
config_file.set('BDSettings', 'port', '3306')

config_file.set('APILegifrance', 'hostApi', 'https://sandbox-api.piste.gouv.fr')
config_file.set('APILegifrance', 'urlToken', 'https://sandbox-oauth.piste.gouv.fr/api/oauth/token')
config_file.set('APILegifrance', 'urlBase', '/dila/legifrance-beta/lf-engine-app/')
config_file.set('APILegifrance', 'urlGetArticle', 'consult/getArticle')
config_file.set('APILegifrance', 'urlGetCode', 'consult/code')
config_file.set('APILegifrance', 'urlallcodes', 'list/code')
config_file.set('APILegifrance', 'urlMain', 'www.legifrance.gouv.fr')
config_file.set('APILegifrance', 'clientId', '43448424-f516-4c85-8d3f-e5e485a7fc00')
config_file.set('APILegifrance', 'clientSecret', 'c597166e-85d7-46c2-91e6-f7579ceda134')

config_file.set('APPSettings', 'doctemppath', './app/core/data/temp/last_document.json')
config_file.set('APPSettings', 'arttemppath', './app/core/data/temp/last_articles.pkl')
config_file.set('APPSettings', 'modelpath', './app/core/data/model.pkl')

# SAVE CONFIG FILE
with open(r'configurations.ini', 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print('Config file "configurations.ini" created')

# PRINT FILE CONTENT
read_file = open('configurations.ini', 'r')
content = read_file.read()
print('Content of the config file are:\n')
print(content)
read_file.flush()
read_file.close()