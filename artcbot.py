#!/Users/sfdavis/anaconda3/bin/python

#ARTCbot. Responds to ! commands 
#Updating the !help is going to be the most difficult to keep up with 

import praw
from config_bot import *
import codecs
from datetime import datetime, timedelta

#Reddit stuff
r = praw.Reddit("ARTCbot 1.0 by herumph")
r.login(REDDIT_USERNAME, REDDIT_PASS)
subreddit = r.get_subreddit("RumphyBot")
#subreddit = r.get_subreddit("artc")
subreddit_comments = subreddit.get_comments()

#Functions to read and write files into arrays.
def get_array(input_string):
    with open(input_string+".txt","r") as f:
        input_array = f.readlines()
    input_array = [x.strip("\n") for x in input_array]
    return(input_array)

def write_out(input_string,input_array):
    with open(input_string+".txt","w") as f:
        for i in input_array:
            f.write(i+"\n")
    return

#Fetching arrays
already_done = get_array("already_done")
command_list = get_array("command_list")

print("\n * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n")

#Getting subreddit contributors
contributors=[]
for contributor in subreddit.get_contributors():
    contributors.append(str(contributor))

#Conversion function
def convert(time, distance, unit,inputs, string):
    if(unit == "miles" or unit == "m" or unit == "mile"):
        distance_conversion = str(round(distance*1.60934,1))
        time_conversion = time/1.60934
        time_conversion = round(time_conversion % 100)
        minutes = round(time_conversion % 100)
        seconds = round((time_conversion % 1)*60)
        str_seconds = str(seconds)
        if(seconds < 10):
            str_seconds = "0"+str(seconds)
        time_sec = time*60.0
        split = int(400.0*time_sec/1609.0)

        #Checking command
        if(string == "!convertdistance"):
            message = str(distance)+" miles is "+distance_conversion+" kilometers."
        if(string == "!convertpace"):
            message = "A "+inputs+" mile is a "+str(minutes)+":"+str_seconds+" kilometer."
        if(string == "!splits"):
            message = "For a "+inputs+" mile, run "+str(split)+" second 400s."

    if(unit == "kilometers" or unit == "km" or unit == "kilometer"):
        conversion = str(round(distance/1.60934,1))
        time_conversion = time*1.60934
        time_conversion = round(time_conversion % 100)
        minutes = round(time_conversion % 100)
        seconds = round((time_conversion % 1)*60)
        str_seconds = str(seconds)
        if(seconds < 10):
            str_seconds = "0"+str(seconds)
        time_sec = time*60.0
        split = int(400.0*time_sec/1000.0)

        #Checking command
        if(string == "!convertdistance"):
            message = str(distance)+" kilometers is "+conversion+" ~~freedom units~~ miles."
        if(string == "!convertpace"):
            message = "A "+inputs+" kilometer is a "+str(minutes)+":"+str_seconds+" mile."
        if(string == "!splits"):
            message = "For a "+inputs+" kilometer, run "+str(split)+" second 400s."

    #Replying
    comment.reply(message)

