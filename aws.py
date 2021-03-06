#!/usr/bin/env python3
import sys, os, time, menugenerator as menu, boto3, botocore
debug = 1
menu = menu.menu
size = sys.stdout

# menu declerations
mainMenu = ['AWS Functions', 'Setup', 'Exit']
awsMenu = ['S3','Exit']
s3Menu = ['Modify or View Files', 'Modify or View Buckets']
bucketsMenu = ['List All Buckets', 'Initialise a New Bucket','Delete Bucket', 'Check the Status of a Bucket']
s3sub = ['View Files', 'Upload Files', 'Download File', 'Delete File']
uploadMenu = ['Single File Upload', 'Multi-File Upload']


s3 = boto3.resource('s3')

# intro "animation" and ASCII art
def asciiArt():
    print("\n      __          _______   _____       _   _                 ")
    print("     /\ \        / / ____| |  __ \     | | | |                ")
    print("    /  \ \  /\  / / (___   | |__) |   _| |_| |__   ___  _ __  ")
    print("   / /\ \ \/  \/ / \___ \  |  ___/ | | | __| '_ \ / _ \| '_ \ ")
    print("  / ____ \  /\  /  ____) | | |   | |_| | |_| | | | (_) | | | |")
    print(" /_/    \_\/  \/  |_____/  |_|    \__, |\__|_| |_|\___/|_| |_|")
    print(" (S3 Functionality Only)           __/ |                      ")
    print("Written by Tom Hulbert            |___/                   V0.2")

# Thanks to Active State user Barry Walker for assistance with window sizing
size.write("\x1b[8;{rows};{cols}t".format(rows=28, cols=150))

menu.clearScreen()
asciiArt()
if not debug:
    time.sleep(3)
