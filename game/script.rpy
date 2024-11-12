﻿# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
define p = Character("You", color= "#df059a")
define tv = Character("Television")
define f = Character("Friend", color= "#7605df")
define fna = Character("Elder", color="#12a683")
define fnf = Character("Community Member", color="#54cd03")
define s = Character("office receptionist", color="#0050df")
define np = Character("council leader", color="#00bfae")
define pol = Character("politician", color="#00ccff")
define lab_rec = Character("lab_rec", color="#ff0062")
define efor = Character("efor", color="#80ff37")
 

#This will contain all variables
default bedroom_status = False
default count_drawer_Tfrontdoor = False
default count_drawer_Tfrontdoor2 = False
default current_room = 'start'
default fn_status = False
#inventory variables
default keys = False
default newspaper = False
default fn_counter = False
default fn_for = False
default e_counter = False
default e_for = False
default politician = False
#Define a list variable to store kept dialogues
default journal_entries = []
default journal_open = False
#Define for phone system
define p_nvl = Character("You", kind=nvl, color= "#df059a", callback=Phone_SendSound)
define f_nvl = Character("Steve", kind=nvl, color= "#df059a", callback=Phone_ReceiveSound)
define config.adv_nvl_transition = None
define config.nvl_adv_transition = Dissolve(0.3)

#for quiz at the end
default selected_options = []
init python:
    def ToggleSelected(entry):
        # Add or remove the entry from selected_options
        if entry in selected_options:
            selected_options.remove(entry)
        else:
            selected_options.append(entry)

    def check_answers_yes():
        # Define the correct answers for prop
        correct_answers = [
            "Another information bla bla"
        ]
        # Check if the player's selections match the correct answers
        if sorted(selected_options) == sorted(correct_answers):
            renpy.hide_screen("yes_checkquiz")
            renpy.jump("task_passed")
        else:
            renpy.notify("Incorrect or incomplete selection. Try again.")
            selected_options.clear()  # Clear selections if incorrect

    def check_answers_no():
        # Define the correct answers for opp
        correct_answers = [
            "Another information bla bla"
        ]
        # Check if the player's selections match the correct answers
        if sorted(selected_options) == sorted(correct_answers):
            renpy.hide_screen("no_checkquiz")
            renpy.jump("task_passed")
        else:
            renpy.notify("Incorrect or incomplete selection. Try again.")
            selected_options.clear()  # Clear selections if incorrect

#function used for zooming image in 
# how to use it: show image_name at double_size
transform double_size:
    zoom 1.5

#Create a function to add dialogue to the journal
init python:
    def add_to_journal(dialogue):
        if dialogue not in journal_entries:
            journal_entries.append(dialogue)

#Define the screen for the journal
screen journal():
    if journal_open:
        frame:
            align (0.0, 0.2)  # Align the journal to the right side of the screen
            xpadding 10
            ypadding 10
            xsize 400
            ysize 250

            viewport:
                draggable True
                scrollbars "vertical" #Add a vertical scroll bar

                vbox:
                    add "journal_open.png"  xpos 0.5 xanchor 0.5 #Journal icon
                    text "Journal" xalign 0.5 bold True size 20# Title for the journal
                    for entry in journal_entries:
                        text "✅  " + entry style "journal_entry"
# Define the screen for the journal toggle button
screen journal_toggle_button():
    imagebutton:
        action ToggleVariable("journal_open", True, False)
        idle "journal_main.png"
        hover "journal_hover.png"
        align (0.0, 0.0)
#Styles for journal entry
style journal_entry:
    color "#E0E0E0"
    xpadding 10
    ypadding 10
    left_margin 10
    top_margin 5
    bottom_margin 30 
#How to use journal system
# menu:
#         e "Here's some important information you might want to keep."
#         "Take a note.":
#             # Add the dialogue to the journal
#             $ add_to_journal("Another information bla bla")
#             $ renpy.notify("All written down on my journal!")
#         "Skip.":
#             pass  # Do nothing if the player chooses not to keep it


