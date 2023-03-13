import openai
import threading
import os
from file_cache_manager import StringCache, DEFAULT_CACHE_FILE_NAME

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set up the OpenAI model to use for generating descriptions
model_engine = "text-davinci-002"

def generate_descriptions(strings, cache_file):
    # Create a StringCache object to cache the descriptions
    cache = StringCache(cache_file)

    # Create a list to hold the threads we'll create
    threads = []

    # Define a function that will be run in each thread
    def generate_description(string):
        # Check if we already have a description for this string in the cache
        description = cache.get(string)

        # If not, generate a description using the OpenAI API
        if not description:
            prompt = f"Generate a short description for '{string}'"
            response = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=64,
                n=1,
                stop=None,
                temperature=0.5,
            )
            description = response.choices[0].text.strip()

            # Add the description to the cache
            cache.set(string, description)

        print(f"{string}: {description}")

    # Create a thread for each string
    for string in strings:
        t = threading.Thread(target=generate_description, args=(string,))
        threads.append(t)

    # Start all the threads
    for t in threads:
        t.start()

    # Wait for all the threads to finish
    for t in threads:
        t.join()

    # Save the cache to file
    cache.save_cache()

if __name__ == "__main__":
    # TODO(cleanup): This file name cleaning is duplicated in main.py
    strings = [image_file[:-4].replace("-", " ") for image_file in os.listdir("images/")]

    # Generate descriptions for each string and print the result
    generate_descriptions(strings, DEFAULT_CACHE_FILE_NAME)