while True:
    menu.clearScreen()
    print("For first time users select 'Setup'")
    if debug:
        print("Debug is enabled")
    main = menu.generate('\nMain Menu', 0, 0, *mainMenu)
    if main == 1:  # AWS Functions
        submain1 = menu.generate('AWS Functions', 1, 1, *awsMenu)
        if submain1 == 1:  # S3 Functions
            menu.clearScreen()
            s3main = menu.generate('S3 Functions', 1, 1, *s3Menu)
            if s3main == 1:
                s3Sub = menu.generate('Upload or Download Files', 1, 1, *s3sub)
                if s3Sub == 1:
                    menu.clearScreen()
                    print("View Files\n")
                    for bucket in s3.buckets.all():
                        print("\n" + bucket.name + ":")
                        for key in bucket.objects.all():
                            print(key.key)
                    input("Press enter to continue...")
                if s3Sub == 2:
                    filesub = menu.generate('Upload Files', 1, 1, *uploadMenu)
                    if filesub == 1:
                        menu.clearScreen()
                        print("Single File Upload")
                        print("\nAvailable Buckets:")
                        for bucket in s3.buckets.all():
                            print(bucket.name)
                        bucketName = input("\nBucket to Upload to: ")
                        file = open(input("Full Address of File: "), 'rb')
                        try:
                            s3.Object(bucketName, os.path.basename(file.name)).put(Body=file)
                            print("Successfully Uploaded File " + os.path.basename(file.name) + " to " + bucketName)
                            file.close()
                        except Exception as e:
                            menu.clearScreen()
                            print(e)
                            print("An error has occured, please try again later...")
                            if debug:
                                input()
                                time.sleep(2)
                    if filesub == 2:
                        menu.clearScreen()
                        print("Multi-File Upload")
                        print("\nAvailable Buckets:")
                        for bucket in s3.buckets.all():
                            print(bucket.name)
                        bucketName = input("\nBucket to Upload to: ")
                        print("To finish file selection press enter.")
                        pendinguploads = []
                        while True:
                            file = input("Full Address of File: ")
                            if file == "":
                                break
                            pendinguploads.append(file)
                        #TODO: setup up multi threading for background upload
                        for file in pendinguploads:
                            try:
                                openfile = open(file, 'rb')
                                s3.Object(bucketName, os.path.basename(openfile.name)).put(Body=openfile)
                            except Exception as e:
                                print(e)
                                input()
                        print("Successfully Uploaded Files to " + bucketName)
                        time.sleep(2)
                if s3Sub == 3:
                    menu.clearScreen()
                    print("Download File")
                    print("\nAvailable Buckets and Files:")
                    for bucket in s3.buckets.all():
                        print("\n" + bucket.name + ":")
                        for key in bucket.objects.all():
                            print(key.key)
                    bucketName = input("\nBucket to Download From: ")
                    file = input("Full Address of File: ")
                    try:
                        s3.Bucket(bucketName).download_file(file, '/downloads/' + file)
                        print("Successfully Downloaded File " + file)
                    except Exception as e:
                        menu.clearScreen()
                        print(e)
                        print("An error has occured, please try again later...")
                        if debug:
                            input()
                    time.sleep(2)
                if s3Sub == 4:
                    menu.clearScreen()
                    print("Delete File")
                    print("\nAvailable Buckets and Files:")
                    for bucket in s3.buckets.all():
                        print("\n" + bucket.name + ":")
                        for key in bucket.objects.all():
                            print(key.key)
                    bucketName = input("\nBucket to Delete From: ")
                    file = input("Full Address of File: ")
                    if input("Are you sure you want to delete file " + file + "? [Y/N]: ") == 'Y' or 'y':
                        try:
                            s3.Object(bucketName, file).delete()
                            print("Successfully Deleted File " + file)
                        except Exception as e:
                            menu.clearScreen()
                            print(e)
                            print("An error has occured, please try again later...")
                            if debug:
                                input()
                    else:
                        print("File " + file + " has not been deleted.")
                    time.sleep(2)
            elif s3main == 2:
                bucketmain = menu.generate(
                    'Bucket Functions', 1, 1, *bucketsMenu)
                if bucketmain == 1:
                    menu.clearScreen()
                    for bucket in s3.buckets.all():
                        print(bucket.name)
                    input("Press Enter to continue...")
                elif bucketmain == 2:
                    menu.clearScreen()
                    print("Initialise a New Bucket")
                    print("\nPlease Note:\nThe name that you choose must be unique across all existing bucket names in Amazon S3.\nOne way to help ensure uniqueness is to prefix your bucket names with the name of your organization.\n")
                    bucketName = input("Enter Name For New Bucket: ")
                    try:
                        print("\nInitialising New Bucket as " + bucketName + "...")
                        s3.create_bucket(Bucket=bucketName)
                        print("New Bucket " + bucketName + " Initialised")
                    except Exception as e:
                        menu.clearScreen()
                        print(e)
                        print("Please Wait...")
                        if debug:
                            input()
                    time.sleep(5)
                elif bucketmain == 3:
                    menu.clearScreen()
                    print("Delete Bucket")
                    print("\nAvailable Buckets:")
                    for bucket in s3.buckets.all():
                        print(bucket.name)
                    bucketName = input("Name of Bucket: ")
                    if input("Are you sure you want to delete bucket " + bucketName + "? [Y/N]: ") == 'Y' or 'y':
                        bucket = s3.Bucket(bucketName)
                        print("Deleting keys in " + bucketName)
                        for key in bucket.objects.all():
                            key.delete()
                        bucket.delete()
                        print("Bucket " + bucketName + " has been deleted.")
                    else:
                        print("Bucket " + bucketName + " has not been deleted.")
                    time.sleep(1)
                    input("Press Enter to continue...")
                elif bucketmain == 4:
                    menu.clearScreen()
                    print("Check Bucket")
                    print("\nAvailable Buckets:")
                    for bucket in s3.buckets.all():
                        print(bucket.name)
                    bucketName = input("Bucket: ")
                    bucket = s3.Bucket(bucketName)
                    exists = True
                    try:
                        s3.meta.client.head_bucket(Bucket=bucketName)
                        print("Bucket is up and functional")
                    except botocore.exceptions.ClientError as e:
                        error_code = int(e.response['Error']['Code'])
                        if error_code == 404:
                            exists = False
                            print("The bucket you requested does not exist or you do not have the correct permissions")
                    print(exists)
                    time.sleep(2)
        if submain1 == 1:
            exit()
    elif main == 2:
        os.system('aws configure')
        time.sleep(2)
        menu.clearScreen()
        print("Initial setup is complete")
        time.sleep(2)
    elif main == 3:
        break
    else:
        menu.clearScreen()
        print("Please Select a valid option")
        time.sleep(2)