# The game starts here.
label start:

    show screen journal_toggle_button
    show screen journal

    #Tutorial
    $ current_room = "start"
    if bedroom_status:
        scene bk_t_bedroom
        call screen bd_press
    else:
        scene bk_t_bedroom
        p "Waking up to the sound of the TV playing isn't an everyday occurence."
        p "But, as weird as it was. If not for the TV, I wouldn't have known about, THAT."
        play sound "audio/newsbroadcast.mp3"
        tv "BREAKING NEWS: The city council is holding a vote for the construction of the (river name) Dam. For the first time in years, us the people will have a choice on the matter."
        p "Oh."
        p "That river."
        stop sound
        scene bk_river
        play music "audio/naturemusic.mp3" 
        p "I spent a lot of time there with everyone."
        p "Most of it was me just... Trying to get away from life by canoeing or hanging out with my friends."
        p "But now that life's gotten more and more busy, I haven't really had the time to head back there."
        p "Not to mention, everyone else has been too busy to go hangout."
        p "But... If that dam were to be built...."
        scene bk_river_rev
        p "The river from my memories would cease to exist."
        stop music fadeout 1.0
        scene bk_t_bedroom
        play sound "audio/phone_buzz.mp3"
        "Phone" "*bzt* *bzt*"
        p "My phone? Who could be calling at this time?"
        jump phone_talking

#Inventory system
label inventory_room:
    scene inventory_background
    #THESE NEED TO BE ADDED IN INSTANCE
    #$newspaper = True
    #$ fn_counter = True
    #$ fn_for = True
    #$ e_counter = True
    #$ e_for = True
    #$ politician = True
    call screen inventory_icon_room

screen inventory_icon_room:
    if newspaper:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 0.75
            ypos 0.6835
            idle "paper.png"
            hover "paper_hover.png"

    if fn_counter:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 0.25
            ypos 0.25
            idle "evidence5.png"
            hover "evidence5_hover.png"

    if fn_for:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 0.5
            ypos 0.25
            idle "evidence4.png"
            hover "evidence4_hover.png"

    if e_counter:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 0.75
            ypos 0.25
            idle "evidence3.png"
            hover "evidence3_hover.png"

    if e_for:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 0.25
            ypos 0.683
            idle "evidence2.png"
            hover "evidence2_hover.png"

    if politician:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 0.5
            ypos 0.683
            idle "evidence1.png"
            hover "evidence1_hover.png"

    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.5
        ypos 0.9
        idle "back_button.png"
        hover "back_button_hover.png"
        action Jump(current_room)
        
screen bd_press:
    #door
    imagebutton:
        align(0.85, 0.36)
        idle "door.png"
        hover "door_hover.png"
        action Jump("map")
    
    #image_frame
    imagebutton:
        align(0.47, 0.60)
        idle "image_frame.png"
        hover "image_frame_hover.png"

    #newspaper
    imagebutton:
        align(0.20, 0.72)
        idle "paper.png"
        hover "paper_hover.png"
        action SetVariable("newspaper", True)

    #folder
    imagebutton:
        align (0.0, 1.0) 
        idle "folder_main.png"
        hover "folder_hover.png"
        action Jump("inventory_room")


