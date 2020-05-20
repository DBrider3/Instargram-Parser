import requests
import json
import os

ENDPOINT_URL = "https://www.instagram.com/"
TARGET_ID = input("아이디를 입력하세요: ")
TO_JSON_STR = "/?__a=1"


# Paste your cookie of instagram.
# NOTE THAT You should login first before you paste the cookie in this script.
headers = {}

url = ENDPOINT_URL + TARGET_ID + TO_JSON_STR
r = requests.get(url, headers=headers)

# Get target's information first.
data = json.loads(r.text)
posts = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
post_count = data["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
target_uid = data["graphql"]["user"]['id']

print("[*] Target UID : " + str(target_uid))
print("[*] Total post counts : " + str(post_count))

# Get target's posts
post_code_list = []

end_cursor = ""	
idx = 0
while 1:
	url = "https://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables="
	variables = '{"id":"%s","first":50,"after":"%s"}' % (target_uid, end_cursor)
	url = url + variables
	r = requests.get(url, headers=headers)

	data = json.loads(r.text)

	next_after = data["data"]['user']["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
	posts = data["data"]['user']["edge_owner_to_timeline_media"]["edges"]

	for post in posts:
		shortcode = post["node"]["shortcode"]
		post_code_list.append(shortcode)

	end_cursor = next_after
	# If last post,
	if end_cursor == None:
		break




#basic URL setting
ENDPOINT_URL = "https://www.instagram.com/p/" 

TO_JSON_STR = "/?__a=1"

headers = {}

#배열에 저장되어있는 shortcode를 이용해 게시글마다 돕니다.
for post_code in post_code_list:
        url = ENDPOINT_URL + post_code + TO_JSON_STR 
        r = requests.get(url, headers=headers)

        data = json.loads(r.text)

        jogun_multi =  data["graphql"]["shortcode_media"] #조건을 이용해 사진,동영상이 멀티인지 싱글인지 구별해줍니다.
        if "edge_sidecar_to_children" in jogun_multi:

                jogun_display =  data["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"][0]["node"]["display_url"]
                
                jogun_video = data["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"][0]["node"]
                cnt = len(data["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"])
                #node 배열을 위해 반복돌려주기
                for i in range(0,cnt):
                        if "https://" in jogun_display:
                                        #보니까 동영상동영상 사진 이런순이있을수있으니 예외처리 해줍니당.
                                        try: 
                                                multi_image_posts = data["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"][i]["node"]["display_url"] #display_url이면 변수에 값 저장후 출력
                                                print(multi_image_posts)

                                                r = requests.get(multi_image_posts).content # get방식으로 요청
                                                r2 = multi_image_posts.split('/') 
                                                name = r2[-1].split('?')
                                                print(name) #split 을 이용해 url에서 원값 이름 name에 저장

                                                #파일 저장
                                                f = open("C:/Users/tmdgn/Desktop/HellCamp/instagram_pasing/instapaser/images/"+str(name[0]),'wb')
                                                f.write(r)
                                                f.close()
                                        
                                        except:
                                                pass

                        if "video_url" in jogun_video:
                                        #보니까 동영상동영상 사진 이런순이있을수있으니 예외처리 해줍니당.
                                        try:
                                                multi_video_posts = data["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"][i]["node"]["video_url"] #video_url이면 변수에 값 저장후 출력 
                                                print(multi_video_posts)
                                                
                                                r = requests.get(multi_video_posts).content # get방식으로 요청
                                                r2 = multi_video_posts.split('/')
                                                name = r2[-1].split('?') #split 을 이용해 url에서 원값 이름 name에 저장

                                                #파일 저장
                                                f = open("C:/Users/tmdgn/Desktop/HellCamp/instagram_pasing/instapaser/images/"+str(name[0]),'wb')
                                                f.write(r)
                                                f.close()
                                        except:
                                                pass

        else: #위와 동일하게 싱글일 경우 
                jogun_video = data["graphql"]["shortcode_media"]
                if "video_url" in jogun_video:
                        viedo_posts = data["graphql"]["shortcode_media"]["video_url"]
                        print(viedo_posts)

                        r = requests.get(viedo_posts).content # get방식으로 요청
                        r2 = viedo_posts.split('/')
                        name = r2[-1].split('?') #split 을 이용해 url에서 원값 이름 name에 저장
                        
                        #파일 저장
                        f = open("C:/Users/tmdgn/Desktop/HellCamp/instagram_pasing/instapaser/images/"+str(name[0]),'wb')
                        f.write(r)
                        f.close()

                else:
                       image_posts = data["graphql"]["shortcode_media"]["display_url"]
                       print(image_posts)

                       r = requests.get(image_posts).content # get방식으로 요청
                       r2 = image_posts.split('/')
                       name = r2[-1].split('?') #split 을 이용해 url에서 원값 이름 name에 저장
                       
                       #파일 저장
                       f = open("C:/Users/tmdgn/Desktop/HellCamp/instagram_pasing/instapaser/images/"+str(name[0]),'wb')
                       f.write(r)
                       f.close()
        
        #피드 text도 불러주고싶어서 조건!
        arr_jogun = data["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"] 

        #피드에 text가 없는 경우도 존재하기에 조건분기문
        if len(arr_jogun) > 0:
                write_posts = data["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"]       
                print(write_posts)
        else:
                print("text empty")
                
print("[*] post list count " + str(len(post_code_list))) #마무리 총 갯수 끝남을 의미        

        
        



