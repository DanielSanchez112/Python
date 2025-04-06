def generate_hashtag(s):
    hashtag = f"#{s.title().replace(" ","")}"
    if hashtag == "" or len(hashtag) >= 140:
        print("False")
        return False
    else:
        print(hashtag)
        return hashtag

generate_hashtag("code" + "                                                                                                                                                                           " + "wars")