#Phone talking screeen
label phone_talking:
    scene bk_t_bedroom 
    
    #Phone conversation starts here
    
    nvl_narrator "(⁄ ⁄•⁄ω⁄•⁄ ⁄)   (´｡• ᵕ •｡`) ♡"
    play sound "audio/ReceiveText.ogg"
    f_nvl "Yo! Did you see what was on the TV?"
    play sound "audio/SendText.ogg"
    p_nvl "I did, what about it?"
    play sound "audio/ReceiveText.ogg"
    f_nvl "I can’t believe they are making a dam, we always use to go canoeing at the river!"
    play sound "audio/SendText.ogg"
    p_nvl "Yeah.. But we haven't been there in a while."
    play sound "audio/ReceiveText.ogg"
    f_nvl "That doesn't mean that place isn't important anymore!"
    play sound "audio/SendText.ogg"
    p_nvl "..."
    play sound "audio/ReceiveText.ogg"
    f_nvl "Listen. You know how you work for the government? Your choice matters! Maybe... Your vote will make a difference on the council\'s decision to build the dam or not."
    play sound "audio/SendText.ogg"
    p_nvl "But I don't know enough about dams to know if they really should be built or not..."
    play sound "audio/ReceiveText.ogg"
    f_nvl "Well my friend. You can learn."
    play sound "audio/ReceiveText.ogg"
    f_nvl "Some first nation communities located close to the river are protesting. Why don't you go speak to some of them and learn about their perspectives on the situation?"
    play sound "audio/SendText.ogg"
    p_nvl "You know what? That\'s a great idea! I'll head on over right now."

    scene bk_t_bedroom
    p "Alright! No more talking. Let's go exploring!!"
    $ bedroom_status = True
    call screen bd_press


#MAP SECTION STARTS HERE
label map:
    $ current_room = 'map'
    scene map_background
    p "Right, let's head to the neighborhood first to find more about how the dam affects people."
    call screen map_fn
    jump fn_room

screen map_fn:
    #neighborhood
    imagebutton:
        align(0.215, 0.175)
        idle "map_neighborhood.png"
        hover "map_neighborhood_hover.png"
        action Jump("fn_room")

#NEIGHBORHOOD
label fn_room:
    $ current_room = "fn_room"
    if fn_status:
        scene fn_bksr
        p "Am I ready to leave this area?"
        menu:
            "Yep!":
                jump map_en
            "Still something to do.":
                jump choicesfnstay
    else:
        scene fn_bksr
        p "If I walk around I might run into some people to talk to."
        $ fn_status = True
        call screen fnsr_options

label choicesfnstay:
    $ current_room = "choicesfnstay"
    scene fn_bksr
    call screen fnsr_options

screen fnsr_options:
    #left option
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.6
        idle "arrowl.png"
        hover "arrowl_hover.png"
        action Jump("fnl")
    #right option
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.6
        idle "arrowr.png"
        hover "arrowr_hover.png"
        action Jump("fnr")    
    #folder
    imagebutton:
        align (0.0, 1.0) 
        idle "folder_main.png"
        hover "folder_hover.png"
        action Jump("inventory_room")

define fna = Character("Elder", color= "#12a683")
default been_fnl = False
default been_fnr = False

#LEFT ROOM
label fnl:
    if been_fnl:
        scene fn_bkl
        $ current_room = "fnl"
        call screen fnl_options

    else:
        scene fn_bkl
        $ current_room = "fnl"
        $ been_fnl = True
        show fnaagainst at double_size
        p "Hi, I wanted to ask you some questions about the upcoming dam construction vote."
        fna "Of course, what is your question?"
        p "I would like to understand more about what you're advocating for. Could you tell me your opinion on the matter and why it's important to you?"
        fna "For one, I am completely against the whole dam construction idea."
        fna "Our ancestors have lived here for thousands of years. The nearby river is our lifeblood. It is not just water; it is our spirit, our heritage."
        fna "Here's some important information you might want to keep."
        #example of how you integrate a journal system
        menu:
            fna "Here's some important information you might want to keep."
            "Take a note.":
                # Add the dialogue to the journal
                $ add_to_journal("Another information bla bla")
                $ renpy.notify("All written down on my journal!")
            "Skip.":
                pass  # Do nothing if the player chooses not to keep it
        fna "For some, these dams are progress. But to me, they are a means of destruction. They drown our lands, erasing our history and our future."
        menu: 
            "But doesn't powering our society with diesel fuel cause even more harm?":
                jump choicefnl1
            "So, the land provides for you and your community, and in turn you wish to protect it?":
                jump choicefnl2

label choicefnl1:
    fna "While that may be true, the consequences of building a dam are more harmful to my community."
    fna "You see, we lose more than just land; we lose a part of our identity. We lose our the areas where we hunt for food, for fish and deer. The result of the dam would cause flooding in our area, destroying vegetation, stripping the land of its natural resources."
    jump fnl_choice2
