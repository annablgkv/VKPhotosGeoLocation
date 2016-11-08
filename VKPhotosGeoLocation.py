import vk
import time

print('VK photos geo location')

session = vk.Session('946ce0a39cf1da32961f78d543da9cdbb3eaac63f71aece66d5447df64dbd3d7e9e0d6c99296ef676341a')
api = vk.API(session)
friends = api.friends.get()
js_code=""

friends = api.friends.get()
friends_info = api.users.get(user_ids=friends)

try:
    for friend in friends_info:
        print ('ID: %s Имя %s %s'% (friend['uid'], friend ['last_name'],friend['first_name']))
    geolocation = []
    for id in friends:
        try:
             print('Получаем данные пользователья: %s'%id)
             albums = api.photos.getAlbums(owner_id=id)
             print('\t...альбомов %s...'% len(albums))
             for album in albums:
                 try:
                     photos = api.photos.get(owner_id=id, album_id=album['aid'])
                     print('\t\t...обрабатываем фотографии альбома...')
                     for photo in photos:
                         if 'lat' in photo and 'long' in photo:
                             geolocation.append((photo['lat'],photo['long']))
                     print('\t\t...найдено %s фото...' % len(photos))
                 except:
                     pass
                 time.sleep(0.5)
             time.sleep(0.5)
        except:
            print('BLOCK')
            pass
except:
    pass
for loc in geolocation:
    js_code += 'new google.maps.Marker({position: {lat: %s, lng: %s}, map: map});\n' % (loc[0], loc[1])
html = open('map.html').read()
html = html.replace('/* PLACEHOLDER */', js_code)

f = open('VKPhotosGeoLocation.html', 'w')
f.write(html)
f.close()