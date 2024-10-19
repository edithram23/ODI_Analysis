from googlenewsdecoder import new_decoderv1

def main():

    interval_time = 5 # default interval is 1 sec, if not specified

    source_url = "https://news.google.com/read/CBMiqAFBVV95cUxOanBlS2NIZkJEMzk1LWVqUkFHUzJmeVdSaEN0YS1HRThISXJlSC02TWZ4TGlJa2xscVJmdnlzTVNWTGNHQS1ydmViSWVUUjNOYWxUd3pMLVg1cGw0aTI3SzFOX1dPalhMclNaQWZTMFlybEd3amo1S1U4RjZsMk9wbl8xRnZTSmpWeTdxU3pSLXcweHQzMmRiUzQwOHNDV1cxb29rZ1lJZVc?hl=en-IN&gl=IN&ceid=IN%3Aen"

    try:
        decoded_url = new_decoderv1(source_url, interval=interval_time)
        if decoded_url.get("status"):
            print("Decoded URL:", decoded_url["decoded_url"])
        else:
            print("Error:", decoded_url["message"])
    except Exception as e:
        print(f"Error occurred: {e}")

    # Output: decoded_urls - [{'status': True, 'decoded_url': 'https://healthdatamanagement.com/articles/empowering-the-quintuple-aim-embracing-an-essential-architecture/'}]

if __name__ == "__main__":
    main()