#Sorting through comments and replying
for comment in subreddit_comments:
	#Adding commands
    if(comment.body.count("!add") and comment.id not in already_done and str(comment.author) in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment_list = str(comment.body)
        comment_list = comment_list.split()
        #Finding command to add
        index = comment_list.index("!add")
        add_command = comment_list[index+1]
        if("!"+add_command in command_list):
            comment.reply("The command !"+add_command+" already exists. Please try !edit instead.")
            break
        #Taking the rest of the comment as the new command and stripping it downs
        new_command = str(comment.body).replace("!add","")
        new_command = new_command.replace(add_command,"",1)
        new_command = new_command.lstrip()
        #Human friendly version of the edit
        temp = new_command
        new_command = new_command.splitlines()
        #Doing fancy shit to make the commands work
        new_command = r'\n'.join(map(str, new_command))
        #Actually adding the command
        command_list.append("!"+add_command)
        command_list.append(new_command)
        write_out('command_list',command_list)
        comment.reply("Successfully added !"+add_command+"\n\n The new response is:\n\n"+temp)

    #Deleting commands
    if(comment.body.count("!delete") and comment.id not in already_done and str(comment.author) in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment_list = str(comment.body)
        comment_list = comment_list.split()
        #Finding command user wants to delete
        index = comment_list.index("!delete")
        delete_command = comment_list[index+1]
        command_index = command_list.index("!"+delete_command)
        #Actually deleting command
        del command_list[command_index]
        del command_list[command_index]
        write_out('command_list',command_list)
        comment.reply("Successfully deleted !"+delete_command)

    #Editing commands
    if(comment.body.count("!edit") and comment.id not in already_done and str(comment.author) in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment_list = str(comment.body)
        comment_list = comment_list.split()
        #Finding command user wants to edit
        index = comment_list.index("!edit")
        edit_command = comment_list[index+1]
        #Taking the rest of the comment as the new command and stripping it down
        new_command = str(comment.body).replace("!edit","")
        new_command = new_command.replace(edit_command,"",1)
        new_command = new_command.lstrip()
        #Human friendly version of the edit
        temp = new_command
        new_command = new_command.splitlines()
        #Doing fancy shit to make the commands work
        new_command = r'\n'.join(map(str, new_command))
        #Making sure the command exists
        if("!"+edit_command not in command_list):
            comment.reply("That command does not exist. Try !add instead.")
            break
        #Actually replacing the command
        command_index = command_list.index("!"+edit_command)
        #Easier to delete both old command and response and append the new ones
        del command_list[command_index]
        del command_list[command_index]
        command_list.append("!"+edit_command)
        command_list.append(new_command)
        write_out('command_list',command_list)
        comment.reply("Successfully edited !"+edit_command+"\n\n The new response is:\n\n"+temp)

    #Replying to users not allowed to edit comments
    if(comment.body.count("!edit") and comment.id not in already_done and str(comment.author) not in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment.reply("Sorry, you are not allowed to edit commands.")
	
    #Replying to users not allowed to add commands
    if(comment.body.count("!add") and comment.id not in already_done and str(comment.author) not in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment.reply("Sorry, you are not allowed to edit commands.")

	#Replying to users not allowed to delete commands
    if(comment.body.count("!delete") and comment.id not in already_done and str(comment.author) not in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment.reply("Sorry, you are not allowed to edit commands.")

    #Splitting up the comment text by white space and seeing if it has any commands
    comment_list = str(comment.body)
    comment_list = comment_list.split()
    common = list(set(comment_list).intersection(command_list))
    #Replying if there is a command
    if(len(common) > 0 and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        command_index = command_list.index(common[0])
        #Having to convert back from raw string
        reply = codecs.decode(command_list[command_index+1], 'unicode_escape')
        comment.reply(reply)

    #Converting distances between km and miles, and vise versa.
    if(comment.body.count("!convertdistance") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = comment_list.index("!convertdistance")
        unit = comment_list[index+2].lower()
        distance = comment_list[index+1]
        distance = float(distance)
        convert(1, distance, unit, "!convertdistance")

    #Converting paces between km/min and miles/min, and vise versa
    if(comment.body.count("!convertpace") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = comment_list.index("!convertpace")
        unit = comment_list[index+2].lower()
        pace = comment_list[index+1]
        pace = pace.split(':')
        pace = float(pace[0])+float(pace[1])/60.0
        convert(pace, 1, unit, comment_list[index+1], "!convertpace")

    #Track split calculator
    if(comment.body.count("!splits") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = comment_list.index("!splits")
        unit = comment_list[index+2]
        pace = comment_list[index+1]
        pace = pace.split(':')
        pace = float(pace[0])+float(pace[1])/60.0
        convert(pace, 1, unit, comment_list[index+1], "!splits")

    #Training plan calculator
    if(comment.body.count("!planner") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = comment_list.index("!planner")
        date = comment_list[index+1]
        formatting = date.split('/')
        #Checking the date format
        if(len(formatting[0]) > 2 or len(formatting[1]) > 2 or len(formatting[2]) > 2):
            comment.reply("Your date is the wrong format. Please put your date in mm/dd/yy format.")
            break
        time= comment_list[index+2]
        date = datetime.strptime(date, "%m/%d/%y")
        time_new = date - timedelta(weeks=int(time))
        comment.reply("For a "+time+" week plan, start training on "+str(time_new.month)+"/"+str(time_new.day)+"/"+str(time_new.year))

    #Race pace calculator
    if(comment.body.count("!pacing") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = comment_list.index("!pacing")
        time = comment_list[index+1]
        time = time.split(':')
        distance = comment_list[index+2]
        unit = comment_list[index+3]
        if(len(time) < 3):
            number_sec = float(time[0])*60.0+float(time[1])
            time = float(time[0])+float(time[1])/60.0
        if(len(time) == 3):
            number_sec = float(time[0])*3600.0+float(time[1])*60.0+float(time[2])
            time = float(time[0])*60.0+float(time[1])+float(time[2])/60.0
        #convert(time, distance, unit, comment_list[index+1], "!pacing")
        if(unit == "miles" or unit == "m" or unit == "mile"):
           split = float(400.0*number_sec/(float(distance)*1609.0))
           mile_split = 1609.0*split/(400.0*60.0)
           print(mile_split)
           test = number_sec/(float(distance)*60.0) #This is the same thing....
           print(test)
        #   tens = round(mile_split % 100)
        #   decimal = round((mile_split % 1)*60)
        #   message = str(tens)+":"+str(decimal)
        #   if(decimal < 10):
        #       message = str(tens)+":0"+str(decimal)
        #   comment.reply("To run "+distance+" "+unit+" in "+comment_list[index+1]+" you need to run each mile in "+message+" minutes.")
        #if(unit == "kilometers" or unit == "km" or unit == "kilometer"):
        #   split = float(400.0*number_sec/(float(distance)*1000.0))
        #   km_split = 1000.0*split/(400.0*60.0)
        #   tens = round(km_split % 100)
        #   decimal = round((km_split % 1)*60)
        #   message = str(tens)+":"+str(decimal)
        #   if(decimal < 10):
        #       message = str(tens)+":0"+str(decimal)
        #   comment.reply("To run "+distance+" "+unit+" in "+comment_list[index+1]+" you need to run each kilometer in "+message+" minutes.")
