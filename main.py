import random
import string
import time
import os
from instaloader import Instaloader, Profile


def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def like_followers_posts(your_username, your_password, target_profile, num_bots=10, initial_delay=60):
    L = Instaloader()
    session_filename = f"{your_username}.session"

    if os.path.exists(session_filename):
        try:
            L.load_session_from_file(your_username)
            if not L.context.is_logged_in:
                L.context.log("Session load failed - Logging in...")
                L.login(your_username, your_password)
        except Exception as e:
            L.context.log(f"Error loading session from file: {e}")
            return
    else:
        try:
            L.login(your_username, your_password)
        except Exception as e:
            L.context.log(f"Error logging in: {e}")
            return

    delay = initial_delay
    max_delay = 7200  # Maximum delay of 2 hours
    min_delay = 60  # Minimum delay of 1 minute

    try:
        profile = Profile.from_username(L.context, target_profile)
        followers = list(profile.get_followers())
        L.context.log(f"Retrieved {len(followers)} followers from {target_profile}")
        if not followers:
            L.context.log("No followers to engage with.")
            return

        for i in range(num_bots):
            try:
                target_follower = random.choice(followers)
                L.download_profile(target_follower, profile_pic_only=True)
                L.context.log(f"Successfully downloaded profile pic of {target_follower.username}")
            except Exception as e:
                L.context.log(f"Failed to download profile pic of follower: {e}")

            random_delay = random.randint(min_delay, delay)
            L.context.log(f"Sleeping for {random_delay} seconds before next operation.")
            time.sleep(random_delay)
    except Exception as e:
        L.context.log(f"Failed to fetch followers: {e}")


if __name__ == "__main__":
    your_username = "thatcoder2024"  # Replace with your Instagram username
    your_password = "pyt123"  # Replace with your Instagram password
    target_profile = "curious_coder3"  # Replace with the username of the profile whose followers you want to target
    like_followers_posts(your_username, your_password, target_profile, num_bots=10, initial_delay=60)