label choicefnl2:
    fna "Yes, this is the duty my community has held since the beginning. The land provides for us, we protect it in turn. Besides we use these lands as a means to provide for ourselves."
    jump fnl_choice2

label fnl_choice2:
    menu:
        "But, there's always a different place where you can hunt... With the amount of energy required for society, don't you think we need more dams to help foster this need?":
            jump choicefnl3
        "So, for you, you're generally against this as it is harmful for your community's existence and because it harms your identity?":
            jump choicefnl4

label choicefnl3:
    fna "It seems that you aren't listening to what I have to say."
    fna "Then, I will kindly ask you to leave me be."
    hide fnaagainst at double_size
    p "That... could've gone better."
    p "I didn't get to ask her to add her account to my journal..."
    call screen fnl_options

label choicefnl4:
    fna "Yes."
    p "Would you be willing to write that down in my notebook for me? I wish to learn all that I can about this situation."
    fna "Of course!"
    $ fn_counter = True
    p "Thank you so much!"
    fna "Well I best go back to what I was doing before, take care."
    hide fnaagainst at double_size
    call screen fnl_options

screen fnl_options:
    #right option
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.6
        idle "arrowr.png"
        hover "arrowr_hover.png"
        action Jump("fn_room")    
    #folder
    imagebutton:
        align (0.0, 1.0) 
        idle "folder_main.png"
        hover "folder_hover.png"
        action Jump("inventory_room")

#RIGHT ROOM
define fnf = Character("Community Member", color= "#54cd03")
label fnr:
    scene fn_bkr
    $ current_room = "fnr"
    if been_fnr:
        scene fn_bkr
        p "Is there anything else I need to discuss with the community members here?"
        menu:
            "Yes, let's continue the conversation.":
                jump fnr_dialogue
            "No, I think I'm done here.":
                jump fn_room
    else:
        scene fn_bkr
        $ been_fnr = True
        show fnafor 
        fnf "Excuse me."
        p "Yes?"
        fnf "I couldn’t help but overhear you speaking with other members of our community."
        fnf "I would like to provide my perspective, if you have some spare time."
        p "Yes, I would love to hear your opinion."
        p "What do you think about the construction of a new dam?"

label fnr_opinion_differs:
    fnf "Well, I have the right to my own opinion, don’t I?"
    p "Yes, of course. Please, tell me more about why you support it."

label fnr_support_reason:
    fnf "Building the dam will provide jobs to our people and contracts to First Nation developers."
    fnf "This could really benefit our community economically."

    menu:
        "That’s something I hadn’t considered. Would you mind if I noted this down?":
            # Add dialogue to journal
            $ add_to_journal("Community Member's perspective: The dam could bring economic benefits to the First Nation community.")
            $ renpy.notify("Added to journal!")
            jump fnr_environment

        "I see. What about the environmental impact?":
            jump fnr_environment

label fnr_environment:
    p "Isn’t diesel fuel harmful to the environment?"
    fnf "Oh, absolutely. And spills can contaminate large amounts of water."
    p "Thank you for sharing that perspective with me."

    menu:
        "Take a note on the environmental impact of diesel fuel and the dam.":
            $ add_to_journal("Diesel fuel spills can harm water sources. The dam could reduce reliance on diesel for power.")
            $ renpy.notify("Added to journal!")
        "Skip taking notes.":
            pass  # Do nothing if player chooses not to keep it

    fnf "Thank you for taking the time to listen to me. Have a good day!"
    p "You too, goodbye."

    # End conversation, return to options
    hide fnafor 
    call screen fnr_options

screen fnr_options:
    #left option
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.6
        idle "arrowl.png"
        hover "arrowl_hover.png"
        action Jump("fn_room")
    #folder
    imagebutton:
        align (0.0, 1.0) 
        idle "folder_main.png"
        hover "folder_hover.png"
        action Jump("inventory_room")

