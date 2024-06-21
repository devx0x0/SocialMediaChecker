import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
import time
import concurrent.futures
import sys
import json

def check_username(platform, url_template, username, retries=3):
    url = url_template.format(username=username)
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return False, url  # Username is taken
            else:
                return True, url  # Username is available
        except (ConnectionError, Timeout) as e:
            time.sleep(2)  # Wait for 2 seconds before retrying
        except RequestException as e:
            return False, url
    return False, url

def get_platforms():
    platforms = {
        "GitHub": "https://github.com/{username}",
        "Twitter": "https://twitter.com/{username}",
        "Instagram": "https://www.instagram.com/{username}/",
        "Facebook": "https://www.facebook.com/{username}",
        "LinkedIn": "https://www.linkedin.com/in/{username}",
        "Pinterest": "https://www.pinterest.com/{username}",
        "Reddit": "https://www.reddit.com/user/{username}",
        "Tumblr": "https://{username}.tumblr.com",
        "Flickr": "https://www.flickr.com/people/{username}",
        "Vimeo": "https://vimeo.com/{username}",
        "Dailymotion": "https://www.dailymotion.com/{username}",
        "SoundCloud": "https://soundcloud.com/{username}",
        "Mixcloud": "https://www.mixcloud.com/{username}",
        "Twitch": "https://www.twitch.tv/{username}",
        "Kick": "https://www.kick.com/{username}",
        "YouTube": "https://www.youtube.com/{username}",
        "TikTok": "https://www.tiktok.com/@{username}",
        "Snapchat": "https://www.snapchat.com/add/{username}",
        "WhatsApp": "https://wa.me/{username}",
        "WeChat": "https://web.wechat.com/{username}",
        "QQ": "https://user.qzone.qq.com/{username}",
        "Telegram": "https://t.me/{username}",
        "Viber": "https://viber.com/{username}",
        "Line": "https://line.me/ti/p/{username}",
        "KakaoTalk": "https://story.kakao.com/{username}",
        "Discord": "https://discord.com/users/{username}",
        "Slack": "https://{username}.slack.com",
        "Medium": "https://medium.com/@{username}",
        "Quora": "https://www.quora.com/profile/{username}",
        "Blogger": "https://{username}.blogspot.com",
        "WordPress": "https://{username}.wordpress.com",
        "Dribbble": "https://dribbble.com/{username}",
        "Behance": "https://www.behance.net/{username}",
        "DeviantArt": "https://www.deviantart.com/{username}",
        "Goodreads": "https://www.goodreads.com/{username}",
        "Last.fm": "https://www.last.fm/user/{username}",
        "Spotify": "https://open.spotify.com/user/{username}",
        "Pandora": "https://www.pandora.com/profile/{username}",
        "Apple Music": "https://music.apple.com/profile/{username}",
        "Amazon Music": "https://music.amazon.com/users/{username}",
        "Google Play": "https://play.google.com/store/apps/details?id={username}",
        "Steam": "https://steamcommunity.com/id/{username}",
        "Origin": "https://www.origin.com/usa/en-us/profile/user/{username}",
        "Epic Games": "https://www.epicgames.com/id/{username}",
        "Battle.net": "https://battle.net/{username}",
        "Uplay": "https://uplay.ubisoft.com/{username}",
        "Itch.io": "https://{username}.itch.io",
        "Game Jolt": "https://gamejolt.com/@{username}",
        "VK": "https://vk.com/{username}",
        "Xing": "https://www.xing.com/profile/{username}",
        "Myspace": "https://myspace.com/{username}",
        "Badoo": "https://badoo.com/profile/{username}",
        "Tagged": "https://www.tagged.com/{username}",
        "MeetMe": "https://www.meetme.com/{username}",
        "Nextdoor": "https://nextdoor.com/profile/{username}",
        "Classmates": "https://www.classmates.com/profile/{username}",
        "ReverbNation": "https://www.reverbnation.com/{username}",
        "Ello": "https://ello.co/{username}",
        "Mastodon": "https://mastodon.social/@{username}",
        "Gab": "https://gab.com/{username}",
        "MeWe": "https://mewe.com/i/{username}",
        "WT.Social": "https://wt.social/{username}",
        "Rumble": "https://rumble.com/user/{username}",
        "Parler": "https://parler.com/profile/{username}",
        "CloutHub": "https://app.clouthub.com/profile/{username}",
        "Triller": "https://triller.co/{username}",
        "Byte": "https://byte.co/{username}",
        "Caffeine": "https://www.caffeine.tv/{username}",
        "Houseparty": "https://houseparty.com/{username}",
        "Peach": "https://peach.cool/{username}",
        "Periscope": "https://www.pscp.tv/{username}",
        "Clubhouse": "https://www.joinclubhouse.com/@{username}",
        "Diaspora": "https://diasporafoundation.org/u/{username}",
        "Friendica": "https://{username}.friendica.social",
        "GNU Social": "https://{username}.gnusocial.no",
        "Hubzilla": "https://{username}.hubzilla.org",
        "Twister": "https://twister.net.co/{username}",
        "Minds": "https://www.minds.com/{username}",
        "Steemit": "https://steemit.com/@{username}",
        "DTube": "https://d.tube/#!/c/{username}",
        "LBRY": "https://lbry.tv/@{username}",
        "BitChute": "https://www.bitchute.com/channel/{username}",
        "Odysee": "https://odysee.com/@{username}",
        "3Speak": "https://3speak.online/user/{username}",
        "DLive": "https://dlive.tv/{username}",
        "Theta.tv": "https://www.theta.tv/{username}",
        "Vero": "https://www.vero.co/{username}",
        "Pheed": "https://www.pheed.com/{username}",
        "Taringa": "https://www.taringa.net/{username}",
        "Skyrock": "https://{username}.skyrock.com",
        "Fotolog": "https://www.fotolog.com/{username}",
        "Plurk": "https://www.plurk.com/{username}",
        "Qzone": "https://user.qzone.qq.com/{username}",
        "Renren": "https://www.renren.com/{username}",
        "Mixi": "https://mixi.jp/show_profile.pl?id={username}",
        "Weibo": "https://www.weibo.com/{username}",
        "Douban": "https://www.douban.com/people/{username}",
        "BiliBili": "https://space.bilibili.com/{username}"
    }
    return platforms

def main():
    data = json.loads(sys.argv[1])
    username = data.get("username")
    website = data.get("website")
    results = []

    if website:
        # Manual search for a specific website
        exists, url = check_username('Custom Website', website + '/{username}', username)
        results.append({
            "platform": website,
            "exists": exists,
            "url": url
        })
    else:
        # Check popular social media platforms
        platforms = get_platforms()

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(check_username, platform, url_template, username): platform for platform, url_template in platforms.items()}
            for future in concurrent.futures.as_completed(futures):
                platform = futures[future]
                try:
                    exists, url = future.result()
                    results.append({
                        "platform": platform,
                        "exists": exists,
                        "url": url
                    })
                except Exception as e:
                    results.append({
                        "platform": platform,
                        "exists": False,
                        "url": "",
                        "error": str(e)
                    })

    print(json.dumps(results))

if __name__ == "__main__":
    main()