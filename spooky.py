import random
import asyncio
import sys
import time
import os
import cv2
import random
import platform



#alexander ____________________________

def randomImage():
    image_directory = os.path.join('', "images/")
    images = [os.path.join(image_directory, img) for img in os.listdir(image_directory) if img.endswith(('.png', '.jpg', '.jpeg', '.webp'))]


    random_image_path = random.choice(images)
    image = cv2.imread(random_image_path)
    cv2.imshow("Random Image Popup", image)
    if cv2.waitKey(2000) == 27:  # Show image for 2 seconds or until 'Esc' is pressed
        pass
    cv2.destroyAllWindows()


def list_documents_directory():
    # Path to the Documents directory
    documents_path = os.path.join(os.environ["USERPROFILE"], "OneDrive\Documents")
    
    # List to hold names of files and folders
    items_list = []

    # Walk through the directory
    for item in os.listdir(documents_path):
        items_list.append(item)

    for item in items_list:
        print("Deleting: " + item)
        time.sleep(0.5)  # Adjust the time delay as needed

    print("\nAll " + str(len(items_list)) + " files have been successfully deleted. Thanks for playing! Happy Halloween!")

#_____________________________________________________________________________________________________________
#game


async def countdown(stop_event, round_event):
    # Countdown timer, resets each round
    for remaining_time in range(5, 0, -1):
        if stop_event.is_set() or round_event.is_set():  # Check if we should stop or reset the countdown
            break
        print(f"Time left: {remaining_time} seconds", end="\r")
        await asyncio.sleep(1)
    
    # If countdown reaches 0 without being reset, stop the game
    if not round_event.is_set() and not stop_event.is_set():
        stop_event.set()  # Signal to stop the game if time is up

async def get_input(stop_event, round_event, random_char):
    # Prompt the user for input and read a single character
    user_input = await asyncio.to_thread(sys.stdin.readline)  # Reads input asynchronously
    user_input = user_input.strip()
    
    if user_input == random_char:
        print("Correct! Moving to the next round.")
        round_event.set()  # Signal to reset the timer
    else:
        print("Wrong character.")
        stop_event.set()  # Stop the game if the wrong character is entered

async def typing_game():
    count = 0
    while True:
        # Generate a random character for the round
        random_char = chr(random.randint(97, 122))  # ASCII values for lowercase letters (a-z)
        print(f"\nType the character: '{random_char}'")

        # Event to signal stopping the countdown and stopping the round
        stop_event = asyncio.Event()
        round_event = asyncio.Event()

        # Run countdown and input checker concurrently
        countdown_task = asyncio.create_task(countdown(stop_event, round_event))
        input_task = asyncio.create_task(get_input(stop_event, round_event, random_char))

        # Wait for either task to finish
        await asyncio.wait([countdown_task, input_task], return_when=asyncio.FIRST_COMPLETED)
        count+=1
        if count ==3:
            randomImage()
         # Check if the round should reset or the game should stop
        if stop_event.is_set():  # Game ends
            print("\nGame Over!\n")
            list_documents_directory()
            break
        elif round_event.is_set():  # Correct input, reset round
            countdown_task.cancel()  # Cancel the countdown task immediately
            try:
                await countdown_task  # Attempt to await to clear the task completely
            except asyncio.CancelledError:
                pass  # Ignore the cancellation error
            round_event.clear()  # Reset the event for the next round
print('do my minigame or i will delete all your files!!!!!!')
time.sleep(3)
print("Type the character and press Enter: ")
# Run the game
asyncio.run(typing_game())
