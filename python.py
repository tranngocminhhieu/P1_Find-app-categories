# Result header in Console
def header(header_text,enter_before=False):
    if enter_before:
        print('\n')
    print('----------------------------')
    print(header_text)
    print('----------------------------')

# Convert CSV to List of Lists
from csv import reader
def csv_to_list_of_lists(file_path):
    open_file = open(file_path)
    read_file = reader(open_file)
    return list(read_file)

android_full = csv_to_list_of_lists('googleplaystore.csv')
android_header = android_full[0]
android = android_full[1:] #

ios_full = csv_to_list_of_lists('AppleStore.csv')
ios_header = ios_full[0]
ios = ios_full[1:]

# Explore dataset
def explore_dataset(dataset,start_index=0,end_index=3):
    for row in dataset[start_index:end_index]:
        print(row)
    print('Number of rows:',len(dataset))
    print('Number of columns:',len(dataset[0]))

header('Explore Android Dataset')
print(android_header)
print('\n')
explore_dataset(android)

header('Explore IOS Dataset')
print(ios_header)
print('\n')
explore_dataset(ios)

# Check wrong data
def check_wrong_data(dataset,data_header):
    for row in dataset:
        if len(row) != len(data_header):
            print(dataset.index(row))
            print(row)

header('Check wrong data Android')
check_wrong_data(android,android_header)
header('Check wrong data IOS')
check_wrong_data(ios,ios_header)

# Delete wrong data 10472
print('Before deteting the wrong data:',len(android))
del android[10472]
print('After deleting the wrong data:',len(android))

# Check dulicate data
def check_dulicate_data(dataset):
    data_unique = []
    data_duplicate = []

    for row in dataset:
        if row[0] not in data_unique:
            data_unique.append(row[0])
        else:
            data_duplicate.append(row[0])

    data_duplicate = sorted(data_duplicate)
    for i in data_duplicate[0:20]:
        print(i)
    print('--> Duplicate:', len(data_duplicate))

header('Check dulicate data Android')
check_dulicate_data(android)
header('Check dulicate data IOS')
check_dulicate_data(ios)

# View duplicate data
for row in android:
    if row[0] == '8 Ball Pool':
        print(row)

# Remove duplicate data
android_review_max = {}
for row in android:
    app_name = row[0]
    app_review = float(row[3])
    if app_name in android_review_max and app_review > android_review_max[app_name]:
        android_review_max[app_name] = app_review
    elif app_name not in android_review_max: # Use elif to avoid app_name not in android_review_max but app_review < android_review_max[app_name]
        android_review_max[app_name] = app_review

android_unique = []
android_name_added = []
for row in android:
    app_name = row[0]
    app_review = float(row[3])
    if app_name not in android_name_added and app_review == android_review_max[app_name]:
        android_unique.append(row)
        android_name_added.append(app_name)

print('Android review max:',len(android_review_max))
print('Android unique:',len(android_unique))

# Re-check 8 Ball Pool review 14201891
for row in android_unique:
    if row[0] == '8 Ball Pool':
        print(row)


# Check English name
header('Check English name')
def is_english(app_name):
    for i in app_name:
        if ord(i) > 127:
            return False
    return True

print(is_english('Instachat 😜'))
print(is_english('Facebook'))
print(is_english('Official QR Code® Reader "Q"'))
print(is_english('RPG ブレイジング ソウルズ アクセレイト'))

# Check English name - allow 3 characters outside of ASCII
header('Check English name - allow 3 characters outside of ASCII')

def is_english(app_name):
    non_ascii = 0
    for i in app_name:
        if ord(i) > 127:
            non_ascii += 1
    if non_ascii > 3:
        return False
    else:
        return True

print(is_english('Instachat 😜'))
print(is_english('Facebook'))
print(is_english('Official QR Code® Reader "Q"'))
print(is_english('RPG ブレイジング ソウルズ アクセレイト'))

# Create English name list
android_english = []
ios_english = []

for row in android_unique:
    if is_english(row[0]):
        android_english.append(row)
for row in ios:
    if is_english(row[1]):
        ios_english.append(row)

header('Explore Android English')
explore_dataset(android_english)
header('Explore IOS English')
explore_dataset(ios_english)

# Create English Free list
android_english_free = []
ios_english_free = []

for row in android_english:
    if row[7] == '0':
        android_english_free.append(row)

for row in ios_english:
    if row[4] == '0.0':
        ios_english_free.append(row)

header('Explore Android English Free')
explore_dataset(android_english_free)
header('Explore IOS English Free')
explore_dataset(ios_english_free)

