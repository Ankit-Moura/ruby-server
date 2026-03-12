from flask import Flask, jsonify
import yt_dlp

app = Flask(__name__)

# List of songs to generate the feed
song_list = [
    "Blinding Lights The Weeknd",
    "Levitating Dua Lipa",
    "Peaches Justin Bieber",
    "Stay The Kid LAROI",
    "Save Your Tears The Weeknd",
]

# "Good 4 U Olivia Rodrigo",
#     "Montero Lil Nas X",
#     "Bad Habits Ed Sheeran",
#     "Kiss Me More Doja Cat",
#     "Industry Baby Lil Nas X"

def get_yt_data(song_name):
    ydl_opts = {"format": "bestaudio", "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
        video = info["entries"][0]
        return {
            "title": video.get("title"),
            "artist": song_name.replace(video.get("title"), "").strip(),
            "thumbnail": video.get("thumbnail"),
            "stream_url": video.get("url")
        }

@app.route("/feed")
def feed():
    feed_data = []
    for song in song_list:
        try:
            data = get_yt_data(song)
            feed_data.append(data)
        except Exception as e:
            print(f"Failed to fetch {song}: {e}")
    return jsonify(feed_data)

if __name__ == "__main__":
    app.run(debug=True)