from openai import OpenAI

openai_client = None

GPT_35 = 'gpt-3.5-turbo-1106'
GPT_4 = 'gpt-4-1106-preview'

DEFAULT_SYSTEM_PROMPT = "You are an expert musician and composer who is well-versed in every genre and style of music."


def authenticate_openai(api_key):
    global openai_client
    openai_client = OpenAI(api_key=api_key)

# TODO: implement query caching to reduce testing costs
def get_llm_completion(prompt, system_prompt=DEFAULT_SYSTEM_PROMPT, model=GPT_35):
    completion = openai_client.chat.completions.create(model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ])
    print(prompt)
    print(completion.choices[0].message.content)
    print()
    return completion.choices[0].message.content


def get_playlist_description(playlist_str):
    prompt = '\n'.join([
        "Write a highly informative and detailed description of the playlist below. Make sure to include the following sections:",
        "1. A summary of the playlist's characteristics:",
        "     - genres",
        "     - artists",
        "     - instruments",
        "     - mood",
        "     - atmosphere",
        "     - common themes",
        "     - any other characteristics which could help decide if a particular track should be added to the playlist",
        "2. A list of a dozen or so of the most representative tracks in the playlist",
        "3. A qualitative and extensive description of the types of tracks that would work well in the playlist",
        "4. A qualitative and extensive description of the types of tracks that would not work well in the playlist",
        "",
        "Here is the playlist info:",
        playlist_str,
    ])
    return get_llm_completion(prompt)


def get_track_description(track_str):
    prompt = '\n'.join([
        "Write a highly informative and detailed description of the track below. Make sure to include the following sections:",
        "1. A summary of the track's characteristics:",
        "     - genres",
        "     - artist",
        "     - instruments",
        "     - mood",
        "     - atmosphere",
        "     - any other characteristics which could help decide its compatability with the playlist",
        "2. A description of the types of playlists this track would go well in.",
        "3. A description of the types of playlists that this track would not go well in.",
        "",
        "Here is the track info:",
        track_str,
    ])
    return get_llm_completion(prompt)


# TODO: parse LLM output to get score then return dict {'score': score, 'reasoning': reasoning}
def evaluate_playlist_fit(playlist_description, track_description):
    prompt = '\n'.join([
        "You're tasked with evaluating how well a specific track fits into a given playlist. Consider the playlist's overall themes, mood, genres, and any distinctive characteristics. Then, assess the track's compatibility with the playlist. Provide a score on a scale from 0 to 2, where:",
        "0 = Bad Fit (the track significantly diverges from the playlist's theme or mood)",
        "1 = Borderline Fit (the track mostly aligns with the playlist's theme but has some major divergences)",
        "2 = Good Fit (the track aligns with the playlist's theme but may have some minor divergences)",
        "3 = Excellent Fit (the track aligns perfectly with the playlist's theme and enhances its overall mood and style).",
        "Below are examples to illustrate these scores. Notice that the reasoning is not limited to fixed criteria but also embraces the playlist's unique character and the track's individual qualities.",
        "",
        "<examples>",
        "<score 3>",
        "Playlist Description: High-energy workout songs featuring electronic and pop hits.",
        "Track Info: 'Titanium' by David Guetta featuring Sia.",
        "Reasoning: The song's energetic and uplifting tempo aligns perfectly with the workout theme, and its blend of electronic and pop fits the playlist's genre.",
        "Score: 3",
        "",
        "Playlist Description: Classic jazz tracks from the 50s and 60s.",
        "Track Info: 'Take Five' by Dave Brubeck.",
        "Reasoning: This iconic jazz piece captures the essence of the 50s and 60s jazz era, matching the playlist's theme and mood.",
        "Score: 3",
        "</score 3>",
        "<score 2>",
        "Playlist Description: Indie folk music for a relaxed evening.",
        "Track Info: 'Holocene' by Bon Iver.",
        "Reasoning: The song's serene mood fits the relaxed theme, though its experimental sound is a slight divergence from traditional indie folk.",
        "Score: 2",
        "",
        "Playlist Description: 80s pop and rock hits.",
        "Track Info: 'Every Breath You Take' by The Police.",
        "Reasoning: As an 80s hit, it fits the era, but its slower tempo slightly contrasts with the generally upbeat nature of the playlist.",
        "Score: 2",
        "</score 2>",
        "<score 1>",
        "Playlist Description: Upbeat summer hits.",
        "Track Info: 'Malibu' by Miley Cyrus.",
        "Reasoning: The song has a summery feel but leans more towards a mellow mood, diverging from the typically high-energy summer hits.",
        "Score: 1",
        "",
        "Playlist Description: Hard rock classics.",
        "Track Info: 'Another One Bites the Dust' by Queen.",
        "Reasoning: While Queen is a staple in rock, this particular track has a funk edge that doesn't fully align with the hard rock theme.",
        "Score: 1",
        "</score 1>",
        "<score 0>",
        "Playlist Description: Calming classical music for studying.",
        "Track Info: 'Thunderstruck' by AC/DC.",
        "Reasoning: The loud and energetic nature of 'Thunderstruck' is in direct opposition to the calming and focus-oriented nature of a classical study playlist.",
        "Score: 0",
        "",
        "Playlist Description: Romantic ballads.",
        "Track Info: 'Smells Like Teen Spirit' by Nirvana.",
        "Reasoning: The grunge style and rebellious tone of 'Smells Like Teen Spirit' sharply contrast with the gentle, romantic theme of ballads.",
        "Score: 0",
        "</score 0>",
        "</examples>",
        "",
        "Now, evaluate the following track for the provided playlist description:",
        f"Playlist Description: {playlist_description}",
        f"Track Description: {track_description}",
    ])
    return get_llm_completion(prompt)