# Frequently Genres Dict
def freq_genres_dict(dataset,genres_index):
    freq_dict = {}
    total = 0
    for row in dataset:
        app_genres = row[genres_index]
        total += 1
        if app_genres in freq_dict:
            freq_dict[app_genres] += 1
        else:
            freq_dict[app_genres] = 1
    for key in freq_dict:
        freq_dict[key] = (freq_dict[key] / total)*100
    return freq_dict

def display_dict_table(data_dict,desc=True):
    data_list_of_tupe = []
    for key in data_dict:
        dict_to_tupe = (data_dict[key],key)
        data_list_of_tupe.append(dict_to_tupe)
    if desc:
        data_list_of_tupe = sorted(data_list_of_tupe,reverse=True)
    else:
        data_list_of_tupe = sorted(data_list_of_tupe)
    for i in data_list_of_tupe:
        print(i[1],":",i[0])

android_category = freq_genres_dict(android_english_free,1)
android_genres = freq_genres_dict(android_english_free,9)
ios_genres = freq_genres_dict(ios_english_free,11)

header('Frequently Genres IOS')
display_dict_table(ios_genres)
header('Frequently Category Android')
display_dict_table(android_category)
header('Frequently Genres Android')
display_dict_table(android_genres)

# Average Install on Google Play
header('Average Install on Google Play')
def avg_install_or_rating(genres_or_category_dict,dataset,genres_or_category_index,install_or_rating_index):
    avg_dict = {}
    for key in genres_or_category_dict:
        total_app = 0
        total_install = 0
        for row in dataset:
            genres_or_category = row[genres_or_category_index]
            install_or_rating = float(row[install_or_rating_index].replace('+', '').replace(',', ''))
            if genres_or_category == key:
                total_app += 1
                total_install += install_or_rating
        avg_install = total_install / total_app
        avg_dict[key] = avg_install
    return avg_dict

android_avg_install = avg_install_or_rating(android_category,android_english_free,1,5)
display_dict_table(android_avg_install)

# Distinct Value Installs
header('Distinct Value Installs')
## Dictinct
distinct_value_installs = freq_genres_dict(android_english_free,5)
## Prepare for High to Low Sorting
for key in distinct_value_installs:
    distinct_value_installs[key] = int(key.replace('+','').replace(',',''))

display_dict_table(distinct_value_installs)

# Prepare for Explore top android apps
apps_installs = []
for row in android_english_free:
    app_name = row[0]
    installs = int(row[5].replace('+', '').replace(',', ''))
    category = row[1]
    apps_installs.append([installs,app_name,category])
apps_installs = sorted(apps_installs,reverse=True)

def display_android_apps(category):
    header(category)
    total_high = 0
    total_middle = 0
    print('*** High Installs ***')
    for row in apps_installs:
        if row[2] == category and row[0] >= 100000000:
            total_high += 1
            print(row[0],':',row[1])
    print('Total high:', total_high)
    print('*** Middle Installs ***')
    for row in apps_installs:
        if row[2] == category and 5000000 <= row[0] <= 50000000:
            total_middle += 1
            print(row[0],':',row[1])
    print('Total middle:', total_middle)

display_android_apps('COMMUNICATION')

display_android_apps('VIDEO_PLAYERS')
display_android_apps('SOCIAL')
display_android_apps('PHOTOGRAPHY')
display_android_apps('PRODUCTIVITY')
display_android_apps('GAME')
display_android_apps('TRAVEL_AND_LOCAL')
display_android_apps('ENTERTAINMENT')
display_android_apps('TOOLS')
display_android_apps('NEWS_AND_MAGAZINES')
display_android_apps('BOOKS_AND_REFERENCE')

# Average Rating on App Store
header('Average Rating on App Store')
ios_avg_rating = avg_install_or_rating(ios_genres,ios_english_free,11,5)
display_dict_table(ios_avg_rating)

# Display IOS Apps
def display_ios_apps(genre_name):
    header(genre_name)
    ios_apps = []
    for row in ios_english_free:
        genre = row[11]
        rating = int(row[5])
        app_name = row[1]
        if genre == genre_name:
            ios_apps.append([rating,app_name,genre])
    ios_apps = sorted(ios_apps,reverse=True)
    for row in ios_apps:
        print(row[0],':',row[1])

display_ios_apps('Navigation')
display_ios_apps('Reference')
display_ios_apps('Social Networking')
display_ios_apps('Music')
display_ios_apps('Weather')
display_ios_apps('Book')
display_ios_apps('Food & Drink')
display_ios_apps('Finance')
display_ios_apps('Photo & Video')
display_ios_apps('Travel')