#MAP_EN
label map_en:
    $ current_room = 'map_en'
    scene map_background
    p "Right, let's head to the University of Toronto to talk to some experts about the dam."
    call screen map_lab
    jump lab_reception

screen map_lab:
    # University of Toronto lab location
    imagebutton:
        align(0.240, 0.730)
        idle "map_lab.png"
        hover "map_lab_hover.png"
        action Jump("lab_reception")

label lab_reception:
    $ current_room = 'lab_reception'
    scene backgroundlabfront
    show lab_rec with dissolve
    p "I head to the front desk at the University of Toronto's environmental science department."
    p "I need to talk to someone about the dam, but I don't know who to start with."

    lab_rec "Hello! How can I assist you today?"

    p "Hi, I’m looking to speak with a professor regarding the environmental impact of a dam project. Is anyone available?"

    lab_rec "Well, Professor Green is in a lecture at the moment. However, Professor Swift might be available to talk about environmental policies and projects."

    p "Thank you! I'll speak with Professor Swift then."
    jump lab_professor_swift

label lab_professor_swift:
    $ current_room = 'lab_professor_swift'
    scene backgroundlab1
    show efor with dissolve
    p "I knock on Professor Swift's door and enter. She's sitting at her desk surrounded by research papers."
    
    efor "Ah, welcome! How can I help you today?"

    p "Hi, I'm doing research on whether dams are good for environment or not. I was hoping to get your perspective on the environmental impact of a proposed dam. Do you think it's a good idea to build it?"

    efor "Ah, the dam project! It's a significant issue. Well, in terms of the environment, building a dam can have some long-term benefits."
    efor "It provides renewable energy and helps with flood control, especially for nearby communities. Of course, there are environmental impacts too, such as potential loss of biodiversity in the river."

    p "So, you're suggesting the dam could be beneficial in some ways?"

    efor "Yes, exactly. The energy it generates could help reduce carbon emissions, and flood control can protect areas prone to natural disasters. However, we also need to consider how it affects fish populations and aquatic life."

    p "That’s helpful, thank you. I think I’ll add this information to my journal."

    # Option to add journal entry
    menu:
        "Add to journal":
            $ add_to_journal("Professor Swift explains the potential benefits of the dam, including renewable energy generation and flood control, but also highlights environmental concerns like biodiversity loss.")
            p "I’ll make sure to write this down for reference."
        "Don’t add to journal":
            p "I’ll just remember this for now."
    
    p "Thank you for your time, Professor Swift. I’ll head back to the reception desk to check if Professor Green is available yet."

    # show arrow_left
    jump lab_reception2

label lab_reception2:
    $ current_room = 'lab_reception'
    scene backgroundlabfront
    show lab_rec with dissolve
    p "I return to the front desk, hoping to catch Professor Green now that her lecture has finished."

    lab_rec "Ah, you're back! Unfortunately, it might still take a little while for Professor Green to finish. However, I just received a call from Steve."

    play sound "audio/phone_buzz.mp3"
    f_nvl "Yo! Where are you? The politician is really interested in the dam project and is having a press conference in his office right now."

    p_nvl "The politician? I’ll have to check that out, thanks for the heads-up."

    lab_rec "I’ll let you know when Professor Green is ready to meet."

    jump politician_call

label politician_call:
    $ current_room = 'politician_call'
    p "I quickly get in touch with Steve, and he tells me that the politician is attending a press conference at his office. It sounds like the politician is really pushing for the dam’s construction."

    f_nvl "I think you should meet him, he might have more information about the dam’s support from the political side."

    p_nvl "Got it, I’ll go talk to him."
    jump lab_reception3

label lab_reception3:
    $ current_room = 'lab_reception'
    scene backgroundlabfront
    show lab_rec with dissolve
    lab_rec "Ah, finally! Professor Green is available now. You can speak with her about the dam's impact."
    jump lab_professor_green

