import wget, os, time
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Check if linux or windows
iswindows = os.name == "nt"
if iswindows:
    dl_link = "https://www.dropbox.com/s/bpyws3nasiqnfbu/ffmpeg.exe?dl=1"
else:
    dl_link = "https://www.dropbox.com/s/s83ui2fwmdfxuuj/ffmpeg?dl=1"

# Make Pretty
if iswindows:
    os.system("title 10 Hourifier by JJTV")

def download_binary():
    # Check if downloaded
    if iswindows:
        if os.path.isfile("bin/ffmpeg.exe"):
            if md5("bin/ffmpeg.exe") == "9874a725f05265513b104086ec939027":
                print("Binary already found... Skipping Download")
                return
            else:
                print("Corrupted File Found, deleting it and re-downloading")
                os.remove("bin/ffmpeg.exe")
    else:
        if os.path.isfile("bin/ffmpeg"):
            if md5("bin/ffmpeg") == "dfd7e86f5d128c56c38f7d2d224e6e80":
                print("Binary already found... Skipping Download")
                return
            else:
                print("Corrupted File Found, deleting it and re-downloading")
                os.remove("bin/ffmpeg")

    def dl_progress(current, total, width: None):
        print("\rDownloaded {} of {} bytes ({:.2f}%)".format(current, total, 100 * current / total), end="")
    if iswindows:
        print("Downloading Windows Binary...")
    else:
        print("Downloading Linux Binary...")
    os.makedirs("bin", exist_ok=True)
    wget.download(dl_link, bar=dl_progress, out="bin/")

def merge_videos(output_name):
    if iswindows:
        os.system(f'bin/ffmpeg.exe -f concat -safe 0 -i "temp" -c:v copy "{output_name}"')
    else:
        os.system("chmod +x bin/ffmpeg")
        time.sleep(0.5)
        os.system(f'bin/ffmpeg -f concat -safe 0 -i "temp" -c:v copy "{output_name}"')

if __name__ == "__main__":
    # Ask Questions
    input_video = input("Enter the first video file name (with ending): ")
    output_video = input("Enter the output video file name (without .mp4): ")
    output_video += ".mp4"
    loop_amount = int(input("How many times should the video loop?: "))
    # Download ffmpeg binary
    download_binary()
    # Create filelist
    with open("temp", "w") as filelist:
        for i in range(loop_amount-1):
            filelist.write(f"file '{input_video}'\n")
        filelist.write(f"file '{input_video}'")
    # Merge videos
    merge_videos(output_video)
    # Cleanup
    os.remove("temp")
    print("Done")