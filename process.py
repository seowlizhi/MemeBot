import requests
import random
import formatResponse
import editImage
import videoMaker
import os
import glob
import notifBot

def make(subreddit, meme_count, iteration):
  try:
      # Getting response from API
    memeList = []
    resp = requests.get(url+subreddit+"/"+str(meme_count)).json()
    print("Subreddit: ",subreddit)
    memeList = formatResponse.makeMemeList(resp)
  except:
    resp.status_code == 200
    print("Request Error.")
  finally:
    # Calling formatResponse 
    print("Raw Data:\n")
    print(memeList)
    print("\n")


  #Clearing all the old photos in the process folder
  files = glob.glob('processed/*')
  for f in files:
      os.remove(f)


  try:
    #Reformat Image using editImage
    editImage.Reformat_Image(memeList)

  except:
    print("Failed to reformat.")
  finally:
    print("Done!")

  videoMaker.makeVidFromImgSequence(memeList,iteration)

  print("Video is done!")



if __name__ == '__main__':
  url = "https://meme-api.herokuapp.com/gimme/"

  meme_count = 10
  subreddit_count = 4

  # og_subreddits = ["memes","dankmemes","cursedcomments","me_irl","HistoryMemes","BlackPeopleTwitter","ihadastroke","technicallythetruth","trippinthroughtime","starterpacks","2meirl4meirl","deepfriedmeme","Meanjokes","suicidebywords","madlads"] Not accessible until protest is over
  subreddits =  ["animememes","goodanimemes","AOTmemes","animemes","attackontitanmemes","JoJoMemes","ShitPostCrusaders", "dankruto", "narutomemes"]

  # shuffle so can choose between which one
  random.shuffle(subreddits)


  for i in range(subreddit_count):
    # clear previous videos
    if i == 0:
      files = glob.glob('processVids/*')
      for f in files:
        os.remove(f)

    print("\n Video #",i)
    make(subreddits[i], meme_count, i)
    
  
  # Export Video
  try:
    print("Combining all the clips")
    videoMaker.combineVideos()
    print("Video Completed!")
    notifBot.send("Video Completed, Uploading to Youtube!")
  
  except:
    notifBot.send("Some error occured while exporting and uploading the video!")