label lab_professor_green:
    $ current_room = 'lab_professor_green'
    scene backgroundlab2 with dissolve
    show efor at left with fade
    p "I enter Professor Green’s office, and she looks up from her work."

    s "Oh, hello! I’m Professor Sage. I understand you want to discuss the potential impacts of a hydro-electric dam on the Una River?"

    p "Yes, I’d like to hear your thoughts on the downsides."

    s "Certainly. Hydro-electric dams have significant environmental costs. They flood large areas of land, disrupting ecosystems and displacing wildlife."

    menu:
        "Ask about habitat disruption":
            p "How do dams disrupt habitats?"

            s "When land is flooded, entire ecosystems are submerged. Fish, plants, and animals lose their natural habitats."
            s "This can lead to a loss in biodiversity, harming species that rely on the natural river environment."

            p "That sounds serious – I hadn’t thought about it that way."

        "Ask about pollution concerns":
            p "Do hydro-electric dams contribute to pollution?"

            s "Yes, indirectly. When organic material like plants decays underwater, it releases methane, a potent greenhouse gas."
            s "Methane contributes to global warming, sometimes even more than carbon dioxide."

            p "That’s unexpected. I thought hydro-electric power was cleaner."

            s "Cleaner, yes, but not without environmental consequences."

    # Continue the conversation
    p "It seems like there’s a lot to consider. Do you believe the cons outweigh the pros?"

    s "In many cases, yes. There are less invasive alternatives, like wind and solar, that don’t involve flooding or habitat loss."
    s "While dams provide energy, the cost to our ecosystems can be too high."

    menu:
        "Add to journal":
            $ add_to_journal("Professor Sage shared concerns about habitat destruction, methane emissions, and biodiversity loss due to hydro-electric dams.")
            p "I’ll jot this down in my journal."

        "Don’t add to journal":
            p "I’ll keep this in mind for now."


    # show arrow_left
    jump map_to_townhall

#MAP_TO_TOWNHALL (USE JUMP)
label map_to_townhall:
    $ current_room = 'map'
    scene map_background
    p "Now, it is time for you to vote!"
    call screen map_tn
    jump tn_room


screen map_tn:
    #neighborhood
    imagebutton:
        align(0.780, 0.722)
        idle "map_townhall.png"
        hover "map_townhall_hover.png"
        action Jump("tn_room")

label tn_room:
    scene bk_townhall
    p "Alight! I think it is time to show my standign point."
    p "Let me check my note again..."
    show screen voting_buttons

screen voting_buttons:
    add "bk_townhall.png"
    imagebutton:
        #YES: for the dam
        align(0.25, 0.5)
        idle "yes_vote.png"
        hover "yes_vote_hover.png"
        action Show("yes_checkquiz") 

    imagebutton:
        #NO: against the dam
        align(0.75, 0.5)
        idle "no_vote.png"
        hover "no_vote_hover.png"
        action Show("no_checkquiz") 

screen yes_checkquiz:
    add "bk_townhall.png"

    # Create a frame
    frame:
        xsize 500 
        ysize 600
        xalign 0.5 
        yalign 0.5 
        
        # Display the "My Journal" text at the center of the frame
        text "My Journal" at center 
        
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 10  # Space between buttons
            
            # Loop through journal entries and display each as a textbutton
            for entry in journal_entries:
                textbutton entry action [Function(ToggleSelected, entry)]
            
            # Button to check answers
            textbutton "Check Answers" action [Function(check_answers_yes)]

screen no_checkquiz:
    add "bk_townhall.png"

    # Create a frame
    frame:
        xsize 500 
        ysize 600
        xalign 0.5 
        yalign 0.5 
        
        # Display the "My Journal" text at the center of the frame
        text "My Journal" at center 
        
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 10  # Space between buttons
            
            # Loop through journal entries and display each as a textbutton
            for entry in journal_entries:
                textbutton entry action [Function(ToggleSelected, entry)]
            
            # Button to check answers
            textbutton "Check Answers" action [Function(check_answers_no)]

label task_passed:
    p "Congratulations! You've selected the correct answers and passed the task."

label end:
    return
